from typing import Annotated, override

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.AssetTools.AssetToolsModule import AssetToolsModule
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.CoreUObject.UObject.Object import NewObject, Package, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, BlueprintType
from UE5.Editor.UnrealEd.Factories.MaterialInstanceConstantFactoryNew import MaterialInstanceConstantFactoryNew
from UE5.Engine.Materials.Material import Material, MaterialInterface
from UE5.Engine.Materials.MaterialInstanceConstant import MaterialInstanceConstant

from App.Editor.Asset.AssetMaker import AssetMaker
from App.Editor.Material.MIBuilder import MIBuildCommandRunner, MIBuilder
from App.Main.Core.Asset.AssetPaths import AssetPaths
from App.Main.Core.Lang.Json.Json import Json
from const.const_asset import AssetDomains, AssetNames


@Embed.alias('U', prefix=True)
@UCLASS(BlueprintType)
class MIAssetMaker(AssetMaker):
	"""アセット生成モジュール(マテリアルインスタンス)"""

	__commands: dict[str, tuple[str, Json]]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.__commands = {}

	@property
	def commands(self) -> Annotated[dict[str, tuple[str, Json]], Embed.immutable]:
		"""Returns: コマンド一覧"""
		if len(self.__commands) == 0:
			data = self.assets.on.master_of(AssetPaths.to_path(AssetDomains.MasterApp.value, AssetNames.MIs.value))
			# FIXME 名前とパスが混在して微妙。GetNameの結果に依存するべきではない
			self.__commands = {AssetPaths.pick_name(src): (src, data[src]) for src in data.keys}

		return self.__commands

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
		return self.assets.on.asset_of(MaterialInstanceConstant, asset_path)

	@override
	def skip_update(self, asset: CP[UObject]) -> bool:
		"""アセットの更新をスキップするか判定

		Args:
			asset: アセット
		Returns:
			True = スキップ
		Note:
			アセット内に保存したメタデータのハッシュ値を基に更新可否を判定
		"""
		return self.fetch_hash(asset) == self.commands[asset.on.GetName()][1]['hash'].as_string

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
		via_src = MIBuildCommandRunner.via_src(self.commands[name][1])
		via = self.assets.on.asset_of(Material, AssetPaths.to_path(AssetDomains.Material.value, via_src))
		factory = NewObject(MaterialInstanceConstantFactoryNew, package)
		factory.on.InitialParent = ObjectPtr[MaterialInterface](via)
		return AssetToolsModule.GetModule().on.Get().on.CreateAsset(name, AssetPaths.to_ue_save_dir(asset_path), MaterialInstanceConstant.StaticClass(), factory)

	@override
	def build_asset_impl(self, asset: CP[UObject]) -> None:
		"""アセットをビルド(実装)

		Args:
			asset: アセット
		"""
		mi = asset.down(MaterialInstanceConstant)
		builder = MIBuilder(self.assets, mi)
		MIBuildCommandRunner.run(CP(builder), self.commands[mi.on.GetName()][1])
		self.apply_hash(asset, self.commands[mi.on.GetName()][1]['hash'].as_string)
