# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionLinearInterpolate.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionLinearInterpolate(MaterialExpression):
	"""マテリアル関数式(lerp)"""

	A: ExpressionInput
	B: ExpressionInput
	Alpha: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.A = ExpressionInput()
		self.B = ExpressionInput()
		self.Alpha = ExpressionInput()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<lerp: a: {self.A}, b: {self.B}, alpha: {self.Alpha}>'
