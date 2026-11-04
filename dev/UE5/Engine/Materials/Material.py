from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, Abstract, BlueprintType


@Embed.alias('U', prefix=True)
@UCLASS(Abstract)
class MaterialInterface(UObject):
	"""マテリアル(インターフェイス)"""
	...


@Embed.alias('U', prefix=True)
@UCLASS(BlueprintType)
class Material(MaterialInterface):
	"""マテリアル"""
	...
