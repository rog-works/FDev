# @see Engine/Source/Runtime/CoreUObject/Public/UObject/Object.h

from abc import abstractmethod
from collections.abc import Callable
from enum import Enum
from importlib import import_module
from types import TracebackType
from typing import Annotated, Any, ClassVar, Generic, Self, TypeIs, TypeVar, cast, override

from tranp.app.compatible.cpp.classes import uint64, void
from tranp.app.compatible.cpp.cvar import CP, CRaw, CRef, CVar
from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.annotation import deprecated
from tranp.app.lang.typehint import ClassTypehint
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, Abstract, EmbedKeys

from App.Main.Const.ProjectConst import PackagePrefixs, ProjectConst
from compatible.error import Errors

T_Obj = TypeVar('T_Obj', bound='UObject')


@Embed.python
class _EnumLikeFlags:
	"""Enum風のビットフィールド

	Note:
		Enumをビットフィールドで使用すると言うあり得ない実装のため代替クラスを用意
	"""

	__flags: int

	def __init__(self, flags: int = 0) -> None:
		"""インスタンスを生成 Args: flags: 初期値"""
		self.__flags = flags

	def __eq__(self, other: Self) -> bool:
		"""Args: other: 対象 Returns: True = 一致"""
		return self.__flags == other.__flags

	def __and__(self, other: Self) -> Self:
		"""Args: other: 対象 Returns: 演算結果"""
		return self.__class__(self.__flags & other.__flags)

	def __or__(self, other: Self) -> Self:
		"""Args: other: 対象 Returns: 演算結果"""
		return self.__class__(self.__flags | other.__flags)
	
	def __int__(self) -> int:
		"""Returns: 数値"""
		return self.__flags

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: {hex(self.__flags)}>'

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return self.__flags


@Embed.alias('E', prefix=True)
class ObjectFlags(_EnumLikeFlags):
	"""オブジェクトフラグ Note: 定義位置が不自然なため移設 @see ObjectMacros.h"""
	...


@Embed.alias('EObjectFlags')
class ObjectFlags_:
	"""オブジェクトフラグ @python

	Note:
		RF_Public: パッケージ外でも表示 XXX 詳細不明
		RF_Standalone: 編集のためにオブジェクトを保持 XXX 詳細不明
		RF_ClassDefaultObject: CDO
	"""

	RF_NoFlags: ClassVar = ObjectFlags(0x0000)
	RF_Public: ClassVar = ObjectFlags(0x0001)
	RF_Standalone: ClassVar = ObjectFlags(0x0002)
	RF_ClassDefaultObject: ClassVar = ObjectFlags(0x0010)


@Embed.alias('E', prefix=True)
class ClassFlags(_EnumLikeFlags):
	"""クラスフラグ Note: 定義位置が不自然なため移設 @see ObjectMacros.h"""
	...


@Embed.alias('EClassFlags')
class ClassFlags_:
	"""クラスフラグ @python

	Note:
		CLASS_Native: ネイティブクラス(C++で実装)
	"""

	CLASS_Native: ClassVar = ClassFlags(0x80)


@Embed.alias('E', prefix=True)
class PropertyFlags(_EnumLikeFlags):
	"""オブジェクトフラグ Note: 定義位置が不自然なため移設 @see ObjectMacros.h"""
	...


@Embed.alias('EPropertyFlags')
class PropertyFlags_:
	"""プロパティーフラグ @python

	Note:
		```
		CPF_BlueprintVisible: ローカル変数/引数
		CPF_Net: レプリケーション対象
		CPF_Parm: 引数
		CPF_OutParm: 引数
		CPF_ReturnParm: 戻り値(C++の関数のみ)
		CPF_SaveGame: セーブデータの保存対象
		```
	"""

	CPF_None: ClassVar = PropertyFlags(0)
	CPF_BlueprintVisible: ClassVar = PropertyFlags(0x0004)
	CPF_Net: ClassVar = PropertyFlags(0x0020)
	CPF_Parm: ClassVar = PropertyFlags(0x0080)
	CPF_OutParm: ClassVar = PropertyFlags(0x0100)
	CPF_ReturnParm: ClassVar = PropertyFlags(0x0400)
	CPF_SaveGame: ClassVar = PropertyFlags(0x1000000)


@Embed.alias('E', prefix=True)
class ClassCastFlags:
	"""クラスキャストフラグ"""
	CASTCLASS_FInt8Property: ClassVar = uint64(0x0000000000000002)
	CASTCLASS_FByteProperty: ClassVar = uint64(0x0000000000000040)
	CASTCLASS_FIntProperty: ClassVar = uint64(0x0000000000000080)
	CASTCLASS_FFloatProperty: ClassVar = uint64(0x0000000000000100)
	CASTCLASS_FUInt64Property: ClassVar = uint64(0x0000000000000200)
	CASTCLASS_FClassProperty: ClassVar = uint64(0x0000000000000400)
	CASTCLASS_FUInt32Property: ClassVar = uint64(0x0000000000000800)
	CASTCLASS_FNameProperty: ClassVar = uint64(0x0000000000002000)
	CASTCLASS_FStrProperty: ClassVar = uint64(0x0000000000004000)
	CASTCLASS_FObjectProperty: ClassVar = uint64(0x0000000000010000)
	CASTCLASS_FBoolProperty: ClassVar = uint64(0x0000000000020000)
	CASTCLASS_FStructProperty: ClassVar = uint64(0x0000000000100000)
	CASTCLASS_FArrayProperty: ClassVar = uint64(0x0000000000200000)
	CASTCLASS_FInt64Property: ClassVar = uint64(0x0000000000400000)
	CASTCLASS_FTextProperty: ClassVar = uint64(0x0000000040000000)
	CASTCLASS_FDoubleProperty: ClassVar = uint64(0x0000000100000000)
	CASTCLASS_FMapProperty: ClassVar = uint64(0x0000400000000000)
	CASTCLASS_FEnumProperty: ClassVar = uint64(0x0001000000000000)


