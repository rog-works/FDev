# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionMax.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionBinary


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionMax(MaterialExpressionBinary):
	"""マテリアル関数式(max)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<max: a: {self.A}, b: {self.B}>'
