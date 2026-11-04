from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, Abstract

from compatible.error import Errors
from FDev.Main.Const.ProjectConst import ClassPrefixs
from FDev.Main.Core.Lang.Json.Json import Json


@Embed.alias(ClassPrefixs.UObject.value, prefix=True)
@UCLASS(Abstract)
class IAssetStorage(UObject):
	"""アセットストレージ(インターフェイス)"""

	@Embed.allow_override
	def exists(self, path: str) -> bool:
		"""アセットが存在するか判定

		Args:
			path: アセットパス
		Returns:
			True = 存在
		"""
		raise Errors.MustBeImplemented

	@Embed.allow_override
	def load(self, path: str, cache: bool = True) -> CP[UObject]:
		"""アセットをロード

		Args:
			path: アセットパス
			cache: True = キャッシュ使用 (default = True)
		Returns:
			アセット
		Raises:
			NotFound: 存在しないアセットを指定
		"""
		raise Errors.MustBeImplemented


@Embed.alias(ClassPrefixs.UObject.value, prefix=True)
@UCLASS(Abstract)
class IMasterStorage(UObject):
	"""マスターストレージ(インターフェイス)"""

	@Embed.allow_override
	def exists(self, path: str) -> bool:
		"""アセットが存在するか判定

		Args:
			path: アセットパス
		Returns:
			True = 存在
		"""
		raise Errors.MustBeImplemented

	@Embed.allow_override
	def load(self, path: str, cache: bool = True) -> Json:
		"""アセットをロード

		Args:
			path: アセットパス
			cache: True = キャッシュ使用 (default = True)
		Returns:
			アセット
		Raises:
			NotFound: 存在しないアセットを指定
		"""
		raise Errors.MustBeImplemented
