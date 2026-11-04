# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionMultiply.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionBinary


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionMultiply(MaterialExpressionBinary):
	"""マテリアル関数式(2項演算/乗算)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<mul: left: {self.A}, right: {self.B}>'