class FunctionFlags(_EnumLikeFlags):
	"""関数フラグ @see Script.h"""
	...


@Embed.alias('EFunctionFlags')
class FunctionFlags_:
	"""関数フラグ"""

	FUNC_Static: ClassVar = FunctionFlags(0x00002000)


@UCLASS()
class UObjectBase:
	"""UObjectの基底クラス

	Note:
		通常このクラスを意識する必要はない。特別な理由がない限りUObjectを使用すること
	"""

	@abstractmethod
	def GetClass(self) -> 'CP[UClass]':
		"""自身のクラスの型情報を取得

		Returns:
			クラスの型情報
		"""
		raise Errors.MustBeImplemented

	@abstractmethod
	def GetOuter(self) -> 'CP[UObject]':
		"""管理オブジェクトを取得

		Returns:
			管理オブジェクト
		"""
		raise Errors.MustBeImplemented


@UCLASS()
class UObject(UObjectBase):
	"""オブジェクトの共通基底クラス"""

	OuterPrivate: 'CP[UObject] | None'
	NamePrivate: Name

	def __init__(self) -> None:
		"""インスタンスを生成

		Note:
			必ず引数なしでインスタンス化できるようにすること ※メンバー変数も同様
		"""
		super().__init__()
		# XXX 本来はプライベートだが、生成時に外部で設定が必要なため公開
		self.OuterPrivate = None
		self.NamePrivate = Name()

	@Embed.python
	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: "{self.GetName()}" @ {CP(self)}>'

	@classmethod
	@Embed.python
	def StaticClass(cls) -> 'CP[UClass]':
		"""クラスの型情報を取得 @python

		Returns:
			クラスの型情報
		Raises:
			IllegalSchema: UCLASSの設定不備
		Note:
			```
			* XXX 本来はコードジェネレーターによって各クラスに直接定義されるメソッド
			* XXX UObjectのメソッドではないが、便宜上必要なため定義
			```
		"""
		if not hasattr(cls, EmbedKeys.Class.value):
			raise Errors.IllegalSchema(cls)

		return Classes.uclass_by(cls)

	@Embed.allow_override
	@deprecated
	def post_init_properties(self) -> None:
		"""インスタンス初期化時の処理

		Note:
			```
			本来はCDO回避/基底クラスの呼び出しが必須だが、テンプレートで省略 @see data/template/function/_post_init_properties.j2
			### 前提
			* 公開メンバーの初期化は一時データに共有される
			* 公開メンバーはPostInitPropertiesの前後で一時データがコピーされる
			XXX ※クラスや構造体によっても結果が異なる。詳細は不明だが、一時データがコピーされるのは事実
			### PostInitPropertiesの実装スキーム
			* 公開メンバー: 一時データのコピーにより、様々な問題を引き起こす可能性があるため禁止
			* 非公開メンバー: 一応問題はないが、コンストラクター内で初期化する方が良い
			* 結論: 非推奨。代替手段(BeginPlay等)に置き換える方がベター
			### 一時データのコピーパターン
			* Replicatedなし/UObject: インスタンスの置き換え ※ XXX 予想
			* Replicatedなし/非UObject: 代入 ※operator=によって確認可能
			* Replicated: 同期開始タイミングで置き換え ※タイミングはBeginPlayの後である可能性も有り
			```
		"""
		...

	# XXX 一旦備忘録として追加
	# @Embed.allow_override
	# def PostLoad(self) -> None:
	# 	"""デシリアライズ時の処理 Note: CDOでも実行される点に注意"""
	# 	...

	def __del__(self) -> None:
		"""インスタンスを破棄"""
		self.begin_destroy()

	@Embed.allow_override
	def begin_destroy(self) -> None:
		"""インスタンスリリース時の処理

		Note:
			```
			本来はCDO回避/基底クラスの呼び出しが必須だが、テンプレートで省略 @see data/template/function/_begin_destroy.j2
			### 解放処理に関する留意事項
			* GCは生成した順序と逆順にインスタンスを解放する
			* 親がGC回収される際、保持している子から先にBeginDestroyが実行される
			* 親のBeginDestroy内で子は既に解放済みであるため、子に対してはアドレスを参照する以外は何も行ってはならない
			### 解放処理の実装スキーム
			* 解放処理が必要な場合、独自にライフサイクルを実装する。BeginDestroyは使ってはならない
			* BeginDestroyでは、実装したライフサイクルが正常かどうかを確認するだけの用途に留める
			```
		"""
		...

	@override
	def GetClass(self) -> 'CP[UClass]':
		"""自身のクラスの型情報を取得

		Returns:
			クラスの型情報
		"""
		return Classes.uclass_by(self.__class__)

	@override
	def GetOuter(self) -> 'CP[UObject]':
		"""管理オブジェクトを取得

		Returns:
			管理オブジェクト
		"""
		if not self.OuterPrivate:
			raise Errors.Never(self)

		return self.OuterPrivate

	def GetTypedOuter(self, outer_type: 'type[T_Obj]') -> CP[T_Obj] | None:
		"""オブジェクト階層を辿って指定の型の管理オブジェクトを取得。未検出の場合はNoneを返却

		Args:
			outer_type: 対象の型
		Returns:
			管理オブジェクト
		"""
		curr = self.OuterPrivate
		while curr and not isinstance(curr.raw, outer_type):
			curr = curr.raw.OuterPrivate

		if curr is not None and isinstance(curr.raw, outer_type):
			return curr.down(outer_type)

		return None

	def GetName(self) -> str:
		"""名前を取得。取得される値はオブジェクトの種類によって異なる @python

		Returns:
			名前
		Note:
			```
			@see UObjectBaseUtility.h UObjectBaseUtility
			### 書式
			* 型情報: '{クラス名}'
			* インスタンス: '{クラス名}_{管理番号}'
			### 注意事項
			* このメソッドからは接頭辞付きのオリジナルの型名は取得できない
			```
		"""
		return f'{self.__class__.__name__}_{CP(self)}' if self.GetFName().GetStringLength() == 0 else self.GetFName().ToString()

	def GetFName(self) -> Name:
		"""NewObjectで設定された名前を取得

		Returns:
			名前
		Note:
			@see UObjectBase.h
			```
			### 注意事項
			* あくまでもNewObjectによって設定された名前
			* 取得できる名前が確実なものであるかどうかはユースケース次第
			* 通常のインスタンスではこの名前に依存するべきではない
			### 依存が許容されるパターン
			* Actor配下のコンポーネント
			* UserWidget配下のUIコンポーネント
			```
		"""
		if isinstance(self, UStruct):
			raise Errors.NotAllowed(self)

		return self.NamePrivate

	def GetPathName(self) -> str:
		"""インスタンスを表す一意なパス名を取得

		Returns:
			DSN
		Note:
			```
			@see UObjectBaseUtility.h UObjectBaseUtility
			* 所有するオブジェクトを再帰的に辿って取得するようなので負荷が高いであろう点に注意
			* 非常に複雑で難解な書式であり、事前の予想はほぼ不可能。これを基に何かを管理してはならない
			* おそらくオンラインの同期処理でインスタンスを特定するのに利用される
			### 書式 ※無数にパターンがあるため、ほんの一例
			* プロジェクト内(C++): '/Script/{プロジェクト名}.{クラス名}[.{インスタンス名}]'
			* プロジェクト内(エディター): '/Game/{Contentからの相対パス}/{クラス名}[.{インスタンス名}]'
			* UE: '/{未確認}/{クラス名}[.{インスタンス名}]'
			```
		"""
		return f'{self.GetClass().on.GetPathName()}.{self.GetName()}'

	def IsA(self, expect_uclass: 'CP[UClass]') -> bool:
		"""自身が指定のクラスと同じか派生クラスか判定

		Args:
			expect_uclass: 期待するクラスの型情報
		Returns:
			True = 同じか派生クラス
		Note:
			```
			@see UObjectBaseUtility
			### 注意点
			* このメソッドを型情報のインスタンスから呼び出してはならない
			* 以下の様に型情報を経由すると結果がFalseになる場合がある ※UObjectのままであればTrue
			* `CastChecked(Struct, instance.on.GetClass()).on.IsA(same_uclass)`
			### アクセス制限に関して
			* C++ではStruct/UObjectのみpublic、Classではprivate
			```
		"""
		if isinstance(self, UStruct):
			raise Errors.IncompatibleConvertion(self)

		return issubclass(self.__class__, expect_uclass.on.origin)

	def IsIn(self, outer: 'CP[UObject]') -> bool:
		"""指定の管理オブジェクトの配下か判定

		Args:
			outer: 管理オブジェクト
		Returns:
			True = 配下
		Note:
			```
			* XXX 基本的に特定のワールド配下か判定する目的で以外で使用しない想定
			* XXX Pythonではワールドを考慮する必要がないため常にTrueを返却
			@see UObjectBaseUtility.h
			```
		"""
		return True

	def HasAnyFlags(self, flags: ObjectFlags) -> bool:
		"""指定のオブジェクトフラグを所持しているか判定

		Args:
			flags: オブジェクトフラグ
		Returns:
			True = 所持
		Note:
			```
			* @see UObjectBaseUtility.h UObjectBaseUtility
			* 前提が不明なため、初期値はフラグ無しとする ※必要であればオーバーライドかモックで対応
			```
		"""
		self_flags = ObjectFlags_.RF_NoFlags
		return (int(self_flags) & int(flags)) != 0

	def SetFlags(self, flags: ObjectFlags) -> None:
		"""オブジェクトフラグを設定

		Args:
			flags: オブジェクトフラグ
		Note:
			XXX 現状は何も設定しない
		"""
		...

	def ProcessEvent(self, ufunc: 'CP[UFunction]', params_and_returns_at: CP[void]) -> None:
		"""関数のコールプロクシー @python

		Args:
			ufunc: 関数の型情報
			params_and_returns_at: 引数＋戻り値の属性を持つインスタンスのアドレス
		"""
		is_object = not isinstance(self, UStruct)
		is_class = isinstance(self, UClass)
		if not (is_object or is_class):
			raise Errors.Never(self, ufunc)

		params_obj = cast(object, params_and_returns_at.raw)
		params = {key: value for key, value in params_obj.__dict__.items() if not key.startswith('__') and key != 'ReturnValue'}
		method: Callable[..., Any] = getattr(self if is_object else self.origin, ufunc.on.GetName())
		# XXX `not callable`はpropertyである想定
		result = method(**params) if callable(method) else method
		if hasattr(params_obj, 'ReturnValue'):
			setattr(params_obj, 'ReturnValue', result)

	def CreateDefaultSubobject(self, returned_type: type[T_Obj], name: Name | str) -> CP[T_Obj]:
		"""自身の配下用にオブジェクトを生成

		Args:
			returned_type: 生成するオブジェクトのクラス
			name: 名前 ※変数名と別名を指定すると重複定義されるため、必ず同名を指定すること。strはリテラルのみ
		Returns:
			生成したオブジェクト
		"""
		return NewObject(returned_type, CP(self), returned_type.StaticClass(), name)


