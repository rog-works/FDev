# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionFunctionInput.h

from enum import Enum

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.Guid import Guid
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UENUM
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('E', prefix=True)
@UENUM()
class FunctionInputType(Enum):
	"""引数の型の種別"""
	FunctionInput_Scalar = 'scalar'
	FunctionInput_Vector2 = 'float2'
	FunctionInput_Vector3 = 'float3'
	FunctionInput_Vector4 = 'float4'
	FunctionInput_Texture2D = 'texture2d'
	# FunctionInput_TextureCube = 'texture_cube'
	# FunctionInput_Texture2DArray = 'texture2d_array'
	# FunctionInput_VolumeTexture = 'volume_texture'
	FunctionInput_StaticBool = 'static_bool'
	# FunctionInput_MaterialAttributes = 'material_attributes'
	# FunctionInput_TextureExternal = 'texture_external'
	# FunctionInput_Bool = 'bool'
	# FunctionInput_Substrate = 'substrate'
	FunctionInput_MAX = 'max'


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionFunctionInput(MaterialExpression):
	"""マテリアル関数式(関数の引数)"""

	Preview: ExpressionInput
	InputName: Name
	InputType: FunctionInputType
	Description: str
	Id: Guid
	SortPriority: int
	bUsePreviewValueAsDefault: bool

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Preview = ExpressionInput()
		self.InputName = Name()
		self.InputType = FunctionInputType.FunctionInput_Scalar
		self.Description = ''
		self.Id = Guid.NewGuid()
		self.SortPriority = 0
		self.bUsePreviewValueAsDefault = False

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<param: name: "{self.InputName}", type: {self.InputType.value}, preview: {self.Preview}, desc: "{self.Description}">'
