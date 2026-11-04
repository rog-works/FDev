# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialExpression.h

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.convertion import as_a
from UE5.Core.Misc.Guid import Guid
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.Object import GenStruct, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, USTRUCT


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpression(UObject):
	"""マテリアル関数式(基底)"""

	MaterialExpressionEditorX: int
	MaterialExpressionEditorY: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.MaterialExpressionEditorX = 0
		self.MaterialExpressionEditorY = 0



@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class ExpressionInput(GenStruct):
	"""マテリアル関数式用入力PIN"""

	Expression: CP[MaterialExpression] | None
	OutputIndex: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.Expression = None
		self.OutputIndex = 0

	def Connect(self, index: int, exp: CP[MaterialExpression]) -> None:
		"""出力PINを接続

		Args:
			index: 使用する出力番号
			exp: マテリアル関数式
		"""
		self.Expression = exp
		self.OutputIndex = index

	@Embed.python
	def __str__(self) -> str:
		"""Returns: 文字列表現"""
		# XXX 基本的にnull時に参照することは無いが、デバッグ上はnullになり得るので一応対処
		if self.Expression is None:
			return 'null'

		# XXX param/varの変数参照の出力は循環しているため名前だけに省略
		if self.Expression.raw.__class__.__name__ == 'MaterialExpressionNamedRerouteDeclaration':
			return f'<var: ref: "{as_a(Name, getattr(self.Expression.raw, "Name")).ToString()}">'
		elif self.Expression.raw.__class__.__name__ == 'MaterialExpressionMaterialFunctionCall':
			return f'{str(self.Expression.raw)}[{self.OutputIndex}]'
		else:
			return str(self.Expression.raw)


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionUnary(MaterialExpression):
	"""マテリアル関数式(単項処理/基底) Note: 本来は存在しない定義である点に注意"""

	Input: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Input = ExpressionInput()


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionBinary(MaterialExpression):
	"""マテリアル関数式(2項処理/基底) Note: 本来は存在しない定義である点に注意"""

	A: ExpressionInput
	B: ExpressionInput

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.A = ExpressionInput()
		self.B = ExpressionInput()


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionParameter(MaterialExpression):
	"""マテリアルパラメーター(基底)"""

	ParameterName: Name
	ExpressionGUID: Guid
	Group: Name
	SortPriority: int
	Desc: str

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.ParameterName = Name()
		self.ExpressionGUID = Guid()
		self.Group = Name()
		self.SortPriority = 32
		self.Desc = ''
