# @see Engine/Source/Runtime/Engine/Public/Materials/Material.h

from enum import Enum
from typing import Annotated

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import NewObject, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UENUM, UPROPERTY, USTRUCT, Abstract, BlueprintType
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpressionCollection


@Embed.alias('U', prefix=True)
@UCLASS(Abstract)
class MaterialInterface(UObject):
	"""マテリアル(インターフェイス)"""
	...


@Embed.alias('U', prefix=True)
@UCLASS(BlueprintType)
class Material(MaterialInterface):
	"""マテリアル"""

	__EditorOnlyData: 'CP[MaterialEditorOnlyData] | None'
	MaterialDomain_: Annotated['MaterialDomain', Embed.alias('MaterialDomain')]
	BlendMode_: Annotated['BlendMode', Embed.alias('BlendMode')]
	TwoSided: bool
	# グラフ
	EditorX: int
	EditorY: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.__EditorOnlyData = None
		self.MaterialDomain_ = MaterialDomain.MD_Surface
		self.BlendMode_ = BlendMode.BLEND_Opaque
		self.TwoSided = False
		self.EditorX = 0
		self.EditorY = 0

	def GetEditorOnlyData(self) -> 'CP[MaterialEditorOnlyData]':
		"""Returns: エディター専用データ"""
		if not self.__EditorOnlyData:
			self.__EditorOnlyData = NewObject(MaterialEditorOnlyData, CP(self))

		return self.__EditorOnlyData

	def SetShadingModel(self, shading: 'MaterialShadingModel') -> None:
		"""Args: shading: シェーディングモデル"""
		...


@Embed.alias('E', prefix=True)
@UENUM()
class MaterialDomain(Enum):
	"""マテリアルドメイン Note: @see MaterialDomain.h"""
	MD_Surface = 0
	MD_DeferredDecal = 1
	MD_LightFunction = 2
	MD_Volume = 3
	MD_PostProcess = 4
	MD_UI = 5
	MD_RuntimeVirtualTexture = 6


@Embed.alias('E', prefix=True)
@UENUM()
class BlendMode(Enum):
	"""ブレンドモード Note: @see EngineTypes.h"""
	BLEND_Opaque = 0
	BLEND_Masked = 1
	BLEND_Translucent = 2
	BLEND_Additive = 3
	BLEND_Modulate = 4
	BLEND_AlphaComposite = 5
	BLEND_AlphaHoldout = 6
	BLEND_TranslucentColoredTransmittance = 7


@Embed.alias('E', prefix=True)
@UENUM()
class MaterialShadingModel(Enum):
	"""シェーディングモデル Note: @see EngineTypes.h"""
	MSM_Unlit = 0
	MSM_DefaultLit = 1
	MSM_Subsurface = 2
	MSM_PreintegratedSkin = 3
	MSM_ClearCoat = 4
	MSM_SubsurfaceProfile = 5
	MSM_TwoSidedFoliage = 6
	MSM_Hair = 7
	MSM_Cloth = 8
	MSM_Eye = 9
	MSM_SingleLayerWater = 10
	MSM_ThinTranslucent = 11
	MSM_Strata = 12


@Embed.struct
@Embed.alias('F', prefix=True)
@USTRUCT()
class MaterialInput(ExpressionInput):
	"""マテリアル入力PIN

	Note:
		```
		Material.hにも同名の定義があるが、実際に利用されるのは以下
		@see MaterialExpressionIO.h
		```
	"""
	...


@Embed.struct
@Embed.alias('F', prefix=True)
@USTRUCT()
class ColorMaterialInput(MaterialInput): """マテリアル入力PIN(カラー)"""
@Embed.struct
@Embed.alias('F', prefix=True)
@USTRUCT()
class ScalarMaterialInput(MaterialInput): """マテリアル入力PIN(スカラー)"""


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialEditorOnlyData(UObject):
	"""エディター専用データ(マテリアル)"""

	ExpressionCollection: Annotated[MaterialExpressionCollection, UPROPERTY()]
	EmissiveColor: Annotated[ColorMaterialInput, UPROPERTY()]
	Opacity: Annotated[ScalarMaterialInput, UPROPERTY()]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.ExpressionCollection = MaterialExpressionCollection()
		self.EmissiveColor = ColorMaterialInput()
		self.Opacity = ScalarMaterialInput()
