# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialParameterCollection.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.Guid import Guid
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialParameterCollection(UObject):
	"""マテリアルパラメーターコレクション"""

	def GetParameterId(self, name: Name) -> Guid:
		"""名前に対応するGuidを返却

		Returns:
			Guid
		Note:
			重要ではないため適当な値を返す
		"""
		return Guid.NewGuid()
