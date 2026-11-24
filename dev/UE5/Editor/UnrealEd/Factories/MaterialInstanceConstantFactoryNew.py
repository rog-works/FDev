# @see Engine/Source/Editor/UnrealEd/Classes/Factories/MaterialInstanceConstantFactoryNew.h

from tranp.app.compatible.python.embed import Embed
from UE5.AssetTools.AssetToolsModule import Factory
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.Material import MaterialInterface


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialInstanceConstantFactoryNew(Factory):
	"""アセットファクトリー(マテリアルインスタンス)"""

	InitialParent: ObjectPtr[MaterialInterface]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.InitialParent = ObjectPtr[MaterialInterface]()
