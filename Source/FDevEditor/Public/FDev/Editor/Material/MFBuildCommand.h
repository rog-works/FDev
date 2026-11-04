// @tranp.meta: {"version":"0.9.19","module":{"hash":"47a26de0d6c7a35eee64305db6db2b32","path":"FDev.Editor.Material.MFBuildCommand"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Math/MathFwd.h"
#include "Materials/MaterialExpressionTextureSample.h"
#include "FDev/Editor/Material/MFBuilder.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Lang/Json/Json.h"
#include "FDev/Main/Core/Core.h"
// #include "enum.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/error.h"
/**
 * ビルドコマンド
 */
class FDevMFBuildCommand {
	/**
	 * コマンド種別
	 */
	public: enum class Roles {
		Bool = 0,
		Integer = 1,
		Number = 2,
		String = 3,
		Exp = 4,
		Function = 5,
	};
	public: FFDevJson data;
	public: Roles role;
	public:
	/**
	 * インスタンスを生成
	 * @param data 定義データ
	 * @param role_is_function True = 関数, False = 自動判別
	 */
	FDevMFBuildCommand(FFDevJson data, bool role_is_function = false) : data(data), role(role_is_function ? FDevMFBuildCommand::Roles::Function : FDevMFBuildCommand::analyze_role(data)) {}
	public:
	/**
	 *
	 * @return コマンド種別
	 * @note 関数以外の判別に利用
	 */
	static Roles analyze_role(FFDevJson data) {
		if (data.is_scalar()) {
			if (data.is_bool()) {
				return FDevMFBuildCommand::Roles::Bool;
			} else if (data.is_int()) {
				return FDevMFBuildCommand::Roles::Integer;
			} else if (data.is_float()) {
				return FDevMFBuildCommand::Roles::Number;
			} else {
				return FDevMFBuildCommand::Roles::String;
			}
		} else {
			return FDevMFBuildCommand::Roles::Exp;
		}
	}
	public:
	/**
	 *
	 * @return True = スカラー型
	 */
	bool is_scalar() {
		return this->data.is_scalar();
	}
	public:
	/**
	 *
	 * @return 関数名/コマンド名
	 */
	FString name() {
		if (this->role == FDevMFBuildCommand::Roles::Function) {
			return this->data["name"].as_string();
		} else if (this->role == FDevMFBuildCommand::Roles::Exp) {
			return this->data.key_at(0);
		} else {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::name()"), *(this->data).ToString(), this->role));
		}
	}
	public:
	/**
	 *
	 * @return コメント(関数)
	 */
	FString desc() {
		if (this->role != FDevMFBuildCommand::Roles::Function) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s, %d"), TEXT("FDevMFBuildCommand::desc()"), *(this->data).ToString(), this->role));
		}
		return this->data["desc"].as_string();
	}
	public:
	/**
	 *
	 * @return ハッシュ(関数)
	 */
	FString hash() {
		if (this->role != FDevMFBuildCommand::Roles::Function) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s, %d"), TEXT("FDevMFBuildCommand::hash()"), *(this->data).ToString(), this->role));
		}
		return this->data["hash"].as_string();
	}
	public:
	/**
	 *
	 * @return 仮引数リスト(関数)
	 */
	TArray<FDevMFBuildCommand> params() {
		if (this->role != FDevMFBuildCommand::Roles::Function) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s, %d"), TEXT("FDevMFBuildCommand::params()"), *(this->data).ToString(), this->role));
		}
		return [&]() -> TArray<FDevMFBuildCommand> {
			TArray<FDevMFBuildCommand> __ret;
			for (auto& under : this->data["params"].entries()) {
				__ret.Add(FDevMFBuildCommand(under));
			}
			return __ret;
		}();
	}
	public:
	/**
	 *
	 * @return ステートメントリスト(関数)
	 */
	TArray<FDevMFBuildCommand> statements() {
		if (this->role != FDevMFBuildCommand::Roles::Function) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s, %d"), TEXT("FDevMFBuildCommand::statements()"), *(this->data).ToString(), this->role));
		}
		return [&]() -> TArray<FDevMFBuildCommand> {
			TArray<FDevMFBuildCommand> __ret;
			for (auto& under : this->data["statements"].entries()) {
				__ret.Add(FDevMFBuildCommand(under));
			}
			return __ret;
		}();
	}
	public:
	/**
	 *
	 * @return True = 有効
	 */
	bool as_bool() {
		if (!this->is_scalar()) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::as_bool()"), *(this->data).ToString(), this->role));
		}
		return this->data.as_bool();
	}
	public:
	/**
	 *
	 * @return シンボル名/コメント
	 */
	FString as_string() {
		if (!this->is_scalar()) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::as_string()"), *(this->data).ToString(), this->role));
		}
		return this->data.as_string();
	}
	public:
	/**
	 *
	 * @return 定数値
	 */
	float as_float() {
		if (!this->is_scalar()) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::as_float()"), *(this->data).ToString(), this->role));
		}
		if (this->role == FDevMFBuildCommand::Roles::String && this->as_string() == "PI") {
			return PI;
		} else {
			return this->data.as_float();
		}
	}
	public:
	/**
	 *
	 * @return 関数の戻り値の使用インデックス
	 */
	int as_int() {
		if (!this->is_scalar()) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::as_int()"), *(this->data).ToString(), this->role));
		}
		return this->data.as_int();
	}
	public:
	/**
	 *
	 * @return マテリアル関数式の実引数リスト
	 */
	TArray<FDevMFBuildCommand> args() {
		if (this->role != FDevMFBuildCommand::Roles::Exp) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::args()"), *(this->data).ToString(), this->role));
		}
		return [&]() -> TArray<FDevMFBuildCommand> {
			TArray<FDevMFBuildCommand> __ret;
			for (auto& under : this->data.at(0).entries()) {
				__ret.Add(FDevMFBuildCommand(under));
			}
			return __ret;
		}();
	}
};
/**
 * ビルドコマンドランナー
 */
