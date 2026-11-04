# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpressionMaterialFunctionCall.h

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.CoreUObject.UObject.Object import GenStruct
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UFUNCTION, USTRUCT
from UE5.Engine.Materials.MaterialExpression import ExpressionInput, MaterialExpression
from UE5.Engine.Materials.MaterialFunction import MaterialFunctionInterface

from FDev.Main.Core.Lang.Convertion import safe_addr


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class FunctionExpressionInput(GenStruct):
	"""マテリアル関数式用入力PIN(関数コール用)"""

	Input: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.Input = ExpressionInput()


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class FunctionExpressionOutput(GenStruct):
	"""マテリアル関数式用出力PIN(関数コール用)"""

	Output: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		# XXX 本来はExpressionOutputだが特に利用することがないため一旦ExpressionInputで代用
		self.Output = ExpressionInput()


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionMaterialFunctionCall(MaterialExpression):
	"""マテリアル関数式(関数コール)"""

	MaterialFunction: ObjectPtr[MaterialFunctionInterface]
	FunctionInputs: list[FunctionExpressionInput]
	FunctionOutputs: list[FunctionExpressionOutput]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.MaterialFunction = ObjectPtr[MaterialFunctionInterface]()
		self.FunctionInputs = []
		self.FunctionOutputs = []

	@UFUNCTION()
	def SetMaterialFunction(self, mf: CP[MaterialFunctionInterface]) -> None:
		"""マテリアル関数を紐付け

		Args:
			mf: マテリアル関数
		Note:
			紐付けを行うことで引数と戻り値のリストが生成される
		"""
		self.MaterialFunction = ObjectPtr[MaterialFunctionInterface](mf)

		for _ in range(mf.on.args_num):
			self.FunctionInputs.append(FunctionExpressionInput())

		for _ in range(mf.on.return_num):
			self.FunctionOutputs.append(FunctionExpressionOutput())

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		join_args = ', '.join([str(arg.Input) for arg in self.FunctionInputs])
		return f'<call: name: {safe_addr(self.MaterialFunction.Get).on.GetFName()}, args: [{join_args}], returns: x{len(self.FunctionOutputs)}>'
