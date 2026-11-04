# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionPower.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionPower(MaterialExpression):
	"""マテリアル関数式(power)"""

	Base: ExpressionInput
	Exponent: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Base = ExpressionInput()
		self.Exponent = ExpressionInput()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<power: value: "{self.Base}", exponent: {self.Exponent}>'
