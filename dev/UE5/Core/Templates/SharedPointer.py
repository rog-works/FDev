# @see Engine/Source/Runtime/Core/Public/Templates/SharedPointer.h

from typing import Any, Generic, TypeVar

from tranp.app.compatible.cpp.cvar import CP, CW, CRef
from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.annotation import deprecated
from UE5.CoreUObject.UObject.Object import UObject

from compatible.cvar import AtomicCSP
from compatible.error import Errors
from FDev.Main.Core.Lang.Convertion import safe_weak

T_co = TypeVar('T_co', covariant=True)
T_Obj_co = TypeVar('T_Obj_co', bound=UObject, covariant=True)


@Embed.alias('T', prefix=True)
class SharedRef(Generic[T_co]):
	"""C++型変数の互換クラス(スマート参照)

	Note:
		XXX 現状はWidget内のみの利用を想定しているため、CVarと同じ使い方は出来ない
	"""

	__obj: CP[T_co]

	def __init__(self, obj: CP[T_co]) -> None:
		"""インスタンスを生成

		Args:
			obj: インスタンス
		"""
		self.__obj = obj

	@property
	def Get(self) -> CRef[T_co]:
		"""Returns: インスタンス"""
		return self.__obj.ref

	@property
	def sref_on(self) -> T_co:
		"""Returns: 実体を返却するリレー代替メソッド。C++では`->`に相当 @python"""
		return self.__obj.raw

	@property
	def sref_dot(self) -> T_co:
		"""Returns: 実体を返却するリレー代替メソッド。C++では`.`に相当 @python Note: XXX Widgetの@cascadeのメソッドチェーンにのみ利用"""
		return self.__obj.raw

	def ToSharedPtr(self) -> AtomicCSP[T_co]:
		"""Returns: スマートポインター"""
		return AtomicCSP(self.__obj)


@Embed.alias('T', prefix=True)
class ObjectPtr(Generic[T_Obj_co]):
	"""C++型変数の互換クラス(UObject用強参照) Note: @see Engine/Source/Runtime/CoreUObject/Public/UObject/ObjectPtr.h"""

	__obj: CP[T_Obj_co] | None

	def __init__(self, obj: CP[T_Obj_co] | None = None) -> None:
		"""インスタンスを生成

		Args:
			obj: インスタンス (default = None)
		"""
		self.__obj = obj

	@property
	def Get(self) -> CP[T_Obj_co] | None:
		"""Returns: インスタンス | None"""
		return self.__obj


@deprecated
@Embed.alias('T', prefix=True)
class WeakObjectPtr(Generic[T_Obj_co]):
	"""C++型変数の互換クラス(UObject用弱参照) 
	
	Note:
		```
		@see Engine/Source/Runtime/Core/Public/UObject/WeakObjectPtrTemplates.h
		### IsValid vs WeakObjectPtr
		IsValid: 実質的にIsValidCheckedと等価であり、無効判定だけを行うことは出来ない
		WeakObjectPtr: 常に無効判定が可能
		```
	"""

	__obj: CW[T_Obj_co] | None

	def __init__(self, obj: CP[T_Obj_co] | None = None) -> None:
		"""インスタンスを生成

		Args:
			obj: インスタンス (default = None)
		"""
		self.__obj = CW(obj) if obj else None

	@property
	def IsValid(self) -> bool:
		"""Returns: True = 有効"""
		return bool(self.__obj and self.__obj.addr)

	@property
	def Get(self) -> CP[T_Obj_co]:
		"""Returns: インスタンス

		Note:
			```
			* 参照前にIsValidで検証すること
			* C++では無効時にNoneになるが、Pythonではエラーを出力
			```
		"""
		return safe_weak(self.__obj)

	def Reset(self) -> None:
		"""保持している参照を解除"""
		self.__obj = None


def StaticCastSharedRef[T](to_class: type[T], value: SharedRef[Any]) -> SharedRef[T]:
	"""スマート参照型を派生クラスにキャスト。実行時型を検証し、不正な変換の場合はアサーションを出力

	Args:
		to_class: 変換後のクラス
		value: インスタンス
	Returns:
		キャスト後のインスタンス
	Raises:
		TypeError: 不正な変換先を指定
	"""
	if not isinstance(value.Get, to_class):
		raise Errors.IncompatibleConvertion(value.Get.__class__, to_class)

	return value


def ToSharedRef[T](value: AtomicCSP[T]) -> SharedRef[T]:
	"""スマート参照に変換

	Returns:
		スマート参照
	Note:
		XXX 本来はSharedPtr.ToSharedRef"""
	return SharedRef(value.addr)
