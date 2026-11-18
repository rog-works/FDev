# @see Engine/Source/Developer/AssetTools/Public/AssetToolsModule.h

from tranp.app.compatible.cpp.cvar import CP, CRef
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UClass, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS

from App.Main.Const.ProjectConst import PackageConst
from compatible.error import Errors


@Embed.alias('U', prefix=True)
@UCLASS()
class Factory(UObject):
	"""ファクトリー(基底) Note: @see Engine/Source/Editor/UnrealEd/Classes/Factories/Factory.h"""

	@Embed.python
	@Embed.allow_override
	def create(self, name: str, uclass: CP[UClass]) -> CP[UObject]:
		"""アセットを生成

		Args:
			name: アセット名
			uclass: アセットの型情報
		Returns:
			生成したアセットのインスタンス
		"""
		raise Errors.MustBeImplemented(name, uclass)


class IAssetTools:
	"""アセットツール(インターフェイス) Note: @see AssetTools/Public/IAssetTools.h"""

	def CreateAsset(self, name: str, asset_dir: str, uclass: CP[UClass], factory: CP[Factory]) -> CP[UObject]:
		"""アセットを生成

		Args:
			name: アセット名
			asset_dir: アセットの保存先ディレクトリー
			uclass: アセットの型情報
			factory: ファクトリー
		Returns:
			生成したアセットのインスタンス
		Raises:
			InvalidArguments: アセットディレクトリーがUE仕様と異なる
		"""
		if not asset_dir.startswith(PackageConst.Game):
			raise Errors.InvalidArguments(name, asset_dir, uclass)

		return factory.on.create(name, uclass)


@Embed.alias('F', prefix=True)
class AssetToolsModule:
	"""アセットツール(フロントエンド)"""

	@classmethod
	def GetModule(cls) -> 'CRef[AssetToolsModule]':
		"""Returns: シングルトンインスタンス"""
		return CRef(cls())

	def Get(self) -> 'CRef[IAssetTools]':
		"""Returns: アセットツール"""
		return CRef(IAssetTools())
