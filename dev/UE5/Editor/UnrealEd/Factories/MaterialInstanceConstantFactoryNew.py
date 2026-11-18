# @see Engine/Source/Editor/UnrealEd/Classes/Factories/MaterialInstanceConstantFactoryNew.h

from typing import override

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.AssetTools.AssetToolsModule import Factory
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.CoreUObject.UObject.Object import NewObject, UClass, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.Material import MaterialInterface
from UE5.Engine.Materials.MaterialInstanceConstant import MaterialInstanceConstant


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialInstanceConstantFactoryNew(Factory):
	"""アセットファクトリー(マテリアルインスタンス)"""

	InitialParent: ObjectPtr[MaterialInterface]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.InitialParent = ObjectPtr[MaterialInterface]()

	@override
	@Embed.python
	def create(self, name: str, uclass: CP[UClass]) -> CP[UObject]:
		"""アセットを生成

		Args:
			name: アセット名
			uclass: アセットの型情報
		Returns:
			生成したアセットのインスタンス
		"""
		return NewObject(MaterialInstanceConstant, CP(self), uclass, name)