class Field:
	"""プロパティー(基底)"""
	...


@UCLASS()
class UStruct(UObject):
	"""構造体・クラス・関数の型情報 @see Public/UObject/Class.h"""

	origin: type[Any]
	cvar: type[CVar]
	props: list[CP[Field]]

	def __init__(self, origin: type[Any]) -> None:
		"""インスタンスを生成 @python

		Args:
			origin: クラス ※実際はUObject、または構造体(Python上はただのclass)
		"""
		super().__init__()
		# @python
		self.origin = origin
		self.cvar = CRaw
		self.props = []

	@override
	def GetName(self) -> str:
		"""Returns: 名前 @python"""
		return self.origin.__name__

	@override
	def GetPathName(self) -> str:
		"""Returns: DSN"""
		return f'{PackagePrefixs.Script}/{ProjectConst.Name}.{self.GetName()}'

	@override
	def GetClass(self) -> 'CP[UClass]':
		"""Returns: クラスの型情報 @python"""
		if self.__class__ is UStruct:
			raise Errors.NotAllowed(self)

		return Classes.uclass_by(self.origin)

	def GetStructureSize(self) -> int:
		"""Returns: 構造体・クラスのバイナリサイズ (typeofの結果と同等) @python"""
		# XXX Pythonで再現が困難な割に、大して重要ではないため1を返す
		return 1

	@Embed.python
	def dirty_apply_props(self, props: list[CP[Field]]) -> None:
		"""Args: プロパティーリスト"""
		self.props = props

