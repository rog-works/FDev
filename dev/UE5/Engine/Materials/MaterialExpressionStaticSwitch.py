# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionStaticSwitch.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionStaticSwitch(MaterialExpression):
	"""マテリアルパラメーター(ternary)"""

	A: ExpressionInput
	B: ExpressionInput
	Value: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.A = ExpressionInput()
		self.B = ExpressionInput()
		self.Value = ExpressionInput()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<ternary: then: {self.A}, reject: {self.B}, on: {self.Value}>'
