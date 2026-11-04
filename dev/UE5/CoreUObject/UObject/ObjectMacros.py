# @see Engine/Source/Runtime/CoreUObject/Public/UObject/ObjectMacros.h

from collections.abc import Callable
from enum import Enum
from typing import Literal

# region アノテーション

class UEAnno: """アノテーション(基底)"""
class UEAnnoClass(UEAnno): """アノテーション(クラス)"""
class UEAnnoFunction(UEAnno): """アノテーション(関数)"""
class UEAnnoProperty(UEAnno): """アノテーション(プロパティー)"""

# endregion
# region アノテーション/クラス

class Abstract(UEAnnoClass): """抽象クラス。インスタンス化を防止"""
class BlueprintType(UEAnnoClass): """BPで変数の型として使用可能"""
class Blueprintable(UEAnnoClass): """BPで基底クラスとして使用可能"""
# class NotBlueprintType(UEAnnoClass): """BPの変数として使用不可 Note: @deprecated XXX 基底クラスのアノテーション解除用であり、単体で使用しても効果はない"""
# class NotBlueprintable(UEAnnoClass): """BPの基底クラスとして使用不可 Note: @deprecated XXX 基底クラスのアノテーション解除用であり、単体で使用しても効果はない"""

# endregion
# region アノテーション/関数

class BlueprintCallable(UEAnnoFunction): """BPで使用可能"""
class BlueprintPure(UEAnnoFunction): """副作用のない関数。ノードが簡略表示に変化"""

# endregion
# region アノテーション/関数/通信

class BlueprintAuthorityOnly(UEAnnoFunction): """BPで使用した場合、サーバー側でのみ実行。C++から呼び出された場合は保証しない"""
class Client(UEAnnoFunction): """クライアント側で実行する関数。Serverと排他関係"""
class Server(UEAnnoFunction): """サーバー側で実行する関数。Clientと排他関係"""
class Reliable(UEAnnoFunction): """サーバー実行保証。順序保証。Unreliableに比べ遅い。正確性重視。ステート変更などのトランザクション処理、順序が重要な用途。Unreliableと排他関係"""
class Unreliable(UEAnnoFunction): """サーバー実行保証なし。順序保証なし。Reliableに比べ早い。高速性重視。衝突判定などの物理演算系、最悪順序を無視しても良い用途。Reliableと排他関係"""
class WithValidation(UEAnnoFunction): """サーバーで実行される前にバリデーションを実施。バリデーション用の関数を別途実装する必要あり"""

# endregion
# region アノテーション/プロパティー

class BlueprintReadOnly(UEAnnoProperty): """BPで参照のみ許可"""
class BlueprintReadWrite(UEAnnoProperty): """BPで参照/変更を許可"""
class Replicated(UEAnnoProperty): """レプリケーション対象"""
class SaveGame(UEAnnoProperty): """SaveGameへの保存対象"""
class EditAnywhere(UEAnnoProperty): """プロパティー詳細で編集を許可"""
class VisibleAnywhere(UEAnnoProperty): """プロパティー詳細に情報を開示"""

# endregion
# region アノテーション/プロパティー/デリゲート

class BlueprintAssignable(UEAnnoProperty): """ハンドラーのバインドを許可"""

# endregion
# region メタデータ

class UEMeta: """メタデータ(基底)"""
class UEMetaClass(UEMeta): """メタデータ(クラス)"""
class UEMetaFunction(UEMeta): """メタデータ(関数)"""
class UEMetaProperty(UEMeta): """メタデータ(プロパティー)"""

# endregion
# region メタデータ/クラス

class BlueprintSpawnableComponent(UEMetaClass): """コンポーネントの候補に表示"""

# endregion
# region メタデータ/関数

class UEMetaFunctionOfString(UEMetaFunction):
	"""メタデータ(関数/String系)"""

	def __init__(self, string: str) -> None: ...

class DefaultToSelf(UEMetaFunctionOfString): """デフォルト値をSelfで自動補完"""
class DisplayName(UEMetaFunctionOfString): """エディター上の表示名を設定"""
class WorldContext(UEMetaFunctionOfString):
	"""BPでWorldContextの引数を省略"""

	def __init__(self, string: Literal['WorldContextObject']) -> None: ...

