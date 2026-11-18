# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionNamedReroute.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.Guid import Guid
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.Core.UObject.NameTypes import Name as FName
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression

from App.Main.Core.Lang.Convertion import safe_addr


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionNamedRerouteDeclaration(MaterialExpression):
	"""マテリアル関数式(名前付きリルート)"""

	Input: ExpressionInput
	Name: FName
	VariableGuid: Guid

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Input = ExpressionInput()
		self.Name = FName()
		self.VariableGuid = Guid()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<var: name: "{self.Name}", exp: {self.Input}>'


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionNamedRerouteUsage(MaterialExpression):
	"""マテリアル関数式(名前付きリルート/参照)"""

	Declaration: ObjectPtr[MaterialExpressionNamedRerouteDeclaration]
	DeclarationGuid: Guid

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Declaration = ObjectPtr[MaterialExpressionNamedRerouteDeclaration]()
		self.DeclarationGuid = Guid()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<var_ref: name: "{safe_addr(self.Declaration.Get).on.Name.ToString()}">'
