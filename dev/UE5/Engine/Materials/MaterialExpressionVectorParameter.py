# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionVectorParameter.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Math.Color import LinearColor
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionParameter


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionVectorParameter(MaterialExpressionParameter):
	"""マテリアルパラメーター(float4)"""

	DefaultValue: LinearColor

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.DefaultValue = LinearColor()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<ex_float4: name: "{self.ParameterName}", value: {self.DefaultValue}>'
