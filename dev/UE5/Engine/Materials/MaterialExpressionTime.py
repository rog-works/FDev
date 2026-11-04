# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionTime.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionTime(MaterialExpression):
	"""マテリアルパラメーター(time)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<time>'
