from enum import Enum

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import NewObject, UClass, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UFUNCTION, BlueprintCallable, DefaultToSelf

from App.Editor.Asset.AssetMaker import AssetMaker
from App.Editor.Asset.MFAssetMaker import MFAssetMaker
from App.Main.Core.Asset.Assets import Assets
from App.Main.Core.Asset.AssetStorageImpl import AssetStorageImpl, MasterStorageImpl


@Embed.python
class MakerTags(Enum):
	"""アセット生成モジュールタグ"""
	MFs = 'mfs'


@Embed.alias('U', prefix=True)
@UCLASS()
class AssetMakerFactory(UObject):
	"""アセット生成モジュールファクトリー"""

	@classmethod
	def create(cls, tag: str, outer: CP[UObject]) -> CP[AssetMaker]:
		"""アセット生成モジュールを生成

		Args:
			tag: モジュールタグ
			outer: 管理オブジェクト
		Returns:
			アセット生成モジュール
		"""
		return cls.from_class(cls.to_uclass(tag), outer)

	@classmethod
	@UFUNCTION(BlueprintCallable, meta=[DefaultToSelf('outer')])
	def from_class(cls, uclass: CP[UClass], outer: CP[UObject]) -> CP[AssetMaker]:
		"""アセット生成モジュールを生成

		Args:
			uclass: クラスの型情報
			outer: 管理オブジェクト
		Returns:
			アセット生成モジュール
		"""
		instance = NewObject(AssetMaker, outer, uclass)
		instance.on.injection(cls.new_assets(outer))
		return instance

	@classmethod
	def to_uclass(cls, tag: str) -> CP[UClass]:
		"""モジュールタグからクラスの型情報を解決

		Args:
			tag: モジュールタグ
		Returns:
			クラスの型情報
		"""
		to_uclasses = Embed.static(cls.to_uclass).decl(lambda: {
			MakerTags.MFs.value: MFAssetMaker.StaticClass(),
		})
		return to_uclasses[tag]

	@classmethod
	def new_assets(cls, outer: CP[UObject]) -> CP[Assets]:
		"""Args: outer: 管理オブジェクト Returns: アセットマネージャー"""
		assets = NewObject(Assets, outer)
		assets.on.injection(NewObject(AssetStorageImpl, outer), NewObject(MasterStorageImpl, outer))
		return assets