@Embed.python
class GenStruct:
	"""構造体用の基底クラス @python

	Note:
		* XXX 本来はコードジェネレートされる定義だが、再現出来ないためクラス形式で実装
		* XXX USTRUCTでアノテーションされるクラスは必ず継承する必要がある
		* XXX このクラスの継承はC++では暗黙的に除外される @see data/template/class/_inherits.j2
	"""

	@classmethod
	def StaticStruct(cls) -> CP[UStruct]:
		"""構造体の型情報を取得 @python

		Returns:
			構造体の型情報
		Raises:
			IllegalSchema: USTRUCTの設定不備
		"""
		if not hasattr(cls, EmbedKeys.Struct.value):
			raise Errors.IllegalSchema(cls)

		return Classes.utype_by(cls)


@UCLASS()
class UFunction(UStruct):
	"""関数の型情報 @see Public/UObject/Class.h

	Note:
		```
		ParmsSize: 全ての引数と戻り値の型の合計バイナリサイズ
		ReturnValueOffset: 戻り値のアドレスまでのオフセット(？) XXX 意味不明な値(65535)になる。扱いにくいので使用しない
		```
	"""

	ParmsSize: int
	method: Callable

	def __init__(self, origin: type[UObject], method: Callable) -> None:
		"""インスタンスを生成 @python

		Args:
			origin: クラス @see Struct
			method: メソッド @python
		"""
		super().__init__(origin)
		self.ParmsSize = 0
		# @python
		self.method = method

	@override
	def GetName(self) -> str:
		"""Returns: 名前 @python Note XXX メソッド名が翻訳された場合正しくならない"""
		if isinstance(self.method, property):
			return getattr(self.method, 'fget').__name__
		else:
			return self.method.__name__

	@override
	def GetPathName(self) -> str:
		"""Returns: DSN"""
		return f'{self.GetClass().on.GetPathName()}:{self.GetName()}'

	def GetOuterUClass(self) -> 'CP[UClass]':
		"""Returns: クラスの型情報

		Note:
			```
			* XXX GetClassと結果が変わらないなら、このメソッドの必要性は？
			* XXX UObject::FindFunctionからFunctionを取得した場合と、UClass::FindFunctionByNameの違いを吸収するため？
			```
		"""
		return self.GetClass()

	def HasAnyFunctionFlags(self, flags: FunctionFlags) -> bool:
		"""指定の関数フラグを保持しているか判定

		Args:
			関数フラグ
		Returns:
			True = 有効
		"""
		if (int(flags) & int(FunctionFlags_.FUNC_Static)) != 0:
			return isinstance(getattr(self.method, '__self__'), type)

		return False


