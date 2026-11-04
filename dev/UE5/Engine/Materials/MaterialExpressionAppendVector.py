# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionAppendVector.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionBinary


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionAppendVector(MaterialExpressionBinary):
	"""マテリアル関数式(2項演算/ベクトル生成)"""

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<append_vector: a: {self.A}, b: {self.B}>'
