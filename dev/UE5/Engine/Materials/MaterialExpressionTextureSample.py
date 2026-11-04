# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionTextureSample.h

from enum import Enum

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('E', prefix=True)
@UCLASS()
class MaterialSamplerType(Enum):
	"""テクスチャーサンプル種別

	Note:
		```
		Color: デフォルト
		LinearColor: 浮動小数点テーブルなど
		LinearGrayscale: 同上
		@see Engine/Source/Runtime/Engine/Classes/Engine/EngineTypes.h
		```
	"""
	SAMPLERTYPE_Color = 'Color'
	SAMPLERTYPE_LinearColor = 'LinearColor'
	SAMPLERTYPE_LinearGrayscale = 'LinearGrayscale'


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionTextureSample(MaterialExpression):
	"""マテリアルパラメーター(sample)"""

	Coordinates: ExpressionInput
	TextureObject: ExpressionInput
	SamplerType: MaterialSamplerType

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Coordinates = ExpressionInput()
		self.TextureObject = ExpressionInput()
		self.SamplerType = MaterialSamplerType.SAMPLERTYPE_Color

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<sample: uv: {self.Coordinates}, texture: {self.TextureObject}, sampler: {self.SamplerType.value}>'
