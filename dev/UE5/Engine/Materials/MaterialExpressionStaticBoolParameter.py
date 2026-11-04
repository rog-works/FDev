# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionStaticBoolParameter.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpressionParameter


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionStaticBoolParameter(MaterialExpressionParameter):
	"""マテリアルパラメーター(bool)"""

	DefaultValue: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.DefaultValue = 1

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<ex_bool: name: "{self.ParameterName}", value: {"on" if self.DefaultValue else "off"}>'
