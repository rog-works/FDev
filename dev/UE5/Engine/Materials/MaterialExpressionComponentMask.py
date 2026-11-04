# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionComponentMask.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionComponentMask(MaterialExpression):
	"""マテリアル関数式(コンポーネントマスク)"""

	Input: ExpressionInput
	R: bool
	G: bool
	B: bool
	A: bool

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Input = ExpressionInput()
		self.R = True
		self.G = True
		self.B = False
		self.A = False

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<mask: via: {self.Input}, {"R" if self.R else "-"}{"G" if self.G else "-"}{"B" if self.B else "-"}{"A" if self.A else "-"}>'
