# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionDDY.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionDDY(MaterialExpression):
	"""マテリアルパラメーター(ddy)"""

	Value: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Value = ExpressionInput()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<ddy: value: {self.Value}>'