# @deprecated
# @Embed.alias('U', prefix=True)
# @UCLASS()
# class Interface(Struct):
# 	"""インターフェイス @see Public/UObject/Class.h Note: @deprecated 非推奨"""
# 	...


@UCLASS()
class UClass(UStruct):
	"""クラスの型情報 @see Public/UObject/Class.h"""

	def __init__(self, origin: type[Any]) -> None:
		"""インスタンスを生成 @python

		Args:
			origin: クラス @see Struct
		"""
		super().__init__(origin)
		self.cvar = CP

		hint = ClassTypehint(origin)
		if hint.origin is CP:
			self.origin = hint.sub_types[0].origin
		elif hint.origin is CRef:
			self.origin = cast(ClassTypehint, hint.sub_types[0]).sub_types[0].origin
			self.cvar = CRef

		if not issubclass(self.origin, UObject):
			raise Errors.InvalidArguments(origin)

	def IsChildOf(self, super_uclass: 'CP[UClass]') -> bool:
		"""自身が引数のクラスの派生クラスか検証

		Args:
			super_uclass: 期待する基底クラスの型情報
		Returns:
			True = 同じか派生クラス
		"""
		return issubclass(self.origin, super_uclass.on.origin)

	def GetSuperClass(self) -> 'CP[UClass] | None':
		"""Returns: 親クラス | None Note: 単一継承である前提。UObjectではNoneを返却"""
		if self.origin == UObject:
			return None

		return Classes.uclass_by(self.origin.mro()[1])

	def HasAnyClassFlags(self, flags: ClassFlags) -> bool:
		"""指定のクラスフラグを所持しているか判定

		Args:
			flags: クラスフラグ
		Returns:
			True = 所持
		Note:
			XXX ネイティブクラスのみ判定
		"""
		self_flags = ClassFlags_.CLASS_Native
		return (int(self_flags) & int(flags)) != 0

	def FindFunctionByName(self, name: Name | str, raised_no_embed: bool = True) -> CP[UFunction] | None:
		"""関数の型情報を取得

		Args:
			name: 関数の名前 ※strはリテラルのみ
			raised_no_embed: True = UFUNCTIONが無い関数を検索するとエラーを出力 (default = True) @python
		Returns:
			関数の型情報
		Raises:
			IllegalSchema: UFUNCTIONの設定不備
		"""
		_name: str = name.ToString() if isinstance(name, Name) else name
		if not hasattr(self.origin, _name):
			return None

		func = getattr(self.origin, _name)
		embeded = is_embed_function_recursive(self.origin, _name)
		if not embeded and raised_no_embed:
			raise Errors.IllegalSchema(self.origin, _name)
		elif not embeded:
			return None

		return Classes.ufunc_by(self.origin, func)


@Embed.python
def is_embed_function_recursive(origin: type[Any], name: str) -> bool:
	"""クラスチェーンを辿ってアノテーション済みの関数か判定

	Args:
		origin: オリジン
		name: 関数の名前
	Returns:
		True = アノテーション済み
	"""
	for class_type in origin.mro():
		func = getattr(class_type, name)
		func = getattr(func, 'fget') if type(func) is property else func
		if hasattr(func, EmbedKeys.Function.value):
			return True
		elif not hasattr(func, '__override__'):
			break

	return False


class UEnum:
	"""Enumの型情報

	Note:
		```
		@see Class.h UEnum
		XXX 実際はUFieldの派生クラス
		```
	"""

	enum_origin: type[Enum]

	def __init__(self, enum_origin: type[Enum]) -> None:
		"""インスタンスを生成

		Args:
			enum_origin: Enumのクラス
		"""
		self.enum_origin = enum_origin

	def GetName(self) -> str:
		"""Returns: 型名"""
		return self.enum_origin.__name__


@Embed.alias('F', prefix=True)
class SoftObjectPath:
	"""ソフトオブジェクトパス @see Public/UObject/SoftObjectPath.h"""

	_dsn: str

	def __init__(self, dsn: str) -> None:
		"""インスタンスを生成

		Args:
			dsn: DSN
		"""
		# @python
		self._dsn = dsn

	def ToString(self) -> str:
		"""str: 文字列表現"""
		return self._dsn


@Embed.alias('T', prefix=True)
class SoftObjectPtr(Generic[T_Obj]):
	"""ソフトオブジェクトポインター @see Public/UObject/SoftObjectPtr.h"""

	def __init__(self, path: SoftObjectPath) -> None:
		"""インスタンスを生成

		Args:
			path: ソフトオブジェクトパス
		"""
		...

	def LoadSynchronous(self, module_path: str = '', class_name: str = '', method_name: str = '') -> CP[T_Obj] | None:
		"""型情報をロード @python

		Args:
			module_path: モジュールパス (default = '') @python
			class_name: クラス名 (default = '') @python
			method_name: メソッド名 (default = '') @python
		Returns:
			型情報
		"""
		return self.__resolve_utype(self.__load_origin(module_path, class_name), method_name)

	def __load_origin(self, module_path: str, class_name: str) -> type[Any]:
		"""クラスをロード @python

		Args:
			module_path: モジュールパス
			class_name: クラス名
		Returns:
			クラス
		"""
		return getattr(import_module(module_path), class_name)

	def __resolve_utype(self, origin: type[T_Obj], method_name: str) -> CP[Any]:
		"""型情報を解決 @python

		Args:
			origin: オリジン
			method_name: メソッド名
		Returns:
			型情報
		"""
		if len(method_name) > 0:
			ufunc = origin.StaticClass().on.FindFunctionByName(method_name)
			if not ufunc:
				raise Errors.Never(origin, method_name)

			return ufunc
		elif issubclass(origin, GenStruct):
			return origin.StaticStruct()
		else:
			return origin.StaticClass()


