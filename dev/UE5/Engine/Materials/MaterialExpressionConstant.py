# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionConstant.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionConstant(MaterialExpression):
	"""マテリアル関数式(定数/float)"""

	R: float

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.R = 0.0

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<float: {self.R}>'
