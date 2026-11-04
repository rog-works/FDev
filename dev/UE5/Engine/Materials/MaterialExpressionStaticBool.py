# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionStaticBool.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionStaticBool(MaterialExpression):
	"""マテリアル関数式(定数/bool)"""

	Value: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Value = 0

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<bool: {self.Value == 1}>'
