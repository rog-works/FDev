# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionCosine.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionCosine(MaterialExpression):
	"""マテリアル関数式(cos)"""

	Input: ExpressionInput
	Period: float

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Input = ExpressionInput()
		self.Period = 1.0

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<cos: ratio: {self.Input}, period: {self.Period}>'
