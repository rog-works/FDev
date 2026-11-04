from typing import Annotated, override

from tranp.app.compatible.cpp.cvar import CP, CSP
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.Paths import PackageName
from UE5.CoreUObject.UObject.Object import SoftObjectPath, SoftObjectPtr, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UPROPERTY

from App.Main.Const.ProjectConst import ClassPrefixs
from App.Main.Core.Asset.AssetPaths import AssetPaths
from App.Main.Core.Asset.AssetStorage import IAssetStorage, IMasterStorage
from App.Main.Core.Lang.IO.File import Files
from App.Main.Core.Lang.Json.Json import Json
from App.Main.Core.Lang.Json.JsonEntry import JsonEntry
from compatible.error import Errors
from const.const_asset import AssetFormats


@Embed.alias(ClassPrefixs.UObject.value, prefix=True)
@UCLASS()
class AssetStorageImpl(IAssetStorage):
	"""アセットストレージ"""

	__caches: Annotated[dict[str, CP[UObject]], UPROPERTY()]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.__caches = {}

	@override
	def exists(self, path: str) -> bool:
		"""アセットが存在するか判定

		Args:
			path: アセットパス
		Returns:
			True = 存在
		"""
		return PackageName.DoesPackageExist(AssetPaths.to_ue_package_path(path))

	@override
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
		if path not in self.__caches or not cache:
			self.__caches[path] = self.load_asset(path)

		return self.__caches[path]

	def load_asset(self, path: str) -> CP[UObject]:
		"""アセットをロード

		Args:
			path: アセットパス
		Returns:
			アセット
		Raises:
			NotFound: 存在しないアセットを指定
		"""
		ue_asset_path = AssetPaths.to_ue_path(path)
		resolver = SoftObjectPtr[UObject](SoftObjectPath(ue_asset_path))
		asset = resolver.LoadSynchronous()
		if not asset:
			raise Errors.NotFound(AssetStorageImpl.load_asset, ue_asset_path)

		return asset


@Embed.alias(ClassPrefixs.UObject.value, prefix=True)
@UCLASS()
class MasterStorageImpl(IMasterStorage):
	"""マスターストレージ"""

	__caches: dict[str, CSP[JsonEntry]]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.__caches = {}

	@override
	def exists(self, path: str) -> bool:
		"""アセットが存在するか判定

		Args:
			path: アセットパス
		Returns:
			True = 存在
		"""
		if path in self.__caches:
			return True

		if self.for_origin(path):
			return Files.exiets(AssetPaths.to_master_filepath(path))

		origin_path, internal_path = self.break_internal_path(path)
		origin = self.load(origin_path)
		return origin.has_key(internal_path)

	@override
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
		if path not in self.__caches or not cache:
			if self.for_origin(path):
				self.__caches[path] = self.load_origin(path)
			else:
				self.__caches[path] = self.load_internal(path)

		return Json(self.__caches[path].addr)

	def load_origin(self, path: str) -> CSP[JsonEntry]:
		"""マスターをファイルからロード

		Args:
			path: アセットパス
		Returns:
			マスター
		Raises:
			NotFound: 存在しないアセットを指定
		"""
		filepath = AssetPaths.to_master_filepath(path)
		return Json.parse(Files.load(filepath))

	def load_internal(self, path: str) -> CSP[JsonEntry]:
		"""マスターの内部データをロード

		Args:
			path: アセットパス
		Returns:
			マスター
		Raises:
			NotFound: 存在しないアセットを指定
		"""
		origin_path, internal_path = self.break_internal_path(path)
		origin = self.load(origin_path)
		return Json.parse(origin[internal_path].as_string)

	def for_origin(self, path: str) -> bool:
		"""対象がオリジンか判定

		Args:
			path: アセットパス
		Returns:
			True = オリジン
		"""
		return path.count(AssetFormats.InternalDelimiter.value) == 0

	def break_internal_path(self, path: str) -> tuple[str, str]:
		"""アセットパスからオリジンのパスと内部データのパスに分解

		Args:
			path: アセットパス
		Returns:
			(アセットパス, アセットソースパス)
		"""
		origin_end = path.find(AssetFormats.InternalDelimiter.value)
		return path[:origin_end], path[origin_end + 1:]