class FDevMFBuildCommandRunner {
	public:
	/**
	 * ビルドコマンドをパース
	 * @return ビルドコマンド(関数)リスト
	 */
	static TMap<FString, FDevMFBuildCommand> parse(FFDevJson data) {
		return [&]() -> TMap<FString, FDevMFBuildCommand> {
			TMap<FString, FDevMFBuildCommand> __ret;
			for (auto& src : data.keys()) {
				__ret.Add(src, FDevMFBuildCommand(data[src], true));
			}
			return __ret;
		}();
	}
	public:
	/**
	 * ビルダーに対してコマンドを実行(関数)
	 * @param builder マテリアル関数ビルダー
	 * @param func ビルドコマンド(関数)
	 */
	static void run(FDevMFBuilder* builder, FDevMFBuildCommand func) {
		builder->clear();
		builder->description(func.desc());
		for (auto& param : func.params()) {
			FDevMFBuildCommandRunner::run_command(builder, param);
		}
		for (auto& statement : func.statements()) {
			FDevMFBuildCommandRunner::run_command(builder, statement);
		}
	}
	public:
	/**
	 * ビルダーに対してコマンドを実行
	 * @param builder マテリアル関数ビルダー
	 * @param command ビルドコマンド
	 */
	static FDevMFExp run_command(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		if (command.role == FDevMFBuildCommand::Roles::Bool) {
			return builder->literal_b(command.as_bool());
		} else if (command.role == FDevMFBuildCommand::Roles::Number) {
			return builder->literal_f(command.as_float());
		} else if (command.role == FDevMFBuildCommand::Roles::String) {
			return builder->var_ref(command.as_string());
		}
		FString name = command.name();
		TArray<FDevMFBuildCommand> args = command.args();
		if (name == "get") {

		} else if (name == "var") {

		} else {

		}
		if (name == "param") {
			return builder->param(args[0].as_string(), args[1].as_string(), FDevMFBuildCommandRunner::run_command(builder, args[2]), args[3].as_string());
		} else if (name == "returns") {
			return builder->returns(args[0].as_string(), FDevMFBuildCommandRunner::run_command(builder, args[1]), args[2].as_string());
		} else if (name == "var") {
			return builder->var(args[0].as_string(), FDevMFBuildCommandRunner::run_command(builder, args[1]));
		} else if (name == "vars") {
			return builder->vars([&]() -> TArray<FString> {
				TArray<FString> __ret;
				for (auto index = 0; index < args.Num() - 1; index++) {
					__ret.Add(args[index].as_string());
				}
				return __ret;
			}(), FDevMFBuildCommandRunner::run_command(builder, args[args.Num() - 1]));
		} else if (name == "get") {
			return FDevMFBuildCommandRunner::run_command(builder, args[0]).new_index(args[1].as_int());
		} else if (name == "ex_bool") {
			return builder->ex_bool(args[0].as_string(), args[1].as_string(), args[2].as_string(), args[3].as_bool(), args[4].as_string());
		} else if (name == "ex_float") {
			return builder->ex_float(args[0].as_string(), args[1].as_string(), args[2].as_string(), args[3].as_float(), args[4].as_string(), args[5].as_float(), args[6].as_float());
		} else if (name == "ex_float3") {
			return builder->ex_float3(args[0].as_string(), args[1].as_string(), args[2].as_string(), args[3].as_float(), args[4].as_float(), args[5].as_float(), args[6].as_string());
		} else if (name == "ex_texture") {
			return builder->ex_texture(args[0].as_string(), args[1].as_string(), args[2].as_string(), args[3].as_string(), args[4].as_string(), args.Num() == 6 ? args[5].as_string() : "Color");
		} else if (name == "pi") {
			return builder->literal_f(PI);
		} else if (name == "float2") {
			return builder->literal_f2(args[0].as_float(), args[1].as_float());
		} else if (name == "float3") {
			return builder->literal_f3(args[0].as_float(), args[1].as_float(), args[2].as_float());
		} else if (name == "float4") {
			return builder->literal_f4(args[0].as_float(), args[1].as_float(), args[2].as_float(), args[3].as_float());
		} else if (name == "add") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->add(values.Get<0>(), values.Get<1>());
		} else if (name == "sub") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->sub(values.Get<0>(), values.Get<1>());
		} else if (name == "mul") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->mul(values.Get<0>(), values.Get<1>());
		} else if (name == "div") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->div(values.Get<0>(), values.Get<1>());
		} else if (name == "mod") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->mod(values.Get<0>(), values.Get<1>());
		} else if (name == "one_minus") {
			return builder->one_minus(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "abs") {
			return builder->abs(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "clamp") {
			TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1]), FDevMFBuildCommandRunner::run_command(builder, args[2])};
			return builder->clamp(values.Get<0>(), values.Get<1>(), values.Get<2>());
		} else if (name == "cos") {
			return builder->cos(FDevMFBuildCommandRunner::run_command(builder, args[0]), args.Num() == 2 ? args[1].as_float() : 1.0f);
		} else if (name == "floor") {
			return builder->floor(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "length") {
			return builder->length(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "lerp") {
			TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1]), FDevMFBuildCommandRunner::run_command(builder, args[2])};
			return builder->lerp(values.Get<0>(), values.Get<1>(), values.Get<2>());
		} else if (name == "max") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->max(values.Get<0>(), values.Get<1>());
		} else if (name == "min") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->min(values.Get<0>(), values.Get<1>());
		} else if (name == "power") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->power(values.Get<0>(), values.Get<1>());
		} else if (name == "sin") {
			return builder->sin(FDevMFBuildCommandRunner::run_command(builder, args[0]), args.Num() == 2 ? args[1].as_float() : 1.0f);
		} else if (name == "smoothstep") {
			TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1]), FDevMFBuildCommandRunner::run_command(builder, args[2])};
			return builder->smoothstep(values.Get<0>(), values.Get<1>(), values.Get<2>());
		} else if (name == "step") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->step(values.Get<0>(), values.Get<1>());
		} else if (name == "tan") {
			return builder->tan(FDevMFBuildCommandRunner::run_command(builder, args[0]), args.Num() == 2 ? args[1].as_float() : 1.0f);
		} else if (name == "saturate") {
			return builder->saturate(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "append") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->append(values.Get<0>(), values.Get<1>());
		} else if (name == "cross") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->cross(values.Get<0>(), values.Get<1>());
		} else if (name == "dot") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->dot(values.Get<0>(), values.Get<1>());
		} else if (name == "make_float2") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->make_float2(values.Get<0>(), values.Get<1>());
		} else if (name == "make_float3") {
			TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1]), FDevMFBuildCommandRunner::run_command(builder, args[2])};
			return builder->make_float3(values.Get<0>(), values.Get<1>(), values.Get<2>());
		} else if (name == "make_float4") {
			TTuple<FDevMFExp, FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1]), FDevMFBuildCommandRunner::run_command(builder, args[2]), FDevMFBuildCommandRunner::run_command(builder, args[3])};
			return builder->make_float4(values.Get<0>(), values.Get<1>(), values.Get<2>(), values.Get<3>());
		} else if (name == "mask") {
			return builder->mask(FDevMFBuildCommandRunner::run_command(builder, args[0]), args[1].as_string());
		} else if (name == "normalize") {
			return builder->normalize(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "rgb_to_hsv") {
			return builder->rgb_to_hsv(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "hsv_to_rgb") {
			return builder->hsv_to_rgb(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "panner") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->panner(values.Get<0>(), values.Get<1>());
		} else if (name == "tex_coord") {
			return builder->tex_coord(args[0].as_int());
		} else if (name == "texture") {
			return builder->texture(args[0].as_string(), args.Num() == 2 ? args[1].as_string() : "Color");
		} else if (name == "time") {
			return builder->time();
		} else if (name == "sample") {
			TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1])};
			return builder->sample(values.Get<0>(), values.Get<1>(), args.Num() == 3 ? args[2].as_string() : "Color");
		} else if (name == "ddx") {
			return builder->ddx(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "ddy") {
			return builder->ddy(FDevMFBuildCommandRunner::run_command(builder, args[0]));
		} else if (name == "const_by") {
			return builder->const_by(args[0].as_string());
		} else if (name == "ternary") {
			TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::run_command(builder, args[0]), FDevMFBuildCommandRunner::run_command(builder, args[1]), FDevMFBuildCommandRunner::run_command(builder, args[2])};
			return builder->ternary(values.Get<0>(), values.Get<1>(), values.Get<2>());
		} else {
			return builder->call(name, [&]() -> TArray<FDevMFExp> {
				TArray<FDevMFExp> __ret;
				for (auto index = 0; index < args.Num(); index++) {
					__ret.Add(FDevMFBuildCommandRunner::run_command(builder, args[index]));
				}
				return __ret;
			}());
		}
	}
};
