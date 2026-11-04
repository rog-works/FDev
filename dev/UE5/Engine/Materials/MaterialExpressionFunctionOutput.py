# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionFunctionOutput.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.Guid import Guid
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionFunctionOutput(MaterialExpression):
	"""マテリアル関数式(関数の戻り値)"""

	A: ExpressionInput
	OutputName: Name
	Description: str
	Id: Guid
	SortPriority: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.A = ExpressionInput()
		self.OutputName = Name()
		self.Description = ''
		self.Id = Guid.NewGuid()
		self.SortPriority = 0

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<returns: name: "{self.OutputName}", exp: {self.A}, desc: "{self.Description}">'