@Embed.struct
@Embed.alias('F', prefix=True)
class SavePackageArgs:
	"""パッケージの保存引数

	Note:
		```
		XXX このクラスを使うためには以下のファイルのインポートが必須
		XXX 循環参照回避のためにこのファイルに定義
		@see Public/UObject/SavePackage.h
		```
	"""

	TopLevelFlags: ObjectFlags

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.TopLevelFlags = ObjectFlags_.RF_NoFlags


@Embed.alias('U', prefix=True)
@UCLASS()
class Package(UObject):
	"""パッケージ

	Note:
		```
		* 実質的にアセットと同義であり、アセットのインスタンスと対になるデータ
		* アセットのファイル情報がパッケージと言う理解で良いと思われる
		@see Public/UObject/Package.h
		```
	"""

	class MetaData:
		"""メタデータコンテナー

		Note:
			```
			XXX 本来は単独のクラスである点に注意
			@see MetaData.h
			```
		"""

		def GetValue(self, asset: CP[UObject], key: bytes) -> str:
			"""メタデータを取得

			Args:
				asset: アセット
				key: キー ※TCHAR型
			Returns:
				メタデータ
			"""
			return ''

		def SetValue(self, asset: CP[UObject], key: bytes, value: bytes) -> None:
			"""メタデータを設定

			Args:
				asset: アセット
				key: キー ※TCHAR型
				value: 値 ※TCHAR型
			"""
			...

	def FullyLoad(self) -> None:
		"""パッケージを完全に読み込む。繰り返しても安全"""
		...

	@classmethod
	def SavePackage(cls, outer: 'CP[Package]', asset: CP[UObject], filepath: bytes, save_args: Annotated['SavePackageArgs', Embed.immutable]) -> bool:
		"""オブジェクトをアセットとしてストレージに保存

		Args:
			outer: パッケージ
			asset: インスタンス
			filepath: ファイルパス
			save_args: パッケージの保存引数 @immutable
		Returns:
			True = 成功
		"""
		return True

	def GetMetaData(self) -> CRef[MetaData]:
		"""Returns: メタデータコンテナー Note: ローカル変数などに展開して型を明示出来ない点に注意"""
		return CRef(Package.MetaData())

	@classmethod
	def from_asset_path(cls, asset_path: str) -> 'CP[Package]':
		"""アセットパスを元にパッケージを生成

		Args:
			asset_path: Contentからの相対アセットパス
		Returns:
			インスタンス
		Note:
			```
			XXX アセット毎のパッケージとして、例外的に独立したインスタンスを生成
			@see Objects.package_by_name
			```
		"""
		instance = CP(cls())
		instance.on.NamePrivate = Name(f'{PackagePrefixs.Game}/{asset_path}')
		return instance


def FindPackage(outer: CP[UObject] | None, package_path: bytes) -> CP[Package]:
	"""パッケージを検索

	Args:
		outer: 管理オブジェクト | None
		package_path: パッケージパス ※TCHAR*のためbytes型とする
	Returns:
		パッケージ
	Examples:
		```python
		FindPackage(outer=None, package_name='/Script/{project_name}')
		```
	Note:
		```
		* Objectでは明示的にインポートしていないが、UnrealTypeからインポートされているため、ほぼ同条件で使えると言う前提でこのモジュールに定義
		* @see Engine/Source/Runtime/CoreUObject/Public/UObject/UObjectGlobals.h
		```
	"""
	return Objects.package_by_name(package_path.decode())