# endregion
# region 埋め込み関数

class EmbedKeys(Enum):
	"""埋め込みキー"""
	Enum = '__UENUM__'
	Struct = '__USTRUCT__'
	Class = '__UCLASS__'
	Function = '__UFUNCTION__'


def UPROPERTY(*args: type[UEAnnoProperty], **meta: list[UEMeta]) -> list[type[UEAnnoProperty]]:
	"""プロパティのアノテーションを埋め込む

	Args:
		*args (type[UEAnnoProperty]): アノテーション
		**meta (list[UEMeta]): メタデータ
	Returns:
		アノテーション
	Note:
		アノテーションのみ評価し、メタデータは評価しない点に注意
	"""
	return list(args)


def UENUM(*args: type[UEAnnoClass], **meta: list[UEMeta]) -> Callable:
	"""列挙子のアノテーションを埋め込むデコレーター

	Args:
		*args (type[UEAnnoClass]): アノテーション
		**meta (list[UEMeta]): メタデータ
	Returns:
		デコレーター
	Note:
		@see UCLASS#Note
	"""
	def decorator[T](wrapped: T) -> T:
		setattr(wrapped, EmbedKeys.Enum.value, list(args))
		return wrapped

	return decorator


def USTRUCT(*args: type[UEAnnoClass], **meta: list[UEMeta]) -> Callable:
	"""構造体のアノテーションを埋め込むデコレーター

	Args:
		*args (type[UEAnnoClass]): アノテーション
		**meta (list[UEMeta]): メタデータ
	Returns:
		デコレーター
	Note:
		@see UCLASS#Note
	"""
	def decorator[T](wrapped: T) -> T:
		setattr(wrapped, EmbedKeys.Struct.value, list(args))
		return wrapped

	return decorator


def UCLASS(*args: type[UEAnnoClass], **meta: list[UEMeta]) -> Callable:
	"""クラスのアノテーションを埋め込むデコレーター

	Args:
		*args (type[UEAnnoClass]): アノテーション
		**meta (list[UEMeta]): メタデータ
	Returns:
		デコレーター
	Note:
		```
		* アノテーションのみ評価し、メタデータは評価しない点に注意
		* C++では継承によって引き継がれるが、Pythonでは上書きされる点に注意
		```
	"""
	def decorator[T](wrapped: T) -> T:
		setattr(wrapped, EmbedKeys.Class.value, list(args))
		return wrapped

	return decorator


def UFUNCTION(*args: type[UEAnnoFunction], **meta: list[UEMeta]) -> Callable:
	"""関数のアノテーションを埋め込むデコレーター

	Args:
		*args (type[UEAnno]): アノテーション
		**meta (list[UEMeta]): メタデータ
	Returns:
		デコレーター
	Note:
		```
		* @see UCLASS#Note
		* overrideした関数で再埋め込みは不可
		```
	"""
	def decorator[T](wrapped: T) -> T:
		setattr(wrapped, EmbedKeys.Function.value, list(args))
		return wrapped

	return decorator


# @deprecated
# def UINTERFACE(*args: type[UEAnnoClass], **meta: list[UEMeta]) -> Callable:
# 	"""インターフェイスのアノテーションを埋め込むデコレーター

# 	Args:
# 		*args (type[UEAnnoClass]): アノテーション
# 		**meta (list[UEMeta]): メタデータ
# 	Returns:
# 		デコレーター
# 	Note:
# 		@deprecated インターフェイスは使わない想定
# 	"""
# 	def decorator(wrapped: T_Type) -> T_Type:
# 		return wrapped

# 	return decorator


# 自動的に挿入されるため、以下のマクロは不要
# def GENERATED_BODY() -> None:
# 	"""UObjectの既定実装を代替するマクロ
# 
# 	Note:
# 		以下のマクロは旧仕様のマクロのため、共通でGENERATED_BODYを使うこと
# 		* GENERATED_UCLASS_BODY
# 		* GENERATED_USTRUCT_BODY
# 	"""
# 	pass

# endregion
