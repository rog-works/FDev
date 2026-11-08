// @tranp.meta: {"version":"0.9.20","module":{"hash":"ce2db876331a360c38364606242e50fd","path":"FDev.Editor.Material.MFBuilder"},"transpiler":{"version":"0.9.7","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Math/Color.h"
#include "Math/MathFwd.h"
#include "Misc/Guid.h"
#include "Templates/SharedPointer.h"
#include "UObject/NameTypes.h"
#include "UObject/Object.h"
#include "Engine/Texture.h"
#include "Materials/MaterialExpression.h"
#include "Materials/MaterialExpressionAbs.h"
#include "Materials/MaterialExpressionAdd.h"
#include "Materials/MaterialExpressionAppendVector.h"
#include "Materials/MaterialExpressionClamp.h"
#include "Materials/MaterialExpressionCollectionParameter.h"
#include "Materials/MaterialExpressionComponentMask.h"
#include "Materials/MaterialExpressionConstant.h"
#include "Materials/MaterialExpressionConstant2Vector.h"
#include "Materials/MaterialExpressionConstant3Vector.h"
#include "Materials/MaterialExpressionConstant4Vector.h"
#include "Materials/MaterialExpressionCosine.h"
#include "Materials/MaterialExpressionCrossProduct.h"
#include "Materials/MaterialExpressionDDX.h"
#include "Materials/MaterialExpressionDDY.h"
#include "Materials/MaterialExpressionDivide.h"
#include "Materials/MaterialExpressionDotProduct.h"
#include "Materials/MaterialExpressionFloor.h"
#include "Materials/MaterialExpressionFmod.h"
#include "Materials/MaterialExpressionFunctionInput.h"
#include "Materials/MaterialExpressionFunctionOutput.h"
#include "Materials/MaterialExpressionHsvToRgb.h"
#include "Materials/MaterialExpressionLength.h"
#include "Materials/MaterialExpressionLinearInterpolate.h"
#include "Materials/MaterialExpressionMaterialFunctionCall.h"
#include "Materials/MaterialExpressionMax.h"
#include "Materials/MaterialExpressionMin.h"
#include "Materials/MaterialExpressionMultiply.h"
#include "Materials/MaterialExpressionNamedReroute.h"
#include "Materials/MaterialExpressionNormalize.h"
#include "Materials/MaterialExpressionOneMinus.h"
#include "Materials/MaterialExpressionPanner.h"
#include "Materials/MaterialExpressionPower.h"
#include "Materials/MaterialExpressionRgbToHsv.h"
#include "Materials/MaterialExpressionSaturate.h"
#include "Materials/MaterialExpressionScalarParameter.h"
#include "Materials/MaterialExpressionSine.h"
#include "Materials/MaterialExpressionSmoothStep.h"
#include "Materials/MaterialExpressionStaticBool.h"
#include "Materials/MaterialExpressionStaticBoolParameter.h"
#include "Materials/MaterialExpressionStaticSwitch.h"
#include "Materials/MaterialExpressionStep.h"
#include "Materials/MaterialExpressionSubtract.h"
#include "Materials/MaterialExpressionTangent.h"
#include "Materials/MaterialExpressionTextureCoordinate.h"
#include "Materials/MaterialExpressionTextureObject.h"
#include "Materials/MaterialExpressionTextureObjectParameter.h"
#include "Materials/MaterialExpressionTextureSample.h"
#include "Materials/MaterialExpressionTime.h"
#include "Materials/MaterialExpressionVectorParameter.h"
#include "Materials/MaterialFunction.h"
#include "Materials/MaterialParameterCollection.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Asset/AssetPaths.h"
#include "FDev/Main/Core/Asset/Assets.h"
#include "FDev/Main/Core/Core.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "tranp/app/lang/annotation.h"
// #include "const/const_asset.h"
/**
 * 整形データ
 */
struct FDevMFAlign {
	private: inline static int p__SpaceX = 200;
	private: inline static int p__SpaceY = 250;
	private: inline static int p__FoldY = 50;
	public: int lines;
	public: int folds;
	public: int rows;
	public:
	/**
	 * インスタンスを生成
	 */
	FDevMFAlign() : lines(0), folds(0), rows(0) {}
	public:
	/**
	 * 行を追加
	 */
	void add_row() {
		this->folds = 0;
		this->rows += 1;
	}
	public:
	/**
	 * 改行
	 */
	void line_break() {
		this->lines += 1;
		this->folds = 0;
		this->rows = 0;
	}
	public:
	/**
	 * 行内の改行
	 */
	void line_fold() {
		this->folds += 1;
	}
	public:
	/**
	 *
	 * @return 配置座標
	 */
	FIntVector2 pos() {
		int x = this->rows * this->p__SpaceX;
		int y = this->lines * this->p__SpaceY + this->folds * this->p__FoldY;
		return FIntVector2(x, y);
	}
};
/**
 * 式PIN
 */
