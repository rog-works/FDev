# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionClamp.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionClamp(MaterialExpression):
	"""マテリアル関数式(clamp)"""

	Input: ExpressionInput
	Min: ExpressionInput
	Max: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Input = ExpressionInput()
		self.Min = ExpressionInput()
		self.Max = ExpressionInput()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<lerp: value: {self.Input}, min: {self.Min}, max: {self.Max}>'
