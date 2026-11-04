# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionTextureCoordinate.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionTextureCoordinate(MaterialExpression):
	"""マテリアル関数式(tex_coord)"""

	CoordinateIndex: int
	UTiling: float
	VTiling: float

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.CoordinateIndex = 0
		# XXX 未使用
		self.UTiling = 0.0
		self.VTiling = 0.0

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<tex_coord: index: {self.CoordinateIndex}>'
