# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionPanner.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionPanner(MaterialExpression):
	"""マテリアルパラメーター(panner)"""

	Coordinate: ExpressionInput
	Speed: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Coordinate = ExpressionInput()
		self.Speed = ExpressionInput()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<panner: uv: {self.Coordinate}, speed: {self.Speed}>'
