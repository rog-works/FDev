from typing import ClassVar

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.annotation import deprecated
from UE5.Core.Math.Color import LinearColor
from UE5.Core.Math.MathFwd import IntVector2
from UE5.Core.Misc.Guid import LexFromString
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.Object import NewObject, UClass, is_a
from UE5.Engine.Engine.Texture import Texture
from UE5.Engine.Materials.MaterialExpression import MaterialExpression, MaterialExpressionBinary, MaterialExpressionParameter, MaterialExpressionUnary
from UE5.Engine.Materials.MaterialExpressionAbs import MaterialExpressionAbs
from UE5.Engine.Materials.MaterialExpressionAdd import MaterialExpressionAdd
from UE5.Engine.Materials.MaterialExpressionAppendVector import MaterialExpressionAppendVector
from UE5.Engine.Materials.MaterialExpressionClamp import MaterialExpressionClamp
from UE5.Engine.Materials.MaterialExpressionCollectionParameter import MaterialExpressionCollectionParameter
from UE5.Engine.Materials.MaterialExpressionComponentMask import MaterialExpressionComponentMask
from UE5.Engine.Materials.MaterialExpressionConstant import MaterialExpressionConstant
from UE5.Engine.Materials.MaterialExpressionConstant2Vector import MaterialExpressionConstant2Vector
from UE5.Engine.Materials.MaterialExpressionConstant3Vector import MaterialExpressionConstant3Vector
from UE5.Engine.Materials.MaterialExpressionConstant4Vector import MaterialExpressionConstant4Vector
from UE5.Engine.Materials.MaterialExpressionCosine import MaterialExpressionCosine
from UE5.Engine.Materials.MaterialExpressionCrossProduct import MaterialExpressionCrossProduct
from UE5.Engine.Materials.MaterialExpressionDDX import MaterialExpressionDDX
from UE5.Engine.Materials.MaterialExpressionDDY import MaterialExpressionDDY
from UE5.Engine.Materials.MaterialExpressionDivide import MaterialExpressionDivide
from UE5.Engine.Materials.MaterialExpressionDotProduct import MaterialExpressionDotProduct
from UE5.Engine.Materials.MaterialExpressionFloor import MaterialExpressionFloor
from UE5.Engine.Materials.MaterialExpressionFmod import MaterialExpressionFmod
from UE5.Engine.Materials.MaterialExpressionFunctionInput import FunctionInputType, MaterialExpressionFunctionInput
from UE5.Engine.Materials.MaterialExpressionFunctionOutput import MaterialExpressionFunctionOutput
from UE5.Engine.Materials.MaterialExpressionHsvToRgb import MaterialExpressionHsvToRgb
from UE5.Engine.Materials.MaterialExpressionLength import MaterialExpressionLength
from UE5.Engine.Materials.MaterialExpressionLinearInterpolate import MaterialExpressionLinearInterpolate
from UE5.Engine.Materials.MaterialExpressionMaterialFunctionCall import MaterialExpressionMaterialFunctionCall
from UE5.Engine.Materials.MaterialExpressionMax import MaterialExpressionMax
from UE5.Engine.Materials.MaterialExpressionMin import MaterialExpressionMin
from UE5.Engine.Materials.MaterialExpressionMultiply import MaterialExpressionMultiply
from UE5.Engine.Materials.MaterialExpressionNamedReroute import MaterialExpressionNamedRerouteDeclaration, MaterialExpressionNamedRerouteUsage
from UE5.Engine.Materials.MaterialExpressionNormalize import MaterialExpressionNormalize
from UE5.Engine.Materials.MaterialExpressionOneMinus import MaterialExpressionOneMinus
from UE5.Engine.Materials.MaterialExpressionPanner import MaterialExpressionPanner
from UE5.Engine.Materials.MaterialExpressionPower import MaterialExpressionPower
from UE5.Engine.Materials.MaterialExpressionRgbToHsv import MaterialExpressionRgbToHsv
from UE5.Engine.Materials.MaterialExpressionSaturate import MaterialExpressionSaturate
from UE5.Engine.Materials.MaterialExpressionScalarParameter import MaterialExpressionScalarParameter
from UE5.Engine.Materials.MaterialExpressionSine import MaterialExpressionSine
from UE5.Engine.Materials.MaterialExpressionSmoothStep import MaterialExpressionSmoothStep
from UE5.Engine.Materials.MaterialExpressionStaticBool import MaterialExpressionStaticBool
from UE5.Engine.Materials.MaterialExpressionStaticBoolParameter import MaterialExpressionStaticBoolParameter
from UE5.Engine.Materials.MaterialExpressionStaticSwitch import MaterialExpressionStaticSwitch
from UE5.Engine.Materials.MaterialExpressionStep import MaterialExpressionStep
from UE5.Engine.Materials.MaterialExpressionSubtract import MaterialExpressionSubtract
from UE5.Engine.Materials.MaterialExpressionTangent import MaterialExpressionTangent
from UE5.Engine.Materials.MaterialExpressionTextureCoordinate import MaterialExpressionTextureCoordinate
from UE5.Engine.Materials.MaterialExpressionTextureObject import MaterialExpressionTextureObject
from UE5.Engine.Materials.MaterialExpressionTextureObjectParameter import MaterialExpressionTextureObjectParameter
from UE5.Engine.Materials.MaterialExpressionTextureSample import MaterialExpressionTextureSample, MaterialSamplerType
from UE5.Engine.Materials.MaterialExpressionTime import MaterialExpressionTime
from UE5.Engine.Materials.MaterialExpressionVectorParameter import MaterialExpressionVectorParameter
from UE5.Engine.Materials.MaterialFunction import MaterialFunction
from UE5.Engine.Materials.MaterialParameterCollection import MaterialParameterCollection

