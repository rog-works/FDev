from typing import Annotated, override

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.AssetTools.AssetToolsModule import AssetToolsModule
from UE5.CoreUObject.UObject.Object import NewObject, Package, UObject, is_a
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, BlueprintType
from UE5.Editor.UnrealEd.Factories.MaterialFactoryNew import MaterialFactoryNew
from UE5.Editor.UnrealEd.Factories.MaterialFunctionFactoryNew import MaterialFunctionFactoryNew
from UE5.Engine.Materials.Material import Material
from UE5.Engine.Materials.MaterialFunction import MaterialFunction

from App.Editor.Asset.AssetMaker import AssetMaker
from App.Editor.Material.MFBuildCommand import MFBuildCommand, MFBuildCommandRunner
from App.Editor.Material.MFBuilder import MFBuilder
from App.Main.Core.Asset.AssetPaths import AssetPaths
from const.const_asset import AssetDomains, AssetNames


@Embed.alias('U', prefix=True)
@UCLASS(BlueprintType)
class MFAssetMaker(AssetMaker):
	"""アセット生成モジュール(マテリアル関数/マテリアル)"""

	__commands: dict[str, tuple[str, MFBuildCommand]]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.__commands = {}

	@property
	def commands(self) -> Annotated[dict[str, tuple[str, MFBuildCommand]], Embed.immutable]:
		"""Returns: コマンド一覧"""
		if len(self.__commands) == 0:
			data = self.assets.on.master_of(AssetPaths.to_path(AssetDomains.MasterApp.value, AssetNames.MFs.value))
			# FIXME 名前とパスが混在して微妙。GetNameの結果に依存するべきではない
			for src, command in MFBuildCommandRunner.parse(data).items():
				self.__commands[AssetPaths.pick_name(src)] = src, command

		return self.__commands

	def command_by(self, name: str) -> MFBuildCommand:
		"""Args: name: アセット名 Returns: コマンド"""
		return self.commands[name][1]

	@override
	def to_asset_path(self, src: str) -> str:
		"""アセットパスに変換

		Args:
			src: ソースパス
		Returns:
			アセットパス
		"""
		return AssetPaths.to_path(AssetDomains.Material.value, src)

	@override
	def all_srcs(self) -> list[str]:
		"""Returns: 全アセットのソースパスリスト"""
		return [entry[0] for entry in self.commands.values()]

	@override
	def resolve_asset(self, asset_path: str) -> CP[UObject]:
		"""アセットを解決

		Args:
			asset_path: アセットパス
		Returns:
			アセット
		"""
		if asset_path.startswith(AssetDomains.MaterialFunc.value):
			return self.assets.on.asset_of(MaterialFunction, asset_path)
		else:
			return self.assets.on.asset_of(Material, asset_path)

	@override
	def skip_update(self, asset: CP[UObject]) -> bool:
		"""アセットの更新をスキップするか判定

		Args:
			asset: アセット
		Returns:
			True = スキップ
		"""
		return self.fetch_hash(asset) == self.command_by(asset.on.GetName()).hash

	@override
	def new_asset_impl(self, package: CP[Package], asset_path: str) -> CP[UObject]:
		"""アセットを生成(実装)

		Args:
			package: パッケージ
			asset_path: アセットパス
		Returns:
			アセット
		"""
		name = AssetPaths.pick_name(asset_path)
		if asset_path.startswith(AssetDomains.MaterialFunc.value):
			factory = NewObject(MaterialFunctionFactoryNew, package)
			return AssetToolsModule.GetModule().on.Get().on.CreateAsset(name, AssetPaths.to_ue_save_dir(asset_path), MaterialFunction.StaticClass(), factory)
		else:
			factory = NewObject(MaterialFactoryNew, package)
			return AssetToolsModule.GetModule().on.Get().on.CreateAsset(name, AssetPaths.to_ue_save_dir(asset_path), Material.StaticClass(), factory)

	@override
	def build_asset_impl(self, asset: CP[UObject]) -> None:
		"""アセットをビルド(実装)

		Args:
			asset: アセット
		"""
		if is_a(asset, MaterialFunction):
			builder = MFBuilder.from_mf(self.assets, asset.down(MaterialFunction))
			MFBuildCommandRunner.build_mf(CP(builder), self.command_by(asset.on.GetName()))
		else:
			builder = MFBuilder.from_material(self.assets, asset.down(Material))
			MFBuildCommandRunner.build_material(CP(builder), self.command_by(asset.on.GetName()))

		self.apply_hash(asset, self.command_by(asset.on.GetName()).hash)