@Embed.python
class Objects:
	"""オブジェクト管理 @python"""

	__instance: ClassVar['Objects | None'] = None

	__packages: dict[str, CP[Package]]
	__tracking: bool
	__trackings: list[CP[UObject]]

	@classmethod
	def instance(cls) -> 'Objects':
		"""Returns: シングルトンインスタンス"""
		if cls.__instance is None:
			cls.__instance = cls()

		return cls.__instance

	@classmethod
	def transient_package(cls) -> CP[Package]:
		"""Returns: パッケージ(Transient)"""
		return cls.package_by_name(f'{PackagePrefixs.Script}/Transient')

	@classmethod
	def package_by_utype(cls, utype: CP[UStruct]) -> CP[Package]:
		"""Args: utype: 型情報 Returns: パッケージ"""
		elems = utype.on.origin.__module__.split('.')
		if elems[0] == 'App' and elems[1] != 'Main':
			return cls.package_by_name(f'{PackagePrefixs.Script}/{ProjectConst.Name}{elems[1]}')
		elif elems[0] == 'App' or elems[0] == 'tests':
			return cls.package_by_name(f'{PackagePrefixs.Script}/{ProjectConst.Name}')
		else:
			return cls.package_by_name(f'{PackagePrefixs.Script}/{elems[1]}')

	@classmethod
	def package_by_name(cls, package_name: str) -> CP[Package]:
		"""Args: パッケージ名 Returns: パッケージ"""
		instance = cls.instance()
		if package_name not in instance.__packages:
			package = CP(Package())
			package.on.NamePrivate = Name(package_name)
			instance.__packages[package_name] = package

		return instance.__packages[package_name]

	@classmethod
	def tracking(cls) -> 'Objects':
		"""オブジェクトトラッキング開始

		Note:
			トラッキング中に生成したオブジェクトをGCから保護
		"""
		return cls.instance()

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.__packages = {}
		self.__tracking = False
		self.__trackings = []

	def __enter__(self) -> 'Objects':
		"""コンテキストマネジメント(開始)"""
		self.__tracking = True
		self.__trackings.clear()
		return self
	
	def __exit__(self, exc_type: type[BaseException], exception: BaseException, traceback: TracebackType) -> None:
		"""コンテキストマネジメント(終了)"""
		self.__tracking = False
		self.__trackings.clear()

	def new_object(self, origin: type[UObject], outer: CP[UObject], name: Name | str, **kwargs: Any) -> CP[UObject]:
		"""オブジェクトを生成

		Args:
			origin: 型
			outer: 管理オブジェクト
			name: 名前 ※strはリテラルのみ
			**kwargs (Any): キーワード引数 @test
		Returns:
			オブジェクト
		"""
		instance = CP(origin(**kwargs))
		self.set_private(instance, outer, name if isinstance(name, Name) else Name(name))
		instance.on.post_init_properties()
		if self.__tracking:
			self.__trackings.append(instance)

		return instance

	@classmethod
	def set_private(cls, instance: CP[UObject], outer: CP[UObject], name: Name) -> None:
		"""UObjectの非公開メンバーを設定

		Args:
			instance: インスタンス
			outer: 管理オブジェクト
			name: 名前
		"""
		instance.on.OuterPrivate = outer
		instance.on.NamePrivate = name


@Embed.python
class Classes:
	"""型情報管理"""

	__utypes: ClassVar[dict[type[Any], CP[UStruct]]] = {}
	__ufuncs: ClassVar[dict[tuple[type[UObject], Callable], CP[UFunction]]] = {}
	__uenums: ClassVar[dict[type[Enum], CP[UEnum]]] = {}

	@classmethod
	@Embed.python
	def utype_by(cls, origin: type[Any]) -> CP[UStruct]:
		"""構造体の型情報を生成

		Args:
			origin: 型(構造体)
		Returns:
			構造体の型情報
		Note:
			外部モジュールではStaticStructを使用し、このメソッドを直接コールしてはならない
		"""
		if origin not in cls.__utypes:
			utype = CP(UStruct(origin))
			Objects.set_private(utype, Objects.package_by_utype(utype), Name())
			cls.__utypes[origin] = utype

		return cls.__utypes[origin]

	@classmethod
	@Embed.python
	def uclass_by(cls, origin: type[UObject]) -> CP[UClass]:
		"""クラスの型情報を生成

		Args:
			origin: 型(クラス)
		Returns:
			クラスの型情報
		Note:
			外部モジュールではStaticClassを使用し、このメソッドを直接コールしてはならない
		"""
		if origin not in cls.__utypes:
			uclass = CP(UClass(origin))
			Objects.set_private(uclass, Objects.package_by_utype(uclass), Name())
			cls.__utypes[origin] = uclass

		return cls.__utypes[origin].down(UClass)

	@classmethod
	@Embed.python
	def ufunc_by(cls, origin: type[UObject], method: Callable) -> CP[UFunction]:
		"""関数の型情報を生成

		Args:
			origin: 型(クラス)
			method: 関数オブジェクト
		Returns:
			関数の型情報
		Note:
			外部モジュールではFindFunctionByNameを使用し、このメソッドを直接コールしてはならない
		"""
		if (origin, method) not in cls.__ufuncs:
			ufunc = CP(UFunction(origin, method))
			Objects.set_private(ufunc, Objects.package_by_utype(ufunc), Name())
			cls.__ufuncs[(origin, method)] = ufunc

		return cls.__ufuncs[(origin, method)]

	@classmethod
	@Embed.python
	def uenum_by(cls, enum_origin: type[Enum]) -> CP[UEnum]:
		"""Enumの型情報を生成

		Args:
			enum_origin: 型(Enum)
		Returns:
			Enumの型情報
		Note:
			外部モジュールではStaticEnumを使用し、このメソッドを直接コールしてはならない
		"""
		if enum_origin not in cls.__uenums:
			uenum = CP(UEnum(enum_origin))
			cls.__uenums[enum_origin] = uenum

		return cls.__uenums[enum_origin]


def CreatePackage(package_path: bytes) -> CP[Package]:
	"""パッケージを生成

	Args:
		package_path: パッケージのパス
	Note:
		@see Public/UObject/UObjectGlobals.h
	"""
	return NewObject(Package, Objects.transient_package(), Package.StaticClass(), Name(package_path.decode()))


def GetTransientPackage() -> CP[Package]:
	"""一時オブジェクトを管理するOuterの代替オブジェクトを取得

	Returns:
		インスタンス
	Note:
		```
		@see Public/UObject/UObjectGlobals.h
		* 主にNewObjectのouterに使用
		```
	"""
	return Objects.transient_package()


