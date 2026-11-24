# @see Engine/Source/Editor/UnrealEd/Classes/MaterialGraph/MaterialGraph.h

from typing import Annotated

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UPROPERTY
from UE5.Engine.Materials.Material import Material


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialGraph(UObject):
	"""マテリアルグラフ"""

	Material_: Annotated[CP[Material] | None, UPROPERTY(), Embed.alias('Material')]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Material_ = None

	def RebuildGraph(self) -> None:
		"""グラフノードを再構築"""
		...
