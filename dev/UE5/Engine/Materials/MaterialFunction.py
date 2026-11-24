# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialFunction.h

from typing import Annotated

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import NewObject, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UPROPERTY
from UE5.Engine.Materials.MaterialExpression import MaterialExpression, MaterialExpressionCollection
from UE5.Engine.Materials.MaterialFunctionInterface import MaterialFunctionInterface


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFunctionEditorOnlyData(UObject):
	"""エディター専用データ(マテリアル関数)"""

	ExpressionCollection: Annotated[MaterialExpressionCollection, UPROPERTY()]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.ExpressionCollection = MaterialExpressionCollection()


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialFunction(MaterialFunctionInterface):
	"""マテリアル関数"""

	Description: str
	__EditorOnlyData: CP[MaterialFunctionEditorOnlyData] | None

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Description = ''
		self.__EditorOnlyData = None

	def GetEditorOnlyData(self) -> CP[MaterialFunctionEditorOnlyData]:
		"""Returns: エディター専用データ"""
		if not self.__EditorOnlyData:
			self.__EditorOnlyData = NewObject(MaterialFunctionEditorOnlyData, CP(self))

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