def NewObject(returned_type: type[T_Obj], outer: CP[UObject] | None = None, uclass: CP[UClass] | None = None, name: Name | str = '', flags: ObjectFlags = ObjectFlags_.RF_NoFlags, **kwargs: Any) -> CP[T_Obj]:
	"""UObjectの派生クラスをインスタンス化

	Args:
		returned_type: 返却型。この引数だけ指定した場合は生成するクラスの型
		outer: 生成したインスタンスを管理するオブジェクト (default = None)
		uclass: 生成する派生クラスの型情報 (default = None)
		name: 名前 ※strはリテラルのみ (default = '')
		flags: オブジェクトフラグ (default = RF_NoFlags)
		**kwargs (Any): テスト用の拡張引数 @test
	Returns:
		生成したインスタンス
	Raises:
		IllegalSchema: UCLASSの設定不備
		NotAllowed: Abstractのクラスを指定
		InvalidArguments: outerがNone
	Note:
		```
		@see Public/UObject/UObjectGlobals.h
		### outerに関して
		* 実際は引数にNoneを渡してはならず、空にする場合は引数自体を省略 ※Pythonの仕様上、Nullableにせざるを得ない
		* 引数を省略した場合のみGetTransientPackageで補完される点に注意
		```
	Examples:
		```python
		# 一時オブジェクトの作成 ※outer指定無し
		instance = NewObject(A)

		# 通常の作成方法 ※作成するクラスが静的である場合
		instance = NewObject(A, CP(self))

		# 派生クラスの型情報を指定して作成 ※作成するクラスが動的である場合(ファクトリーなど)
		instance = NewObject(UObject, CP(self), uclass)
		```
	"""
	origin: type[UObject] = uclass.on.origin if uclass is not None else returned_type
	class_annos = getattr(origin, EmbedKeys.Class.value, None)
	if class_annos is None:
		raise Errors.IllegalSchema(origin)
	elif Abstract in class_annos:
		raise Errors.NotAllowed(origin)
	elif not ((outer is None and uclass is None) or (outer is not None)):
		raise Errors.InvalidArguments()

	_outer: CP[UObject] = outer if outer else GetTransientPackage()
	return Objects.instance().new_object(origin, _outer, name, **kwargs).down(returned_type)


def StaticEnum(origin: type[Enum]) -> CP[UEnum]:
	"""Enumの型情報を取得

	Args:
		origin: Enumのクラス
	Returns:
		Enumの型情報
	Raises:
		IllegalSchema: UENUMの設定不備
	"""
	if not hasattr(origin, EmbedKeys.Enum.value):
		raise Errors.IllegalSchema(origin)

	return Classes.uenum_by(origin)


@Embed.python
def is_a(obj: CP[UObject], expected: type[T_Obj]) -> TypeIs[CP[T_Obj]]:
	"""オブジェクトが指定の型と同じか派生クラスか判定

	Args:
		obj: インスタンス ※型情報は不可 @see UE5.CoreUObject.UObject.Object.IsA
		expected: 期待の型
	Returns:
		True = 関連
	Raises:
		InvalidArguments: 型情報を指定
	"""
	if isinstance(obj.raw, UStruct):
		raise Errors.InvalidArguments(obj.raw)

	return isinstance(obj.raw, expected)


# def IsValid(obj: CP[T_Obj] | None) -> TypeIs[CP[T_Obj]]: """Note: checkを伴うため、実質的にIsValidCheckedと等価。無効判定が必要な場合はWeakObjectPtrを推奨"""


def IsValidChecked(obj: CP[T_Obj] | None) -> TypeIs[CP[T_Obj]]:
	"""オブジェクトが有効(未GC)か判定。checkを同時に実施

	Args:
		obj: オブジェクト
	Returns:
		True = 有効
	Note:
		```
		* Python: Nullチェックのみを行う
		* C++: リリースビルド以外は即クラッシュ
		```
	"""
	return obj is not None


class UObjectTrait:
	"""UObjectトレイト

	Note:
		```
		* XXX UObjectの非標準機能を扱うラッパークラス
		* XXX 本来存在しないクラスである点に注意
		```
	"""

	__obj: CP[UObject]

	def __init__(self, obj: CP[UObject]) -> None:
		"""インスタンスを生成

		Args:
			obj: オブジェクト
		"""
		self.__obj = obj

	# deprecated パッケージを取得する目的であればGetPackageを推奨
	# def GetOutermost(self) -> CP[UObject]:

	def GetPackage(self) -> CP[Package]:
		"""Returns: パッケージ XXX 詳細不明 Note: 本来はUObjectのメソッド @see UObjectBaseUtility.h"""
		outer = self.__obj.on.GetTypedOuter(Package)
		if not outer:
			raise Errors.Never(self.__obj)

		return outer

	def PostEditChange(self) -> None:
		"""編集終了イベントを発火 XXX 詳細不明 Note: 本来はUObjectのメソッド"""
		...

	def MarkPackageDirty(self) -> None:
		"""編集状態をマーク XXX 詳細不明 Note: 本来はUObjectのメソッド @see UObjectBaseUtility.h"""
		...


def to_obj_trait(obj: CP[UObject]) -> CP[UObjectTrait]:
	"""UObjectトレイトに変換

	Args:
		obj: オブジェクト
	Returns:
		UObjectトレイト
	Note:
		```
		* XXX 戻り値を変数に展開するのはNG
		* XXX @see template/func_call/default.j2
		```
	"""
	return CP(UObjectTrait(obj))
