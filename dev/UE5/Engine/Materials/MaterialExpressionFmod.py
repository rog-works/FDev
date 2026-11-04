# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionFmod.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionBinary


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionFmod(MaterialExpressionBinary):
	"""マテリアル関数式(2項演算/余算)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<mod: left: {self.A}, right: {self.B}>'
