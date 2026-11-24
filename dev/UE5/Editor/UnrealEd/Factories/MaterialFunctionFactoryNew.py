# @see Engine/Source/Editor/UnrealEd/Classes/Factories/MaterialFunctionFactoryNew.h

from tranp.app.compatible.python.embed import Embed
from UE5.AssetTools.AssetToolsModule import Factory
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFunctionFactoryNew(Factory):
	"""アセットファクトリー(マテリアル関数)"""
	...
