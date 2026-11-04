from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UFUNCTION

from const.const_asset import AssetDomains
from FDev.Main.Const.ProjectConst import ClassPrefixs
from FDev.Main.Core.Asset.AssetStorage import IAssetStorage, IMasterStorage
from FDev.Main.Core.Lang.Convertion import safe_addr
from FDev.Main.Core.Lang.Json.Json import Json


@Embed.alias(ClassPrefixs.UObject.value, prefix=True)
@UCLASS()
class Assets(UObject):
	"""アセットマネージャー"""

	__asset_storage: CP[IAssetStorage] | None
	__master_storage: CP[IMasterStorage] | None

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.__asset_storage = None
		self.__master_storage = None

	def injection(self, asset_storage: CP[IAssetStorage], master_storage: CP[IMasterStorage]) -> None:
		"""依存を注入"""
		self.__asset_storage = asset_storage
		self.__master_storage = master_storage

	@property
	def asset_storage(self) -> CP[IAssetStorage]:
		"""Returns: アセットストレージ"""
		return safe_addr(self.__asset_storage)

	@property
	def master_storage(self) -> CP[IMasterStorage]:
		"""Returns: マスターストレージ"""
		return safe_addr(self.__master_storage)

	@UFUNCTION()
	def exists(self, path: str) -> bool:
		"""アセットが存在するか判定

		Args:
			path: アセットパス
		Returns:
			True = 存在
		"""
		if path.startswith(AssetDomains.Master.value):
			return self.master_storage.on.exists(path)
		else:
			return self.asset_storage.on.exists(path)

	def asset_of[T_Obj: UObject](self, asset_type: type[T_Obj], path: str, cache: bool = True) -> CP[T_Obj]:
		"""アセットを解決

		Args:
			asset_type: アセットの型
			path: アセットパス
			cache: True = キャッシュ使用 (default = True)
		Returns:
			アセット
		Raises:
			NotFound: 存在しないアセットを指定
		"""
		return self.asset_storage.on.load(path, cache).as_a(asset_type)

	def master_of(self, path: str, cache: bool = True) -> Json:
		"""アセット(マスター)を解決

		Args:
			path: アセットパス
			cache: True = キャッシュ使用 (default = True)
		Returns:
			アセット
		Raises:
			NotFound: 存在しないアセットを指定
		"""
		return self.master_storage.on.load(path, cache)
