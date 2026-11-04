# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionFloor.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionUnary


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionFloor(MaterialExpressionUnary):
	"""マテリアル関数式(floor)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<floor: value: {self.Input}>'