from App.Main.Const.ProjectConst import ClassPrefixs
from App.Main.Core.Asset.AssetPaths import AssetPaths
from App.Main.Core.Asset.Assets import Assets
from const.const_asset import AssetDomains, AssetNames


@Embed.struct
@Embed.alias(ClassPrefixs.General.value, prefix=True)
class MFAlign:
	"""整形データ"""

	__SpaceX: ClassVar[int] = 200
	__SpaceY: ClassVar[int] = 250
	__FoldY: ClassVar[int] = 50

	lines: int
	folds: int
	rows: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.lines = 0
		self.folds = 0
		self.rows = 0

	def add_row(self) -> None:
		"""行を追加"""
		self.folds = 0
		self.rows += 1

	def line_break(self) -> None:
		"""改行"""
		self.lines += 1
		self.folds = 0
		self.rows = 0

	def line_fold(self) -> None:
		"""行内の改行"""
		self.folds += 1

	def pos(self) -> IntVector2:
		"""Returns: 配置座標"""
		x = self.rows * self.__SpaceX
		y = self.lines * self.__SpaceY + self.folds * self.__FoldY
		return IntVector2(x, y)


@Embed.struct
@Embed.alias(ClassPrefixs.General.value, prefix=True)
class MFExp:
	"""式PIN"""

	exp: CP[MaterialExpression]
	index: int

	def __init__(self, exp: CP[MaterialExpression], index: int = 0) -> None:
		"""インスタンスを生成

		Args:
			exp: マテリアル関数式
			index: 使用する出力番号 (default = 0)
		"""
		self.exp = exp
		self.index = index

	def new_index(self, index: int) -> 'MFExp':
		"""出力番号を変更した複製を生成

		Args:
			index: 使用する出力番号
		Returns:
			インスタンス
		"""
		return MFExp(self.exp, index)


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class MFBuilder:
	"""アセットビルダー(マテリアル関数)"""
	
	__io_base_id: ClassVar[str] = '2DCF9ED5B0F44A31A2BDB35BBEAAB986'

	__assets: CP[Assets]
	__mf: CP[MaterialFunction]
	__symbols: dict[str, MFExp]
	__align: MFAlign

	def __init__(self, assets: CP[Assets], mf: CP[MaterialFunction]) -> None:
		"""インスタンスを生成

		Args:
			assets: アセットマネージャー
			mf: マテリアル関数
		"""
		self.__assets = assets
		self.__mf = mf
		self.__symbols = {}
		self.__align = MFAlign()

	def resolve_symbol(self, symbol: str) -> MFExp:
		"""シンボル名の式PINを解決

		Args:
			symbol: シンボル名
		Returns:
			式PIN
		"""
		return self.__symbols[symbol]
	
	def clear(self) -> None:
		"""設定を全て削除"""
		self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Empty()

	# ----- 関数シグネチャー -----

	def description(self, desc: str) -> None:
		"""関数コメントを設定

		Args:
			desc: コメント
		"""
		self.__mf.on.Description = desc
	
	def param(self, type_name: str, symbol: str, preview: MFExp, comment: str) -> MFExp:
		"""仮引数を生成

		Args:
			type_name: 型名
			symbol: シンボル名
			preview: プレビュー
			comment: 仮引数コメント
		Returns:
			変数
		"""
		to_type = Embed.static(MFBuilder.param).decl(lambda: {
			'bool': FunctionInputType.FunctionInput_StaticBool,
			'float': FunctionInputType.FunctionInput_Scalar,
			'float2': FunctionInputType.FunctionInput_Vector2,
			'float3': FunctionInputType.FunctionInput_Vector3,
			'float4': FunctionInputType.FunctionInput_Vector4,
			'texture': FunctionInputType.FunctionInput_Texture2D,
		})
		exp = NewObject(MaterialExpressionFunctionInput, self.__mf)
		exp.on.InputName = Name(symbol)
		exp.on.InputType = to_type[type_name]
		exp.on.Preview.Connect(preview.index, preview.exp)
		exp.on.Description = comment
		# 必ず有効なGuidを設定。これをしないと関数を呼び出す際に引数のPIN接続ができない
		LexFromString(exp.on.Id, self.__publish_id_for_param().encode())
		exp.on.SortPriority = self.__count_of_exps
		exp.on.bUsePreviewValueAsDefault = True
		self.__append_exp(exp)
		return MFExp(exp)

	def returns(self, symbol: str, result: MFExp, comment: str) -> MFExp:
		"""戻り値を生成

		Args:
			symbol: シンボル名
			result: 値
			comment: コメント
		Returns:
			戻り値
		"""
		exp = NewObject(MaterialExpressionFunctionOutput, self.__mf)
		exp.on.OutputName = Name(symbol)
		exp.on.Description = comment
		exp.on.A.Connect(result.index, result.exp)
		# 必ず有効なGuidを設定。これをしないと関数を呼び出す際に戻り値のPIN接続ができない
		LexFromString(exp.on.Id, self.__publish_id_for_returns().encode())
		exp.on.SortPriority = self.__count_of_exps
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- 変数 -----

	def var(self, symbol: str, var: MFExp) -> MFExp:
		"""変数を生成

		Args:
			symbol: シンボル名
			var: 入力値
		Returns:
			変数
		"""
		exp = NewObject(MaterialExpressionNamedRerouteDeclaration, self.__mf)
		exp.on.Name = Name(symbol)
		exp.on.Input.Connect(var.index, var.exp)
		LexFromString(exp.on.VariableGuid, self.__publish_id_for_var().encode())
		self.__append_exp(exp)
		self.__symbols[symbol] = MFExp(exp)
		return self.__symbols[symbol]

	def vars(self, symbols: list[str], result: MFExp) -> MFExp:
		"""変数を生成(分割代入)

		Args:
			symbols: シンボル名リスト
			result: 結果値(call/sample)
		Returns:
			変数
		"""
		for index in range(len(symbols)):
			self.var(symbols[index], result.new_index(index))

		return result

	@deprecated
	def var_ref(self, symbol: str) -> MFExp:
		"""変数参照を生成

		Args:
			symbol: シンボル名
		Returns:
			変数参照
		Note:
			@deprecated 原因は不明だが、戻り値の使用番号の2番目以降が使えなくなる不具合(?)のため使用NG
		"""
		exp = NewObject(MaterialExpressionNamedRerouteUsage, self.__mf)
		via = self.__symbols[symbol].exp.as_a(MaterialExpressionNamedRerouteDeclaration)
		exp.on.Declaration = ObjectPtr[MaterialExpressionNamedRerouteDeclaration](via)
		exp.on.DeclarationGuid = via.on.VariableGuid
		self.__append_exp(exp)
		return MFExp(exp)

	def ex_bool(self, symbol: str, group: str, uid: str, value: bool, desc: str) -> MFExp:
		"""公開パラメーター(bool)を生成

		Args:
			symbol: シンボル名
			gorup: グループ名
			uid: パラメーターID
			value: 真偽値
			desc: コメント
		Returns:
			変数
		"""
		exp = NewObject(MaterialExpressionStaticBoolParameter, self.__mf)
		exp.on.ParameterName = Name(symbol)
		exp.on.Group = Name(group)
		exp.on.DefaultValue = int(value)
		exp.on.Desc = desc
		LexFromString(exp.on.ExpressionGUID, uid.encode())
		self.__append_exp(exp)
		return MFExp(exp)

	def ex_float(self, symbol: str, group: str, uid: str, value: float, desc: str, minimum: float, maximum: float) -> MFExp:
		"""公開パラメーター(float)を生成

		Args:
			symbol: シンボル名
			gorup: グループ名
			uid: パラメーターID
			value: 初期値
			desc: コメント
			minimum: 下限値
			maximum: 上限値
		Returns:
			変数
		"""
		exp = NewObject(MaterialExpressionScalarParameter, self.__mf)
		exp.on.ParameterName = Name(symbol)
		exp.on.Group = Name(group)
		exp.on.DefaultValue = value
		exp.on.SliderMin = minimum
		exp.on.SliderMax = maximum
		exp.on.Desc = desc
		LexFromString(exp.on.ExpressionGUID, uid.encode())
		self.__append_exp(exp)
		return MFExp(exp)

	def ex_float3(self, symbol: str, group: str, uid: str, x: float, y: float, z: float, desc: str) -> MFExp:
		"""公開パラメーター(float3)を生成

		Args:
			symbol: シンボル名
			gorup: グループ名
			uid: パラメーターID
			x: X座標
			y: Y座標
			z: Z座標
			desc: コメント
		Returns:
			変数
		Note:
			```
			XXX 定義上の型はfloat4だが、実態としてはfloat3として扱われている模様
			XXX aを使えないケースが多々あるため、予めfloat3として扱う
			```
		"""
		exp = NewObject(MaterialExpressionVectorParameter, self.__mf)
		exp.on.ParameterName = Name(symbol)
		exp.on.Group = Name(group)
		exp.on.DefaultValue = LinearColor(x, y, z, 1.0)
		exp.on.Desc = desc
		LexFromString(exp.on.ExpressionGUID, uid.encode())
		self.__append_exp(exp)
		return MFExp(exp)

	def ex_texture(self, symbol: str, group: str, uid: str, src: str, desc: str, sampler: str) -> MFExp:
		"""公開パラメーター(texture)を生成

		Args:
			symbol: シンボル名
			gorup: グループ名
			uid: パラメーターID
			src: テクスチャーソースパス
			desc: コメント
			sampler: テクスチャーサンプル種別
		Returns:
			変数
		"""
		exp = NewObject(MaterialExpressionTextureObjectParameter, self.__mf)
		exp.on.ParameterName = Name(symbol)
		exp.on.Group = Name(group)
		exp.on.Texture = ObjectPtr[Texture](self.__assets.on.asset_of(Texture, AssetPaths.to_path(AssetDomains.Texture.value, src)))
		exp.on.Desc = desc
		exp.on.SamplerType = self.__to_sampler(sampler)
		LexFromString(exp.on.ExpressionGUID, uid.encode())
		self.__append_exp(exp)
		return MFExp(exp)

	# @deprecated
	# @Embed.python
	# def ex_curve(self, symbol: str, group: str, uid: str, easing: str, desc: str, alpha: MFExp) -> MFExp:
	# 	"""公開パラメーター(curve)を生成

	# 	Args:
	# 		symbol: シンボル名
	# 		gorup: グループ名
	# 		uid: パラメーターID
	# 		easing: イージングメソッド
	# 		desc: コメント
	# 		alpha: α値
	# 	Returns:
	# 		変数
	# 	Note:
	# 		```
	# 		* カーブアトラスは固定
	# 		* 返却値はRGBA(0番)に限定
	# 		* 他の公開パラメーターと違い、宣言と同時に使用するため、配置個所に注意
	# 		@deprecated 宣言と使用を分離できないため
	# 		```
	# 	"""
	# 	exp = NewObject(MaterialExpressionCurveAtlasRowParameter, self.__mf)
	# 	exp.on.ParameterName = Name(symbol)
	# 	exp.on.Group = Name(group)
	# 	exp.on.Curve = ObjectPtr[CurveLinearColor](self.__assets.on.resolve_of(CurveLinearColor, AssetPaths.to_easing_path(easing)))
	# 	exp.on.Atlas = ObjectPtr[CurveLinearColorAtlas](self.__assets.on.resolve_of(CurveLinearColorAtlas, AssetPaths.to_easing_path('hoge')))
	# 	exp.on.InputTime.Connect(alpha.index, alpha.exp)
	# 	exp.on.Desc = desc
	# 	LexFromString(exp.on.ExpressionGUID, uid.encode())
	# 	self.__append_exp(exp)
	# 	return MFExp(exp)

	# ----- 定数 -----

	def literal_b(self, value: bool) -> MFExp:
		"""リテラルを生成(bool)

		Args:
			value: 値
		Returns:
			bool
		"""
		exp = NewObject(MaterialExpressionStaticBool, self.__mf)
		exp.on.Value = int(value)
		self.__append_exp(exp)
		return MFExp(exp)

	def literal_f(self, value: float) -> MFExp:
		"""リテラルを生成(float)

		Args:
			value: 値
		Returns:
			float
		"""
		exp = NewObject(MaterialExpressionConstant, self.__mf)
		exp.on.R = value
		self.__append_exp(exp)
		return MFExp(exp)

	def literal_f2(self, x: float, y: float) -> MFExp:
		"""リテラルを生成(float2)

		Args:
			x: 値
			y: 値
		Returns:
			ベクトル(2次元)
		"""
		exp = NewObject(MaterialExpressionConstant2Vector, self.__mf)
		exp.on.R = x
		exp.on.G = y
		self.__append_exp(exp)
		return MFExp(exp)

	def literal_f3(self, x: float, y: float, z: float) -> MFExp:
		"""リテラルを生成(float3)

		Args:
			x: 値
			y: 値
			z: 値
		Returns:
			ベクトル(3次元)
		"""
		exp = NewObject(MaterialExpressionConstant3Vector, self.__mf)
		exp.on.Constant = LinearColor(x, y, z, 1.0)
		self.__append_exp(exp)
		return MFExp(exp)

	def literal_f4(self, r: float, g: float, b: float, a: float) -> MFExp:
		"""リテラルを生成(float4)

		Args:
			r: 値
			g: 値
			b: 値
			a: 値
		Returns:
			ベクトル(4次元)
		"""
		exp = NewObject(MaterialExpressionConstant4Vector, self.__mf)
		exp.on.Constant = LinearColor(r, g, b, a)
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- 四則演算 -----

	def add(self, left: MFExp, right: MFExp) -> MFExp:
		"""演算(加算)を生成

		Args:
			left: 左オペランド
			right: 右オペランド
		Returns:
			結果
		"""
		return self.__exp_bin(MaterialExpressionAdd, left, right)

	def sub(self, left: MFExp, right: MFExp) -> MFExp:
		"""演算(減算)を生成

		Args:
			left: 左オペランド
			right: 右オペランド
		Returns:
			結果
		"""
		return self.__exp_bin(MaterialExpressionSubtract, left, right)

	def mul(self, left: MFExp, right: MFExp) -> MFExp:
		"""演算(乗算)を生成

		Args:
			left: 左オペランド
			right: 右オペランド
		Returns:
			結果
		"""
		return self.__exp_bin(MaterialExpressionMultiply, left, right)

	def div(self, left: MFExp, right: MFExp) -> MFExp:
		"""演算(除算)を生成

		Args:
			left: 左オペランド
			right: 右オペランド
		Returns:
			結果
		"""
		return self.__exp_bin(MaterialExpressionDivide, left, right)

	def mod(self, left: MFExp, right: MFExp) -> MFExp:
		"""演算(余算)を生成

		Args:
			left: 左オペランド
			right: 右オペランド
		Returns:
			結果
		"""
		return self.__exp_bin(MaterialExpressionFmod, left, right)

	def one_minus(self, value: MFExp) -> MFExp:
		"""演算(1 - x)を生成

		Args:
			value: 値
		Returns:
			結果
		"""
		return self.__exp_unary(MaterialExpressionOneMinus, value)

	# ----- 算術演算 -----

	def abs(self, value: MFExp) -> MFExp:
		"""式(abs)を生成

		Args:
			value: 値
		Returns:
			絶対値
		"""
		return self.__exp_unary(MaterialExpressionAbs, value)

	# @deprecated
	# def atan2(self, y: MFExp, x: MFExp) -> MFExp:
	# 	"""式(atan2)を生成

	# 	Args:
	# 		y: Y座標
	# 		x: X座標
	# 	Returns:
	# 		弧度(ラジアン)
	# 	Note:
	# 		@deprecated: C++で非公開のため利用不可
	# 	"""
	# 	exp = NewObject(MaterialExpressionArctangent2, self.__mf)
	# 	exp.on.Y.Connect(y.index, y.exp)
	# 	exp.on.X.Connect(x.index, x.exp)
	# 	self.__append_exp(exp)
	# 	return MFExp(exp)

	def clamp(self, value: MFExp, minimum: MFExp, maximum: MFExp) -> MFExp:
		"""式(clamp)を生成

		Args:
			value: 値
			minimum: 下限値
			maximum: 上限値
		Returns:
			クランプ後の値
		Note:
			min/maxを初期値で利用する場合はsaturateを使用することを推奨
		"""
		exp = NewObject(MaterialExpressionClamp, self.__mf)
		exp.on.Input.Connect(value.index, value.exp)
		exp.on.Min.Connect(minimum.index, minimum.exp)
		exp.on.Max.Connect(maximum.index, maximum.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def cos(self, ratio: MFExp, period: float = 1.0) -> MFExp:
		"""式(cos)を生成

		Args:
			ratio: 1周の割合
			period: 1周の基数 (default = 1.0)
		Returns:
			0 ~ 1
		"""
		exp = NewObject(MaterialExpressionCosine, self.__mf)
		exp.on.Input.Connect(ratio.index, ratio.exp)
		exp.on.Period = period
		self.__append_exp(exp)
		return MFExp(exp)

	def floor(self, value: MFExp) -> MFExp:
		"""式(floor)を生成

		Args:
			value: 値
		Returns:
			整数部
		"""
		return self.__exp_unary(MaterialExpressionFloor, value)

	def length(self, vector: MFExp) -> MFExp:
		"""式(length)を生成

		Args:
			vector: ベクトル
		Returns:
			ベクトルの長さ
		"""
		return self.__exp_unary(MaterialExpressionLength, vector)

	def lerp(self, a: MFExp, b: MFExp, alpha: MFExp) -> MFExp:
		"""式(lerp)を生成

		Args:
			a: 始点
			b: 終点
			alpha: α値
		Returns:
			合成後の値
		"""
		exp = NewObject(MaterialExpressionLinearInterpolate, self.__mf)
		exp.on.A.Connect(a.index, a.exp)
		exp.on.B.Connect(b.index, b.exp)
		exp.on.Alpha.Connect(alpha.index, alpha.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def max(self, a: MFExp, b: MFExp) -> MFExp:
		"""式(max)を生成

		Args:
			a: 値1
			b: 値2
		Returns:
			大きい方の値
		"""
		return self.__exp_bin(MaterialExpressionMax, a, b)

	def min(self, a: MFExp, b: MFExp) -> MFExp:
		"""式(min)を生成

		Args:
			a: 値1
			b: 値2
		Returns:
			小さい方の値
		"""
		return self.__exp_bin(MaterialExpressionMin, a, b)

	def power(self, value: MFExp, exponent: MFExp) -> MFExp:
		"""式(power)を生成

		Args:
			value: 値
			exponent: 指数
		Returns:
			べき乗した値
		"""
		exp = NewObject(MaterialExpressionPower, self.__mf)
		exp.on.Base.Connect(value.index, value.exp)
		exp.on.Exponent.Connect(exponent.index, exponent.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def saturate(self, value: MFExp) -> MFExp:
		"""式(saturate)を生成

		Args:
			value: 値
		Returns:
			値(0 ~ 1)
		Note:
			clamp(x, 0, 1)と数学的には等価。HLSL的に高速
		"""
		return self.__exp_unary(MaterialExpressionSaturate, value)

	def sin(self, ratio: MFExp, period: float = 1.0) -> MFExp:
		"""式(sin)を生成

		Args:
			ratio: 1周の割合
			period: 1周の基数 (default = 1.0)
		Returns:
			0 ~ 1
		"""
		exp = NewObject(MaterialExpressionSine, self.__mf)
		exp.on.Input.Connect(ratio.index, ratio.exp)
		exp.on.Period = period
		self.__append_exp(exp)
		return MFExp(exp)

	def smoothstep(self, minimum: MFExp, maximum: MFExp, value: MFExp) -> MFExp:
		"""式(smoothstep)を生成

		Args:
			minimum: 下限値
			maximum: 上限値
			value: 値
		Returns:
			0 ~ 1
		"""
		exp = NewObject(MaterialExpressionSmoothStep, self.__mf)
		exp.on.Min.Connect(minimum.index, minimum.exp)
		exp.on.Max.Connect(maximum.index, maximum.exp)
		exp.on.Value.Connect(value.index, value.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def step(self, value: MFExp, threshold: MFExp) -> MFExp:
		"""式(step)を生成

		Args:
			value: 値
			threshold: 閾値
		Returns:
			0 or 1
		"""
		exp = NewObject(MaterialExpressionStep, self.__mf)
		exp.on.Y.Connect(value.index, value.exp)
		exp.on.X.Connect(threshold.index, threshold.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def tan(self, ratio: MFExp, period: float = 1.0) -> MFExp:
		"""式(tan)を生成

		Args:
			ratio: 1周の割合
			period: 1周の基数 (default = 1.0)
		Returns:
			0 ~ 1
		"""
		exp = NewObject(MaterialExpressionTangent, self.__mf)
		exp.on.Input.Connect(ratio.index, ratio.exp)
		exp.on.Period = period
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- ベクトル操作 -----

	def append(self, value: MFExp, x: MFExp) -> MFExp:
		"""式(append)を生成

		Args:
			value: 元の値(float or ベクトル)
			x: 追加する要素
		Returns:
			ベクトル(2次元)
		"""
		return self.__exp_bin(MaterialExpressionAppendVector, value, x)

	def cross(self, a: MFExp, b: MFExp) -> MFExp:
		"""式(cross)を生成

		Args:
			a: ベクトル1
			b: ベクトル2
		Returns:
			外積
		"""
		return self.__exp_bin(MaterialExpressionCrossProduct, a, b)

	def dot(self, a: MFExp, b: MFExp) -> MFExp:
		"""式(dot)を生成

		Args:
			a: ベクトル1
			b: ベクトル2
		Returns:
			内積
		"""
		return self.__exp_bin(MaterialExpressionDotProduct, a, b)

	def make_float2(self, x: MFExp, y: MFExp) -> MFExp:
		"""式(make_float3)を生成

		Args:
			x: X座標
			y: Y座標
		Returns:
			ベクトル(2次元)
		"""
		return self.__exp_bin(MaterialExpressionAppendVector, x, y)

	def make_float3(self, x: MFExp, y: MFExp, z: MFExp) -> MFExp:
		"""式(make_float3)を生成

		Args:
			x: X座標
			y: Y座標
			z: Z座標
		Returns:
			ベクトル(3次元)
		"""
		xy = self.__exp_bin(MaterialExpressionAppendVector, x, y)
		return self.__exp_bin(MaterialExpressionAppendVector, xy, z)

	def make_float4(self, x: MFExp, y: MFExp, z: MFExp, w: MFExp) -> MFExp:
		"""式(make_float4)を生成

		Args:
			x: X座標
			y: Y座標
			z: Z座標
			w: W座標
		Returns:
			ベクトル(4次元)
		"""
		xy = self.__exp_bin(MaterialExpressionAppendVector, x, y)
		xyz = self.__exp_bin(MaterialExpressionAppendVector, xy, z)
		return self.__exp_bin(MaterialExpressionAppendVector, xyz, w)

	def mask(self, value: MFExp, key: str) -> MFExp:
		"""式(mask)を生成

		Args:
			value: 値
			key: キー名
		Returns:
			float or ベクトル
		"""
		exp = NewObject(MaterialExpressionComponentMask, self.__mf)
		exp.on.Input.Connect(value.index, value.exp)
		exp.on.R = key.count('x') > 0
		exp.on.G = key.count('y') > 0
		exp.on.B = key.count('z') > 0
		exp.on.A = key == 'w'
		self.__append_exp(exp)
		return MFExp(exp)

	def normalize(self, vector: MFExp) -> MFExp:
		"""式(normalize)を生成

		Args:
			vector: ベクトル
		Returns:
			単位ベクトル
		"""
		exp = NewObject(MaterialExpressionNormalize, self.__mf)
		exp.on.VectorInput.Connect(vector.index, vector.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- カラー操作 -----

	def rgb_to_hsv(self, rgb: MFExp) -> MFExp:
		"""HSV変換を生成

		Args:
			rgb: RGB
		Returns:
			HSV
		"""
		return self.__exp_unary(MaterialExpressionRgbToHsv, rgb)

	def hsv_to_rgb(self, rgb: MFExp) -> MFExp:
		"""RGB変換を生成

		Args:
			hsv: HSV
		Returns:
			RGB
		"""
		return self.__exp_unary(MaterialExpressionHsvToRgb, rgb)

	# ----- テクスチャー操作 -----

	def panner(self, uv: MFExp, speed: MFExp) -> MFExp:
		"""UV座標スクロールを生成

		Args:
			uv: UV座標
			speed: スクロール速度
		Returns:
			UV座標
		"""
		exp = NewObject(MaterialExpressionPanner, self.__mf)
		exp.on.Coordinate.Connect(uv.index, uv.exp)
		exp.on.Speed.Connect(speed.index, speed.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def tex_coord(self, index: int) -> MFExp:
		"""UV座標を生成

		Args:
			index: UVインデックス
		Returns:
			UV座標
		"""
		exp = NewObject(MaterialExpressionTextureCoordinate, self.__mf)
		exp.on.CoordinateIndex = index
		self.__append_exp(exp)
		return MFExp(exp)

	def texture(self, src: str, sampler: str) -> MFExp:
		"""テクスチャーオブジェクトを生成

		Args:
			src: テクスチャーソースパス
			sampler: テクスチャーサンプル種別
		Returns:
			テクスチャー
		"""
		exp = NewObject(MaterialExpressionTextureObject, self.__mf)
		exp.on.Texture = ObjectPtr[Texture](self.__assets.on.asset_of(Texture, AssetPaths.to_path(AssetDomains.Texture.value, src)))
		exp.on.SamplerType = self.__to_sampler(sampler)
		self.__append_exp(exp)
		return MFExp(exp)

	def sample(self, texture: MFExp, uv: MFExp, sampler: str) -> MFExp:
		"""テクスチャーサンプリングを生成

		Args:
			texture: テクスチャー
			uv: UV座標 XXX 省略する方法を検討
			sampler: テクスチャーサンプル種別
		Returns:
			RGBA
		Note:
			返却値はRGBA(5番)に限定
		"""
		exp = NewObject(MaterialExpressionTextureSample, self.__mf)
		exp.on.TextureObject.Connect(texture.index, texture.exp)
		exp.on.Coordinates.Connect(uv.index, uv.exp)
		exp.on.SamplerType = self.__to_sampler(sampler)
		self.__append_exp(exp)
		return MFExp(exp, 5)

	# ----- ピクセルシェーダー -----

	def ddx(self, value: MFExp) -> MFExp:
		"""式(ddx)を生成

		Args:
			value: 値
		Returns:
			勾配
		"""
		exp = NewObject(MaterialExpressionDDX, self.__mf)
		exp.on.Value.Connect(value.index, value.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def ddy(self, value: MFExp) -> MFExp:
		"""式(ddy)を生成

		Args:
			value: 値
		Returns:
			勾配
		"""
		exp = NewObject(MaterialExpressionDDY, self.__mf)
		exp.on.Value.Connect(value.index, value.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- パラメーターコレクション -----

	@deprecated
	def const_by(self, name: str) -> MFExp:
		"""パラメーターコレクション参照を生成

		Args:
			name: 値
		Returns:
			定数値(float)
		Note:
			@deprecated 未使用
		"""
		exp = NewObject(MaterialExpressionCollectionParameter, self.__mf)
		collection = self.__assets.on.asset_of(MaterialParameterCollection, AssetPaths.to_path(AssetDomains.MaterialConst.value, AssetNames.Parameters.value))
		exp.on.Collection = ObjectPtr[MaterialParameterCollection](collection)
		exp.on.ParameterName = Name(name)
		exp.on.ParameterId = collection.on.GetParameterId(exp.on.ParameterName)
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- 時間 -----

	def time(self) -> MFExp:
		"""経過時間を生成

		Returns:
			経過時間
		"""
		exp = NewObject(MaterialExpressionTime, self.__mf)
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- フロー制御 -----

	def ternary(self, then: MFExp, reject: MFExp, on: MFExp) -> MFExp:
		"""スイッチ構文を生成

		Args:
			then: 真の時の値
			reject: 偽の時の値
			on: 真偽値
		Returns:
			結果
		"""
		exp = NewObject(MaterialExpressionStaticSwitch, self.__mf)
		exp.on.A.Connect(then.index, then.exp)
		exp.on.B.Connect(reject.index, reject.exp)
		exp.on.Value.Connect(on.index, on.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	# ----- 関数コール -----
	
	def call(self, func_name: str, args: list[MFExp]) -> MFExp:
		"""関数コールを生成

		Args:
			func_name: マテリアル関数の名前
			args: 引数リスト
		Returns:
			戻り値のリスト
		"""
		exp = NewObject(MaterialExpressionMaterialFunctionCall, self.__mf)
		# XXX 関数名の接頭辞をフォルダー名とする
		src = '{dir}/{name}'.format(dir=func_name.split('_')[0], name=func_name)
		exp.on.SetMaterialFunction(self.__assets.on.asset_of(MaterialFunction, AssetPaths.to_path(AssetDomains.MaterialFunc.value, src)))
		for index, arg in enumerate(args):
			exp.on.FunctionInputs[index].Input.Connect(arg.index, arg.exp)

		self.__append_exp(exp)
		return MFExp(exp)

	# ----- ここまで -----

	def __to_sampler(self, sampler: str) -> MaterialSamplerType:
		"""テクスチャーサンプル(定数)に変換

		Args:
			sampler: テクスチャーサンプル(文字列)
		Returns:
			テクスチャーサンプル(定数)
		"""
		to_sampler = {
			MaterialSamplerType.SAMPLERTYPE_Color.value: MaterialSamplerType.SAMPLERTYPE_Color,
			MaterialSamplerType.SAMPLERTYPE_LinearColor.value: MaterialSamplerType.SAMPLERTYPE_LinearColor,
			MaterialSamplerType.SAMPLERTYPE_LinearGrayscale.value: MaterialSamplerType.SAMPLERTYPE_LinearGrayscale,
		}
		return to_sampler[sampler]
	
	def __exp_unary[T_Unary: MaterialExpressionUnary](self, unary_type: type[T_Unary], value: MFExp) -> MFExp:
		"""式(単項)を生成

		Args:
			unary_type: 単項式の型
			value: 値
		Returns:
			結果
		"""
		exp = NewObject(unary_type, self.__mf)
		exp.on.Input.Connect(value.index, value.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	def __exp_bin[T_Bin: MaterialExpressionBinary](self, bin_type: type[T_Bin], a: MFExp, b: MFExp) -> MFExp:
		"""式(2項)を生成

		Args:
			bin_type: 2項式の型
			a: 値1
			b: 値2
		Returns:
			結果
		"""
		exp = NewObject(bin_type, self.__mf)
		exp.on.A.Connect(a.index, a.exp)
		exp.on.B.Connect(b.index, b.exp)
		self.__append_exp(exp)
		return MFExp(exp)

	@property	
	def __count_of_exps(self) -> int:
		"""Returns: マテリアル関数式の数"""
		return len(self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Expressions)

	def __count_for_exps(self, uclass: CP[UClass]) -> int:
		"""uclass: カウント対象の式の型情報 Returns: 対象の式の数"""
		count = 0
		for exp in self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Expressions:
			if exp.on.IsA(uclass):
				count += 1

		return count

	def __publish_id_for_param(self) -> str:
		"""Returns: ユニークID(引数)"""
		return self.__publish_id(str('A') + str(self.__count_for_exps(MaterialExpressionFunctionInput.StaticClass())))

	def __publish_id_for_returns(self) -> str:
		"""Returns: ユニークID(戻り値)"""
		return self.__publish_id(str('B') + str(self.__count_for_exps(MaterialExpressionFunctionOutput.StaticClass())))

	@deprecated
	def __publish_id_for_export(self) -> str:
		"""Returns: ユニークID(公開パラメーター) Note: @deprecated 未使用"""
		return self.__publish_id(str('C') + str(self.__count_for_exps(MaterialExpressionParameter.StaticClass())))

	def __publish_id_for_var(self) -> str:
		"""Returns: ユニークID(変数)"""
		return self.__publish_id(str('D') + str(self.__count_for_exps(MaterialExpressionNamedRerouteDeclaration.StaticClass())))

	def __publish_id(self, id_str: str) -> str:
		"""マテリアル関数内でユニークなIDを発行

		Args:
			id_str: ID
		Returns:
			ID
		Note:
			```
			* 引数/戻り値/公開パラメーターに対して使用
			* IDは関数内でユニークであれば良く、別の関数のIDとの重複を気にする必要は無い
			* 基本的に対象の式のインデックスを基準とするため、インデックスが変わると既存の接続が切れてしまう点に注意
			```
		"""
		return self.__io_base_id[:32 - len(id_str)] + id_str

	def __append_exp(self, exp: CP[MaterialExpression]) -> None:
		"""マテリアル関数に式を追加

		Args:
			exp: マテリアル関数式
		"""
		# XXX ノードが重ならない様に適当に配置
		if self.__line_break(exp):
			self.__align.line_break()
		elif self.__line_fold(exp):
			self.__align.line_fold()
		elif len(self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Expressions) > 0:
			self.__align.add_row()

		pos = self.__align.pos()
		exp.on.MaterialExpressionEditorX = pos.X
		exp.on.MaterialExpressionEditorY = pos.Y

		self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.AddExpression(exp)

	def __line_break(self, curr: CP[MaterialExpression]) -> bool:
		"""式の登録状況から改行を判定

		Args:
			curr: 登録予定のマテリアル関数式
		Returns:
			True = 改行
		"""
		total = len(self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Expressions)
		if total == 0:
			return False

		prev = self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Expressions[total - 1]
		if not (is_a(prev, MaterialExpressionFunctionInput) or is_a(prev, MaterialExpressionNamedRerouteDeclaration) or is_a(prev, MaterialExpressionParameter)):
			return False

		if is_a(curr, MaterialExpressionFunctionInput) or is_a(curr, MaterialExpressionNamedRerouteDeclaration) or is_a(curr, MaterialExpressionParameter):
			return False

		return True

	def __line_fold(self, curr: CP[MaterialExpression]) -> bool:
		"""式の登録状況から行内の改行を判定

		Args:
			curr: 登録予定のマテリアル関数式
		Returns:
			True = 行内の改行
		"""
		total = len(self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Expressions)
		if total == 0:
			return False

		prev = self.__mf.on.GetEditorOnlyData().on.ExpressionCollection.Expressions[total - 1]
		if is_a(prev, MaterialExpressionNamedRerouteUsage) and is_a(curr, MaterialExpressionNamedRerouteUsage):
			return True
		elif is_a(prev, MaterialExpressionNamedRerouteDeclaration) and is_a(curr, MaterialExpressionNamedRerouteDeclaration):
			return True

		return False
