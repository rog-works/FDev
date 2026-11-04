# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionScalarParameter.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionParameter


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionScalarParameter(MaterialExpressionParameter):
	"""マテリアルパラメーター(float)"""

	DefaultValue: float
	SliderMin: float
	SliderMax: float

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.DefaultValue = 0.0
		self.SliderMin = 0.0
		self.SliderMax = 0.0

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<ex_float: name: "{self.ParameterName}", value: {self.DefaultValue}, slider: ({self.SliderMin} ~ {self.SliderMax})>'
