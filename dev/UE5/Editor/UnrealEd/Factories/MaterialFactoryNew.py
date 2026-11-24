# @see Engine/Source/Editor/UnrealEd/Classes/Factories/MaterialFactoryNew.h

from tranp.app.compatible.python.embed import Embed
from UE5.AssetTools.AssetToolsModule import Factory
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFactoryNew(Factory):
	"""アセットファクトリー(マテリアル)"""
	...
