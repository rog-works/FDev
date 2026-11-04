# @see Engine/Source/Runtime/AssetRegistry/Public/AssetRegistry/AssetRegistryModule.h

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject


@Embed.alias('F', prefix=True)
class AssetRegistryModule:
	"""アセット登録モジュール(フロントエンド)"""

	@classmethod
	def AssetCreated(cls, asset: CP[UObject]) -> None:
		"""アセットを生成

		Args:
			asset: インスタンス
		"""
		...
