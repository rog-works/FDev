from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFunctionInterface(UObject):
	"""マテリアル関数(基底)"""
	...
