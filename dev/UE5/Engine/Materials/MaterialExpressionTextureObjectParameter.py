# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionTextureObjectParameter.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Engine.Texture import Texture as UTexture
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionParameter
from UE5.Engine.Materials.MaterialExpressionTextureSample import MaterialSamplerType


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionTextureObjectParameter(MaterialExpressionParameter):
	"""マテリアルパラメーター(texture)"""

	Texture: ObjectPtr[UTexture]
	SamplerType: MaterialSamplerType

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Texture = ObjectPtr[UTexture]()
		self.SamplerType = MaterialSamplerType.SAMPLERTYPE_Color

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<ex_texture: name: "{self.ParameterName}", texture: {"available" if self.Texture.Get else "null"}, sampler: {self.SamplerType.value}>'
