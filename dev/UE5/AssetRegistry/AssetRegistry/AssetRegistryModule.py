# @see Engine/Source/Runtime/AssetRegistry/Public/AssetRegistry/AssetRegistryModule.h

from tranp.app.compatible.cpp.cvar import CP, CRef
from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.annotation import deprecated
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.Object import UObject


@deprecated
@Embed.struct
@Embed.alias('F', prefix=True)
class AssetIdentifier:
	"""アセット識別子

	Note:
		```
		* 書式: '/(Editor|Game)/{asset_path}' ※パッケージパス
		* 本来は入力次第で識別子の表現(=出力)に差が出るはずだが、ToStringの結果もパッケージパスになる模様 ※詳細不明
		@deprecated 未使用
		```
	"""

	PackageName: Name

	def __init__(self, package_name: Name) -> None:
		"""インスタンスを生成

		Args:
			package_name: パッケージ名
		"""
		self.PackageName = package_name


@deprecated
class IRegistryModule:
	"""アセット登録モジュール(基底) @deprecated 未使用"""

	def GetReferencers(self, via: AssetIdentifier, assets: CRef[list[AssetIdentifier]]) -> None:
		"""指定のアセットを参照しているアセットの識別子を取得

		Args:
			via: アセットの識別子
			assets: 参照アセットの識別子リスト ※出力
		"""
		...


@Embed.alias('F', prefix=True)
class AssetRegistryModule:
	"""アセット登録モジュール(フロントエンド)"""

	@classmethod
	@deprecated
	def GetRegistry(cls) -> CRef[IRegistryModule]:
		"""Returns: アセット登録モジュール @deprecated 未使用"""
		return CRef(IRegistryModule())

	@classmethod
	def AssetCreated(cls, asset: CP[UObject]) -> None:
		"""アセットを生成

		Args:
			asset: インスタンス
		"""
		...
