# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionRgbToHsv.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionUnary


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionRgbToHsv(MaterialExpressionUnary):
	"""マテリアル関数式(rgb_to_hsv)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<rgb_to_hsv: rgb: {self.Input}>'