struct FDevMFExp {
	public: UMaterialExpression* exp;
	public: int index;
	public:
	/**
	 * インスタンスを生成
	 * @param exp マテリアル関数式
	 * @param index 使用する出力番号 (default = 0)
	 */
	FDevMFExp(UMaterialExpression* exp, int index = 0) : exp(exp), index(index) {}
	public:
	/**
	 * 出力番号を変更した複製を生成
	 * @param index 使用する出力番号
	 * @return インスタンス
	 */
	FDevMFExp new_index(int index) {
		return FDevMFExp(this->exp, index);
	}
};
/**
 * アセットビルダー(マテリアル関数)
 */
class FDevMFBuilder {
	private: inline static FString p__io_base_id = "2DCF9ED5B0F44A31A2BDB35BBEAAB986";
	private: UFDevAssets* p__assets;
	private: UMaterialFunction* p__mf;
	private: TMap<FString, FDevMFExp> p__symbols;
	private: FDevMFAlign p__align;
	public:
	/**
	 * インスタンスを生成
	 * @param assets アセットマネージャー
	 * @param mf マテリアル関数
	 */
	FDevMFBuilder(UFDevAssets* assets, UMaterialFunction* mf) : p__assets(assets), p__mf(mf), p__symbols(), p__align() {}
	public:
	/**
	 * シンボル名の式PINを解決
	 * @param symbol シンボル名
	 * @return 式PIN
	 */
	FDevMFExp resolve_symbol(const FString& symbol) {
		return this->p__symbols[symbol];
	}
	public:
	/**
	 * 設定を全て削除
	 */
	void clear() {
		this->p__mf->GetEditorOnlyData()->ExpressionCollection.Empty();
	}
	// ----- 関数シグネチャー -----
	public:
	/**
	 * 関数コメントを設定
	 * @param desc コメント
	 */
	void description(const FString& desc) {
		this->p__mf->Description = desc;
	}
	public:
	/**
	 * 仮引数を生成
	 * @param type_name 型名
	 * @param symbol シンボル名
	 * @param preview プレビュー
	 * @param comment 仮引数コメント
	 * @return 変数
	 */
	FDevMFExp param(const FString& type_name, const FString& symbol, FDevMFExp preview, const FString& comment) {
		static TMap<FString, EFunctionInputType> to_type = {
			{"bool", EFunctionInputType::FunctionInput_StaticBool},
			{"float", EFunctionInputType::FunctionInput_Scalar},
			{"float2", EFunctionInputType::FunctionInput_Vector2},
			{"float3", EFunctionInputType::FunctionInput_Vector3},
			{"float4", EFunctionInputType::FunctionInput_Vector4},
			{"texture", EFunctionInputType::FunctionInput_Texture2D},
		};
		UMaterialExpressionFunctionInput* exp = NewObject<UMaterialExpressionFunctionInput>(this->p__mf);
		exp->InputName = FName(symbol);
		exp->InputType = to_type[type_name];
		exp->Preview.Connect(preview.index, preview.exp);
		exp->Description = comment;
		// 必ず有効なGuidを設定。これをしないと関数を呼び出す際に引数のPIN接続ができない
		LexFromString(exp->Id, (*this->p__publish_id_for_param()));
		exp->SortPriority = this->p__count_of_exps();
		exp->bUsePreviewValueAsDefault = true;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 戻り値を生成
	 * @param symbol シンボル名
	 * @param result 値
	 * @param comment コメント
	 * @return 戻り値
	 */
	FDevMFExp returns(const FString& symbol, FDevMFExp result, const FString& comment) {
		UMaterialExpressionFunctionOutput* exp = NewObject<UMaterialExpressionFunctionOutput>(this->p__mf);
		exp->OutputName = FName(symbol);
		exp->Description = comment;
		exp->A.Connect(result.index, result.exp);
		// 必ず有効なGuidを設定。これをしないと関数を呼び出す際に戻り値のPIN接続ができない
		LexFromString(exp->Id, (*this->p__publish_id_for_returns()));
		exp->SortPriority = this->p__count_of_exps();
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- 変数 -----
	public:
	/**
	 * 変数を生成
	 * @param symbol シンボル名
	 * @param var 入力値
	 * @return 変数
	 */
	FDevMFExp var(const FString& symbol, FDevMFExp var) {
		UMaterialExpressionNamedRerouteDeclaration* exp = NewObject<UMaterialExpressionNamedRerouteDeclaration>(this->p__mf);
		exp->Name = FName(symbol);
		exp->Input.Connect(var.index, var.exp);
		LexFromString(exp->VariableGuid, (*this->p__publish_id_for_var()));
		this->p__append_exp(exp);
		this->p__symbols.Add(symbol, FDevMFExp(exp));
		return this->p__symbols[symbol];
	}
	public:
	/**
	 * 変数を生成(分割代入)
	 * @param symbols シンボル名リスト
	 * @param result 結果値(call/sample)
	 * @return 変数
	 */
	FDevMFExp vars(const TArray<FString>& symbols, FDevMFExp result) {
		for (auto index = 0; index < symbols.Num(); index += 1) {
			this->var(symbols[index], result.new_index(index));
		}
		return result;
	}
	public:
	/**
	 * 変数参照を生成
	 * @param symbol シンボル名
	 * @return 変数参照
	 * @note @deprecated 原因は不明だが、戻り値の使用番号の2番目以降が使えなくなる不具合(?)のため使用NG
	 */
	FDevMFExp var_ref(const FString& symbol) {
		UMaterialExpressionNamedRerouteUsage* exp = NewObject<UMaterialExpressionNamedRerouteUsage>(this->p__mf);
		UMaterialExpressionNamedRerouteDeclaration* via = CastChecked<UMaterialExpressionNamedRerouteDeclaration>(this->p__symbols[symbol].exp);
		exp->Declaration = TObjectPtr<UMaterialExpressionNamedRerouteDeclaration>(via);
		exp->DeclarationGuid = via->VariableGuid;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 公開パラメーター(bool)を生成
	 * @param symbol シンボル名
	 * @param gorup グループ名
	 * @param uid パラメーターID
	 * @param value 真偽値
	 * @param desc コメント
	 * @return 変数
	 */
	FDevMFExp ex_bool(const FString& symbol, const FString& group, const FString& uid, bool value, const FString& desc) {
		UMaterialExpressionStaticBoolParameter* exp = NewObject<UMaterialExpressionStaticBoolParameter>(this->p__mf);
		exp->ParameterName = FName(symbol);
		exp->Group = FName(group);
		exp->DefaultValue = (int(value));
		exp->Desc = desc;
		LexFromString(exp->ExpressionGUID, (*uid));
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 公開パラメーター(float)を生成
	 * @param symbol シンボル名
	 * @param gorup グループ名
	 * @param uid パラメーターID
	 * @param value 初期値
	 * @param desc コメント
	 * @param minimum 下限値
	 * @param maximum 上限値
	 * @return 変数
	 */
	FDevMFExp ex_float(const FString& symbol, const FString& group, const FString& uid, float value, const FString& desc, float minimum, float maximum) {
		UMaterialExpressionScalarParameter* exp = NewObject<UMaterialExpressionScalarParameter>(this->p__mf);
		exp->ParameterName = FName(symbol);
		exp->Group = FName(group);
		exp->DefaultValue = value;
		exp->SliderMin = minimum;
		exp->SliderMax = maximum;
		exp->Desc = desc;
		LexFromString(exp->ExpressionGUID, (*uid));
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 公開パラメーター(float3)を生成
	 * @param symbol シンボル名
	 * @param gorup グループ名
	 * @param uid パラメーターID
	 * @param x X座標
	 * @param y Y座標
	 * @param z Z座標
	 * @param desc コメント
	 * @return 変数
	 * @note
	 * ```
	 * XXX 定義上の型はfloat4だが、実態としてはfloat3として扱われている模様
	 * XXX aを使えないケースが多々あるため、予めfloat3として扱う
	 * ```
	 */
	FDevMFExp ex_float3(const FString& symbol, const FString& group, const FString& uid, float x, float y, float z, const FString& desc) {
		UMaterialExpressionVectorParameter* exp = NewObject<UMaterialExpressionVectorParameter>(this->p__mf);
		exp->ParameterName = FName(symbol);
		exp->Group = FName(group);
		exp->DefaultValue = FLinearColor(x, y, z, 1.0f);
		exp->Desc = desc;
		LexFromString(exp->ExpressionGUID, (*uid));
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 公開パラメーター(texture)を生成
	 * @param symbol シンボル名
	 * @param gorup グループ名
	 * @param uid パラメーターID
	 * @param src テクスチャーソースパス
	 * @param desc コメント
	 * @param sampler テクスチャーサンプル種別
	 * @return 変数
	 */
	FDevMFExp ex_texture(const FString& symbol, const FString& group, const FString& uid, const FString& src, const FString& desc, const FString& sampler) {
		UMaterialExpressionTextureObjectParameter* exp = NewObject<UMaterialExpressionTextureObjectParameter>(this->p__mf);
		exp->ParameterName = FName(symbol);
		exp->Group = FName(group);
		exp->Texture = TObjectPtr<UTexture>(this->p__assets->asset_of<UTexture>(FDevAssetPaths::to_path("image/texture", src)));
		exp->Desc = desc;
		exp->SamplerType = this->p__to_sampler(sampler);
		LexFromString(exp->ExpressionGUID, (*uid));
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// @deprecated
	// @Embed.python
	// def ex_curve(self, symbol: str, group: str, uid: str, easing: str, desc: str, alpha: MFExp) -> MFExp:
	// 	"""公開パラメーター(curve)を生成
	// 	Args:
	// 		symbol: シンボル名
	// 		gorup: グループ名
	// 		uid: パラメーターID
	// 		easing: イージングメソッド
	// 		desc: コメント
	// 		alpha: α値
	// 	Returns:
	// 		変数
	// 	Note:
	// 		```
	// 		* カーブアトラスは固定
	// 		* 返却値はRGBA(0番)に限定
	// 		* 他の公開パラメーターと違い、宣言と同時に使用するため、配置個所に注意
	// 		@deprecated 宣言と使用を分離できないため
	// 		```
	// 	"""
	// 	exp = NewObject(MaterialExpressionCurveAtlasRowParameter, self.__mf)
	// 	exp.on.ParameterName = Name(symbol)
	// 	exp.on.Group = Name(group)
	// 	exp.on.Curve = ObjectPtr[CurveLinearColor](self.__assets.on.resolve_of(CurveLinearColor, AssetPaths.to_easing_path(easing)))
	// 	exp.on.Atlas = ObjectPtr[CurveLinearColorAtlas](self.__assets.on.resolve_of(CurveLinearColorAtlas, AssetPaths.to_easing_path('hoge')))
	// 	exp.on.InputTime.Connect(alpha.index, alpha.exp)
	// 	exp.on.Desc = desc
	// 	LexFromString(exp.on.ExpressionGUID, uid.encode())
	// 	self.__append_exp(exp)
	// 	return MFExp(exp)
	// ----- 定数 -----
	public:
	/**
	 * リテラルを生成(bool)
	 * @param value 値
	 * @return bool
	 */
	FDevMFExp literal_b(bool value) {
		UMaterialExpressionStaticBool* exp = NewObject<UMaterialExpressionStaticBool>(this->p__mf);
		exp->Value = (int(value));
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * リテラルを生成(float)
	 * @param value 値
	 * @return float
	 */
	FDevMFExp literal_f(float value) {
		UMaterialExpressionConstant* exp = NewObject<UMaterialExpressionConstant>(this->p__mf);
		exp->R = value;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * リテラルを生成(float2)
	 * @param x 値
	 * @param y 値
	 * @return ベクトル(2次元)
	 */
	FDevMFExp literal_f2(float x, float y) {
		UMaterialExpressionConstant2Vector* exp = NewObject<UMaterialExpressionConstant2Vector>(this->p__mf);
		exp->R = x;
		exp->G = y;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * リテラルを生成(float3)
	 * @param x 値
	 * @param y 値
	 * @param z 値
	 * @return ベクトル(3次元)
	 */
	FDevMFExp literal_f3(float x, float y, float z) {
		UMaterialExpressionConstant3Vector* exp = NewObject<UMaterialExpressionConstant3Vector>(this->p__mf);
		exp->Constant = FLinearColor(x, y, z, 1.0f);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * リテラルを生成(float4)
	 * @param r 値
	 * @param g 値
	 * @param b 値
	 * @param a 値
	 * @return ベクトル(4次元)
	 */
	FDevMFExp literal_f4(float r, float g, float b, float a) {
		UMaterialExpressionConstant4Vector* exp = NewObject<UMaterialExpressionConstant4Vector>(this->p__mf);
		exp->Constant = FLinearColor(r, g, b, a);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- 四則演算 -----
	public:
	/**
	 * 演算(加算)を生成
	 * @param left 左オペランド
	 * @param right 右オペランド
	 * @return 結果
	 */
	FDevMFExp add(FDevMFExp left, FDevMFExp right) {
		return this->p__exp_bin<UMaterialExpressionAdd>(left, right);
	}
	public:
	/**
	 * 演算(減算)を生成
	 * @param left 左オペランド
	 * @param right 右オペランド
	 * @return 結果
	 */
	FDevMFExp sub(FDevMFExp left, FDevMFExp right) {
		return this->p__exp_bin<UMaterialExpressionSubtract>(left, right);
	}
	public:
	/**
	 * 演算(乗算)を生成
	 * @param left 左オペランド
	 * @param right 右オペランド
	 * @return 結果
	 */
	FDevMFExp mul(FDevMFExp left, FDevMFExp right) {
		return this->p__exp_bin<UMaterialExpressionMultiply>(left, right);
	}
	public:
	/**
	 * 演算(除算)を生成
	 * @param left 左オペランド
	 * @param right 右オペランド
	 * @return 結果
	 */
	FDevMFExp div(FDevMFExp left, FDevMFExp right) {
		return this->p__exp_bin<UMaterialExpressionDivide>(left, right);
	}
	public:
	/**
	 * 演算(余算)を生成
	 * @param left 左オペランド
	 * @param right 右オペランド
	 * @return 結果
	 */
	FDevMFExp mod(FDevMFExp left, FDevMFExp right) {
		return this->p__exp_bin<UMaterialExpressionFmod>(left, right);
	}
	public:
	/**
	 * 演算(1 - x)を生成
	 * @param value 値
	 * @return 結果
	 */
	FDevMFExp one_minus(FDevMFExp value) {
		return this->p__exp_unary<UMaterialExpressionOneMinus>(value);
	}
	// ----- 算術演算 -----
	public:
	/**
	 * 式(abs)を生成
	 * @param value 値
	 * @return 絶対値
	 */
	FDevMFExp abs(FDevMFExp value) {
		return this->p__exp_unary<UMaterialExpressionAbs>(value);
	}
	// @deprecated
	// def atan2(self, y: MFExp, x: MFExp) -> MFExp:
	// 	"""式(atan2)を生成
	// 	Args:
	// 		y: Y座標
	// 		x: X座標
	// 	Returns:
	// 		弧度(ラジアン)
	// 	Note:
	// 		@deprecated: C++で非公開のため利用不可
	// 	"""
	// 	exp = NewObject(MaterialExpressionArctangent2, self.__mf)
	// 	exp.on.Y.Connect(y.index, y.exp)
	// 	exp.on.X.Connect(x.index, x.exp)
	// 	self.__append_exp(exp)
	// 	return MFExp(exp)
	public:
	/**
	 * 式(clamp)を生成
	 * @param value 値
	 * @param minimum 下限値
	 * @param maximum 上限値
	 * @return クランプ後の値
	 * @note min/maxを初期値で利用する場合はsaturateを使用することを推奨
	 */
	FDevMFExp clamp(FDevMFExp value, FDevMFExp minimum, FDevMFExp maximum) {
		UMaterialExpressionClamp* exp = NewObject<UMaterialExpressionClamp>(this->p__mf);
		exp->Input.Connect(value.index, value.exp);
		exp->Min.Connect(minimum.index, minimum.exp);
		exp->Max.Connect(maximum.index, maximum.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(cos)を生成
	 * @param ratio 1周の割合
	 * @param period 1周の基数 (default = 1.0)
	 * @return 0 ~ 1
	 */
	FDevMFExp cos(FDevMFExp ratio, float period = 1.0f) {
		UMaterialExpressionCosine* exp = NewObject<UMaterialExpressionCosine>(this->p__mf);
		exp->Input.Connect(ratio.index, ratio.exp);
		exp->Period = period;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(floor)を生成
	 * @param value 値
	 * @return 整数部
	 */
	FDevMFExp floor(FDevMFExp value) {
		return this->p__exp_unary<UMaterialExpressionFloor>(value);
	}
	public:
	/**
	 * 式(length)を生成
	 * @param vector ベクトル
	 * @return ベクトルの長さ
	 */
	FDevMFExp length(FDevMFExp vector) {
		return this->p__exp_unary<UMaterialExpressionLength>(vector);
	}
	public:
	/**
	 * 式(lerp)を生成
	 * @param a 始点
	 * @param b 終点
	 * @param alpha α値
	 * @return 合成後の値
	 */
	FDevMFExp lerp(FDevMFExp a, FDevMFExp b, FDevMFExp alpha) {
		UMaterialExpressionLinearInterpolate* exp = NewObject<UMaterialExpressionLinearInterpolate>(this->p__mf);
		exp->A.Connect(a.index, a.exp);
		exp->B.Connect(b.index, b.exp);
		exp->Alpha.Connect(alpha.index, alpha.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(max)を生成
	 * @param a 値1
	 * @param b 値2
	 * @return 大きい方の値
	 */
	FDevMFExp max(FDevMFExp a, FDevMFExp b) {
		return this->p__exp_bin<UMaterialExpressionMax>(a, b);
	}
	public:
	/**
	 * 式(min)を生成
	 * @param a 値1
	 * @param b 値2
	 * @return 小さい方の値
	 */
	FDevMFExp min(FDevMFExp a, FDevMFExp b) {
		return this->p__exp_bin<UMaterialExpressionMin>(a, b);
	}
	public:
	/**
	 * 式(power)を生成
	 * @param value 値
	 * @param exponent 指数
	 * @return べき乗した値
	 */
	FDevMFExp power(FDevMFExp value, FDevMFExp exponent) {
		UMaterialExpressionPower* exp = NewObject<UMaterialExpressionPower>(this->p__mf);
		exp->Base.Connect(value.index, value.exp);
		exp->Exponent.Connect(exponent.index, exponent.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(saturate)を生成
	 * @param value 値
	 * @return 値(0 ~ 1)
	 * @note clamp(x, 0, 1)と数学的には等価。HLSL的に高速
	 */
	FDevMFExp saturate(FDevMFExp value) {
		return this->p__exp_unary<UMaterialExpressionSaturate>(value);
	}
	public:
	/**
	 * 式(sin)を生成
	 * @param ratio 1周の割合
	 * @param period 1周の基数 (default = 1.0)
	 * @return 0 ~ 1
	 */
	FDevMFExp sin(FDevMFExp ratio, float period = 1.0f) {
		UMaterialExpressionSine* exp = NewObject<UMaterialExpressionSine>(this->p__mf);
		exp->Input.Connect(ratio.index, ratio.exp);
		exp->Period = period;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(smoothstep)を生成
	 * @param minimum 下限値
	 * @param maximum 上限値
	 * @param value 値
	 * @return 0 ~ 1
	 */
	FDevMFExp smoothstep(FDevMFExp minimum, FDevMFExp maximum, FDevMFExp value) {
		UMaterialExpressionSmoothStep* exp = NewObject<UMaterialExpressionSmoothStep>(this->p__mf);
		exp->Min.Connect(minimum.index, minimum.exp);
		exp->Max.Connect(maximum.index, maximum.exp);
		exp->Value.Connect(value.index, value.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(step)を生成
	 * @param value 値
	 * @param threshold 閾値
	 * @return 0 or 1
	 */
	FDevMFExp step(FDevMFExp value, FDevMFExp threshold) {
		UMaterialExpressionStep* exp = NewObject<UMaterialExpressionStep>(this->p__mf);
		exp->Y.Connect(value.index, value.exp);
		exp->X.Connect(threshold.index, threshold.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(tan)を生成
	 * @param ratio 1周の割合
	 * @param period 1周の基数 (default = 1.0)
	 * @return 0 ~ 1
	 */
	FDevMFExp tan(FDevMFExp ratio, float period = 1.0f) {
		UMaterialExpressionTangent* exp = NewObject<UMaterialExpressionTangent>(this->p__mf);
		exp->Input.Connect(ratio.index, ratio.exp);
		exp->Period = period;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- ベクトル操作 -----
	public:
	/**
	 * 式(append)を生成
	 * @param value 元の値(float or ベクトル)
	 * @param x 追加する要素
	 * @return ベクトル(2次元)
	 */
	FDevMFExp append(FDevMFExp value, FDevMFExp x) {
		return this->p__exp_bin<UMaterialExpressionAppendVector>(value, x);
	}
	public:
	/**
	 * 式(cross)を生成
	 * @param a ベクトル1
	 * @param b ベクトル2
	 * @return 外積
	 */
	FDevMFExp cross(FDevMFExp a, FDevMFExp b) {
		return this->p__exp_bin<UMaterialExpressionCrossProduct>(a, b);
	}
	public:
	/**
	 * 式(dot)を生成
	 * @param a ベクトル1
	 * @param b ベクトル2
	 * @return 内積
	 */
	FDevMFExp dot(FDevMFExp a, FDevMFExp b) {
		return this->p__exp_bin<UMaterialExpressionDotProduct>(a, b);
	}
	public:
	/**
	 * 式(make_float3)を生成
	 * @param x X座標
	 * @param y Y座標
	 * @return ベクトル(2次元)
	 */
	FDevMFExp make_float2(FDevMFExp x, FDevMFExp y) {
		return this->p__exp_bin<UMaterialExpressionAppendVector>(x, y);
	}
	public:
	/**
	 * 式(make_float3)を生成
	 * @param x X座標
	 * @param y Y座標
	 * @param z Z座標
	 * @return ベクトル(3次元)
	 */
	FDevMFExp make_float3(FDevMFExp x, FDevMFExp y, FDevMFExp z) {
		FDevMFExp xy = this->p__exp_bin<UMaterialExpressionAppendVector>(x, y);
		return this->p__exp_bin<UMaterialExpressionAppendVector>(xy, z);
	}
	public:
	/**
	 * 式(make_float4)を生成
	 * @param x X座標
	 * @param y Y座標
	 * @param z Z座標
	 * @param w W座標
	 * @return ベクトル(4次元)
	 */
	FDevMFExp make_float4(FDevMFExp x, FDevMFExp y, FDevMFExp z, FDevMFExp w) {
		FDevMFExp xy = this->p__exp_bin<UMaterialExpressionAppendVector>(x, y);
		FDevMFExp xyz = this->p__exp_bin<UMaterialExpressionAppendVector>(xy, z);
		return this->p__exp_bin<UMaterialExpressionAppendVector>(xyz, w);
	}
	public:
	/**
	 * 式(mask)を生成
	 * @param value 値
	 * @param key キー名
	 * @return float or ベクトル
	 */
	FDevMFExp mask(FDevMFExp value, const FString& key) {
		UMaterialExpressionComponentMask* exp = NewObject<UMaterialExpressionComponentMask>(this->p__mf);
		exp->Input.Connect(value.index, value.exp);
		exp->R = FDevString::count(key, "x") > 0;
		exp->G = FDevString::count(key, "y") > 0;
		exp->B = FDevString::count(key, "z") > 0;
		exp->A = key == "w";
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(normalize)を生成
	 * @param vector ベクトル
	 * @return 単位ベクトル
	 */
	FDevMFExp normalize(FDevMFExp vector) {
		UMaterialExpressionNormalize* exp = NewObject<UMaterialExpressionNormalize>(this->p__mf);
		exp->VectorInput.Connect(vector.index, vector.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- カラー操作 -----
	public:
	/**
	 * HSV変換を生成
	 * @param rgb RGB
	 * @return HSV
	 */
	FDevMFExp rgb_to_hsv(FDevMFExp rgb) {
		return this->p__exp_unary<UMaterialExpressionRgbToHsv>(rgb);
	}
	public:
	/**
	 * RGB変換を生成
	 * @param hsv HSV
	 * @return RGB
	 */
	FDevMFExp hsv_to_rgb(FDevMFExp rgb) {
		return this->p__exp_unary<UMaterialExpressionHsvToRgb>(rgb);
	}
	// ----- テクスチャー操作 -----
	public:
	/**
	 * UV座標スクロールを生成
	 * @param uv UV座標
	 * @param speed スクロール速度
	 * @return UV座標
	 */
	FDevMFExp panner(FDevMFExp uv, FDevMFExp speed) {
		UMaterialExpressionPanner* exp = NewObject<UMaterialExpressionPanner>(this->p__mf);
		exp->Coordinate.Connect(uv.index, uv.exp);
		exp->Speed.Connect(speed.index, speed.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * UV座標を生成
	 * @param index UVインデックス
	 * @return UV座標
	 */
	FDevMFExp tex_coord(int index) {
		UMaterialExpressionTextureCoordinate* exp = NewObject<UMaterialExpressionTextureCoordinate>(this->p__mf);
		exp->CoordinateIndex = index;
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * テクスチャーオブジェクトを生成
	 * @param src テクスチャーソースパス
	 * @param sampler テクスチャーサンプル種別
	 * @return テクスチャー
	 */
	FDevMFExp texture(const FString& src, const FString& sampler) {
		UMaterialExpressionTextureObject* exp = NewObject<UMaterialExpressionTextureObject>(this->p__mf);
		exp->Texture = TObjectPtr<UTexture>(this->p__assets->asset_of<UTexture>(FDevAssetPaths::to_path("image/texture", src)));
		exp->SamplerType = this->p__to_sampler(sampler);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * テクスチャーサンプリングを生成
	 * @param texture テクスチャー
	 * @param uv UV座標 XXX 省略する方法を検討
	 * @param sampler テクスチャーサンプル種別
	 * @return RGBA
	 * @note 返却値はRGBA(5番)に限定
	 */
	FDevMFExp sample(FDevMFExp texture, FDevMFExp uv, const FString& sampler) {
		UMaterialExpressionTextureSample* exp = NewObject<UMaterialExpressionTextureSample>(this->p__mf);
		exp->TextureObject.Connect(texture.index, texture.exp);
		exp->Coordinates.Connect(uv.index, uv.exp);
		exp->SamplerType = this->p__to_sampler(sampler);
		this->p__append_exp(exp);
		return FDevMFExp(exp, 5);
	}
	// ----- ピクセルシェーダー -----
	public:
	/**
	 * 式(ddx)を生成
	 * @param value 値
	 * @return 勾配
	 */
	FDevMFExp ddx(FDevMFExp value) {
		UMaterialExpressionDDX* exp = NewObject<UMaterialExpressionDDX>(this->p__mf);
		exp->Value.Connect(value.index, value.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	public:
	/**
	 * 式(ddy)を生成
	 * @param value 値
	 * @return 勾配
	 */
	FDevMFExp ddy(FDevMFExp value) {
		UMaterialExpressionDDY* exp = NewObject<UMaterialExpressionDDY>(this->p__mf);
		exp->Value.Connect(value.index, value.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- 時間 -----
	public:
	/**
	 * 経過時間を生成
	 * @return 経過時間
	 */
	FDevMFExp time() {
		UMaterialExpressionTime* exp = NewObject<UMaterialExpressionTime>(this->p__mf);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- フロー制御 -----
	public:
	/**
	 * スイッチ構文を生成
	 * @param then 真の時の値
	 * @param reject 偽の時の値
	 * @param on 真偽値
	 * @return 結果
	 */
	FDevMFExp ternary(FDevMFExp then, FDevMFExp reject, FDevMFExp on) {
		UMaterialExpressionStaticSwitch* exp = NewObject<UMaterialExpressionStaticSwitch>(this->p__mf);
		exp->A.Connect(then.index, then.exp);
		exp->B.Connect(reject.index, reject.exp);
		exp->Value.Connect(on.index, on.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- 関数コール -----
	public:
	/**
	 * 関数コールを生成
	 * @param func_name マテリアル関数の名前
	 * @param args 引数リスト
	 * @return 戻り値のリスト
	 */
	FDevMFExp call(const FString& func_name, const TArray<FDevMFExp>& args) {
		UMaterialExpressionMaterialFunctionCall* exp = NewObject<UMaterialExpressionMaterialFunctionCall>(this->p__mf);
		// XXX 関数名の接頭辞をフォルダー名とする
		FString src = FString::Printf(TEXT("%s/%s"), *FDevString::split(func_name, "_")[0], *func_name);
		exp->SetMaterialFunction(this->p__assets->asset_of<UMaterialFunction>(FDevAssetPaths::to_path("material/func", src)));
		int index = 0;
		for (auto& arg : args) {
			exp->FunctionInputs[index].Input.Connect(arg.index, arg.exp);
			index++;
		}
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	// ----- ここまで -----
	private:
	/**
	 * テクスチャーサンプル(定数)に変換
	 * @param sampler テクスチャーサンプル(文字列)
	 * @return テクスチャーサンプル(定数)
	 */
	EMaterialSamplerType p__to_sampler(const FString& sampler) {
		TMap<FString, EMaterialSamplerType> to_sampler = {
			{"Color", EMaterialSamplerType::SAMPLERTYPE_Color},
			{"LinearColor", EMaterialSamplerType::SAMPLERTYPE_LinearColor},
			{"LinearGrayscale", EMaterialSamplerType::SAMPLERTYPE_LinearGrayscale},
		};
		return to_sampler[sampler];
	}
	private:
	/**
	 * 式(単項)を生成
	 * @param unary_type 単項式の型
	 * @param value 値
	 * @return 結果
	 */
	template<typename T_Unary>
	FDevMFExp p__exp_unary(FDevMFExp value) {
		T_Unary* exp = NewObject<T_Unary>(this->p__mf);
		exp->Input.Connect(value.index, value.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	private:
	/**
	 * 式(2項)を生成
	 * @param bin_type 2項式の型
	 * @param a 値1
	 * @param b 値2
	 * @return 結果
	 */
	template<typename T_Bin>
	FDevMFExp p__exp_bin(FDevMFExp a, FDevMFExp b) {
		T_Bin* exp = NewObject<T_Bin>(this->p__mf);
		exp->A.Connect(a.index, a.exp);
		exp->B.Connect(b.index, b.exp);
		this->p__append_exp(exp);
		return FDevMFExp(exp);
	}
	private:
	/**
	 *
	 * @return マテリアル関数式の数
	 */
	int p__count_of_exps() {
		return this->p__mf->GetEditorOnlyData()->ExpressionCollection.Expressions.Num();
	}
	private:
	/**
	 * uclass: カウント対象の式の型情報
	 * @return 対象の式の数
	 */
	int p__count_for_exps(UClass* uclass) {
		int count = 0;
		for (auto exp : this->p__mf->GetEditorOnlyData()->ExpressionCollection.Expressions) {
			if (exp->IsA(uclass)) {
				count += 1;
			}
		}
		return count;
	}
	private:
	/**
	 *
	 * @return ユニークID(引数)
	 */
	FString p__publish_id_for_param() {
		return this->p__publish_id(FString("A") + LexToString(this->p__count_for_exps(UMaterialExpressionFunctionInput::StaticClass())));
	}
	private:
	/**
	 *
	 * @return ユニークID(戻り値)
	 */
	FString p__publish_id_for_returns() {
		return this->p__publish_id(FString("B") + LexToString(this->p__count_for_exps(UMaterialExpressionFunctionOutput::StaticClass())));
	}
	private:
	/**
	 *
	 * @return ユニークID(公開パラメーター)
	 * @note @deprecated 未使用
	 */
	FString p__publish_id_for_export() {
		return this->p__publish_id(FString("C") + LexToString(this->p__count_for_exps(UMaterialExpressionParameter::StaticClass())));
	}
	private:
	/**
	 *
	 * @return ユニークID(変数)
	 */
	FString p__publish_id_for_var() {
		return this->p__publish_id(FString("D") + LexToString(this->p__count_for_exps(UMaterialExpressionNamedRerouteDeclaration::StaticClass())));
	}
	private:
	/**
	 * マテリアル関数内でユニークなIDを発行
	 * @param id_str ID
	 * @return ID
	 * @note
	 * ```
	 * * 引数/戻り値/公開パラメーターに対して使用
	 * * IDは関数内でユニークであれば良く、別の関数のIDとの重複を気にする必要は無い
	 * * 基本的に対象の式のインデックスを基準とするため、インデックスが変わると既存の接続が切れてしまう点に注意
	 * ```
	 */
	FString p__publish_id(const FString& id_str) {
		return this->p__io_base_id.Mid(0, 32 - id_str.Len()) + id_str;
	}
	private:
	/**
	 * マテリアル関数に式を追加
	 * @param exp マテリアル関数式
	 */
	void p__append_exp(UMaterialExpression* exp) {
		// XXX ノードが重ならない様に適当に配置
		if (this->p__line_break(exp)) {
			this->p__align.line_break();
		} else if (this->p__line_fold(exp)) {
			this->p__align.line_fold();
		} else if (this->p__mf->GetEditorOnlyData()->ExpressionCollection.Expressions.Num() > 0) {
			this->p__align.add_row();
		}
		FIntVector2 pos = this->p__align.pos();
		exp->MaterialExpressionEditorX = pos.X;
		exp->MaterialExpressionEditorY = pos.Y;
		this->p__mf->GetEditorOnlyData()->ExpressionCollection.AddExpression(exp);
	}
	private:
	/**
	 * 式の登録状況から改行を判定
	 * @param curr 登録予定のマテリアル関数式
	 * @return True = 改行
	 */
	bool p__line_break(UMaterialExpression* curr) {
		int total = this->p__mf->GetEditorOnlyData()->ExpressionCollection.Expressions.Num();
		if (total == 0) {
			return false;
		}
		UMaterialExpression* prev = this->p__mf->GetEditorOnlyData()->ExpressionCollection.Expressions[total - 1];
		if (!(prev->IsA(UMaterialExpressionFunctionInput::StaticClass()) || prev->IsA(UMaterialExpressionNamedRerouteDeclaration::StaticClass()) || prev->IsA(UMaterialExpressionParameter::StaticClass()))) {
			return false;
		}
		if (curr->IsA(UMaterialExpressionFunctionInput::StaticClass()) || curr->IsA(UMaterialExpressionNamedRerouteDeclaration::StaticClass()) || curr->IsA(UMaterialExpressionParameter::StaticClass())) {
			return false;
		}
		return true;
	}
	private:
	/**
	 * 式の登録状況から行内の改行を判定
	 * @param curr 登録予定のマテリアル関数式
	 * @return True = 行内の改行
	 */
	bool p__line_fold(UMaterialExpression* curr) {
		int total = this->p__mf->GetEditorOnlyData()->ExpressionCollection.Expressions.Num();
		if (total == 0) {
			return false;
		}
		UMaterialExpression* prev = this->p__mf->GetEditorOnlyData()->ExpressionCollection.Expressions[total - 1];
		if (prev->IsA(UMaterialExpressionNamedRerouteUsage::StaticClass()) && curr->IsA(UMaterialExpressionNamedRerouteUsage::StaticClass())) {
			return true;
		} else if (prev->IsA(UMaterialExpressionNamedRerouteDeclaration::StaticClass()) && curr->IsA(UMaterialExpressionNamedRerouteDeclaration::StaticClass())) {
			return true;
		}
		return false;
	}
};
