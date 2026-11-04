# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialFunction.h

from typing import Annotated

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import GenStruct, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UPROPERTY, USTRUCT
from UE5.Engine.Materials.MaterialExpression import MaterialExpression


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class MaterialExpressionCollection(GenStruct):
	"""マテリアル関数式コレクション Note: @see MaterialExpression.h"""

	Expressions: Annotated[list[CP[MaterialExpression]], UPROPERTY()]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.Expressions = []

	def AddExpression(self, exp: CP[MaterialExpression]) -> None:
		"""Args: exp: マテリアル関数式"""
		self.Expressions.append(exp)

	def Empty(self) -> None:
		"""式リストを初期化"""
		self.Expressions.clear()


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFunctionEditorOnlyData(UObject):
	"""エディター専用データ"""

	ExpressionCollection: Annotated[MaterialExpressionCollection, UPROPERTY()]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.ExpressionCollection = MaterialExpressionCollection()


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFunctionInterface(UObject):
	"""マテリアル関数(基底)"""

	args_num: int
	return_num: int

	def __init__(self) -> None:
		super().__init__()
		# @test XXX モック経由で設定する想定
		self.args_num = 0
		self.return_num = 0


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFunction(MaterialFunctionInterface):
	"""マテリアル関数"""

	Description: str
	__EditorOnlyData: CP[MaterialFunctionEditorOnlyData]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Description = ''
		# @python
		self.__EditorOnlyData = self.CreateDefaultSubobject(MaterialFunctionEditorOnlyData, '__EditorOnlyData')

	def GetEditorOnlyData(self) -> CP[MaterialFunctionEditorOnlyData]:
		"""Returns: エディター専用データ"""
		return self.__EditorOnlyData

	@Embed.python
	def __statements(self) -> list[CP[MaterialExpression]]:
		"""Returns: ステートメントのマテリアル関数式 Note: __str__用のメソッド"""
		# XXX 重複の無い出力とするためvar/returnsのみ抽出
		include_names = ['MaterialExpressionFunctionOutput', 'MaterialExpressionNamedRerouteDeclaration']
		return [exp for exp in self.GetEditorOnlyData().on.ExpressionCollection.Expressions if exp.raw.__class__.__name__ in include_names]

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		join_statements = ',\n    '.join([str(exp.raw) for exp in self.__statements()])
		return f'<function:\n  desc: "{self.Description}"\n  statements: [\n    {join_statements}\n]>'
