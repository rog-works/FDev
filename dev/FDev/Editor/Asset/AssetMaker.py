from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.AssetRegistry.AssetRegistry.AssetRegistryModule import AssetRegistryModule
from UE5.CoreUObject.UObject.Object import CreatePackage, ObjectFlags_, Package, UObject, to_obj_trait
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UFUNCTION, Abstract, BlueprintCallable, BlueprintType
from UE5.CoreUObject.UObject.SavePackage import SavePackageArgs

from compatible.error import Errors
from FDev.Main.Const.ProjectConst import Aliases
from FDev.Main.Core.Asset.AssetPaths import AssetPaths
from FDev.Main.Core.Asset.Assets import Assets
from FDev.Main.Core.Lang.Convertion import safe_addr


@Embed.alias(Aliases.UObject.value, prefix=True)
@UCLASS(Abstract, BlueprintType)
class AssetMaker(UObject):
	"""アセット生成モジュール(基底)"""

	__assets: CP[Assets] | None

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.__assets = None

	def injection(self, assets: CP[Assets]) -> None:
		"""依存を注入"""
		self.__assets = assets

	@property
	def assets(self) -> CP[Assets]:
		"""Returns: アセットマネージャー"""
		return safe_addr(self.__assets)

	@Embed.allow_override
	def to_asset_path(self, src: str) -> str:
		"""アセットパスに変換

		Args:
			src: ソースパス
		Returns:
			アセットパス
		"""
		return src

	@Embed.allow_override
	def all_srcs(self) -> list[str]:
		"""Returns: 全アセットのソースパスリスト"""
		return []

	@UFUNCTION(BlueprintCallable)
	def create_in_editor(self, src: str, force: bool = False) -> bool:
		"""アセットを生成

		Args:
			src: ソースパス
			force: True = 強制実行 (default = False)
		Returns:
			True = 生成・更新
		Raises:
			Fatal: アセットの生成に失敗
		"""
		return self.create(src, force)

	@UFUNCTION(BlueprintCallable)
	def create_all_in_editor(self, force: bool = False) -> list[str]:
		"""アセットを一括生成

		Args:
			force: True = 強制実行 (default = False)
		Returns:
			生成・更新対象リスト
		Raises:
			Fatal: アセットの生成に失敗
		"""
		return self.create_all(force)

	def create_all(self, force: bool = False) -> list[str]:
		"""アセットを一括生成

		Args:
			force: True = 強制実行 (default = False)
		Returns:
			生成・更新対象リスト
		Raises:
			Fatal: アセットの生成に失敗
		"""
		updates: list[str] = []
		for src in self.all_srcs():
			if self.create(src, force):
				updates.append(src)

		return updates

	def create(self, src: str, force: bool = False) -> bool:
		"""アセットを生成

		Args:
			src: ソースパス
			force: True = 強制実行 (default = False)
		Returns:
			True = 生成・更新
		Raises:
			Fatal: アセットの生成に失敗
		"""
		asset_path = self.to_asset_path(src)
		asset = self.find_asset(asset_path)
		if not force and asset and self.skip_update(asset):
			return False
		elif asset is None:
			self.run_new(asset_path)
			return True
		else:
			self.run_update(asset)
			return True

	def find_asset(self, asset_path: str) -> CP[UObject] | None:
		"""アセットを検索

		Args:
			asset_path: アセットパス
		Returns:
			アセット | None
		"""
		if not self.assets.on.exists(asset_path):
			return None

		return self.resolve_asset(asset_path)

	@Embed.allow_override
	def resolve_asset(self, asset_path: str) -> CP[UObject]:
		"""アセットを解決

		Args:
			asset_path: アセットパス
		Returns:
			アセット
		"""
		raise Errors.MustBeImplemented

	@Embed.allow_override
	def skip_update(self, asset: CP[UObject]) -> bool:
		"""アセットの更新をスキップするか判定

		Args:
			asset: アセット
		Returns:
			True = スキップ
		"""
		return False

	def run_new(self, asset_path: str) -> None:
		"""実行処理(生成)

		Args:
			asset_path: アセットパス
		"""
		asset = self.new_asset(asset_path)
		self.build_asset(asset)
		self.save_asset(asset)

	def run_update(self, asset: CP[UObject]) -> None:
		"""実行処理(更新)

		Args:
			asset: アセット
		"""
		self.build_asset(asset)
		self.save_asset(asset)

	def new_asset(self, asset_path: str) -> CP[UObject]:
		"""アセットを生成

		Args:
			asset_path: アセットパス
		Returns:
			アセット
		"""
		package = CreatePackage(AssetPaths.to_ue_save_package_path(asset_path).encode())
		package.on.FullyLoad()
		return self.new_asset_impl(package, asset_path)

	@Embed.allow_override
	def new_asset_impl(self, package: CP[Package], asset_path: str) -> CP[UObject]:
		"""アセットを生成(実装)

		Args:
			package: パッケージ
			asset_path: アセットパス
		Returns:
			アセット
		"""
		raise Errors.MustBeImplemented

	def build_asset(self, asset: CP[UObject]) -> None:
		"""アセットをビルド

		Args:
			asset: アセット
		"""
		self.build_asset_impl(asset)
		to_obj_trait(asset).on.PostEditChange()
		AssetRegistryModule.AssetCreated(asset)
		to_obj_trait(asset).on.MarkPackageDirty()

	@Embed.allow_override
	def build_asset_impl(self, asset: CP[UObject]) -> None:
		"""アセットをビルド(実装)

		Args:
			asset: アセット
		"""
		raise Errors.MustBeImplemented

	def save_asset(self, asset: CP[UObject]) -> None:
		"""アセットをストレージに保存

		Args:
			asset: アセット
		Raises:
			Fatal: アセットの生成に失敗
		"""
		package = to_obj_trait(asset).on.GetPackage()
		filepath = AssetPaths.to_ue_save_filepath(package.on.GetFName().ToString())
		save_args = SavePackageArgs()
		save_args.TopLevelFlags = ObjectFlags_.RF_Public | ObjectFlags_.RF_Standalone
		if not package.on.SavePackage(package, asset, filepath.encode(), save_args):
			raise Errors.Fatal(AssetMaker.save_asset, asset.on.GetPathName(), filepath)

	def fetch_hash(self, asset: CP[UObject]) -> str:
		"""アセットのメタデータからハッシュ値を取得

		Args:
			asset: アセット
		Returns:
			ハッシュ値
		"""
		return to_obj_trait(asset).on.GetPackage().on.GetMetaData().on.GetValue(asset, str('hash').encode())

	def apply_hash(self, asset: CP[UObject], hash: str) -> None:
		"""アセットのメタデータにハッシュ値を設定

		Args:
			asset: アセット
			hash: ハッシュ値
		"""
		to_obj_trait(asset).on.GetPackage().on.GetMetaData().on.SetValue(asset, str('hash').encode(), hash.encode())
