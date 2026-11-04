# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionDotProduct.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionBinary


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionDotProduct(MaterialExpressionBinary):
	"""マテリアル関数式(2項演算/内積)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<dot: left: {self.A}, right: {self.B}>'
