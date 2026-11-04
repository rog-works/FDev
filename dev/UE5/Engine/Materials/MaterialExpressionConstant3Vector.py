# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionConstant3Vector.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Math.Color import LinearColor
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionConstant3Vector(MaterialExpression):
	"""マテリアル関数式(定数/float3)"""

	Constant: LinearColor

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Constant = LinearColor()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<float3: ({self.Constant.R}, {self.Constant.G}, {self.Constant.B})>'
