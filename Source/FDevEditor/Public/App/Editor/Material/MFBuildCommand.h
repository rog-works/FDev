// @tranp.meta: {"version":"0.9.25","module":{"hash":"717e8002b5b811a7646c4bc0717b9f63","path":"App.Editor.Material.MFBuildCommand"},"transpiler":{"version":"0.9.12","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Math/MathFwd.h"
#include "Materials/MaterialExpressionTextureSample.h"
#include "App/Editor/Material/MFBuilder.h"
#include "App/Main/Core/Lang/Json/Json.h"
#include "App/Main/Core/Logs.h"
#include "App/Main/Core/Core.h"
// #include "enum.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/cpp/function.h"
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
	 */
	FDevMFBuildCommand(FFDevJson data) : data(data), role(FDevMFBuildCommand::analyze_role(data)) {}
	public:
	/**
	 *
	 * @return コマンド種別
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
		} else if (data.has_key("statements")) {
			return FDevMFBuildCommand::Roles::Function;
		} else {
			return FDevMFBuildCommand::Roles::Exp;
		}
	}
	public:
	/**
	 *
	 * @return ハッシュ(関数) @immutable
	 */
	const FString& hash() {
		if (this->role != FDevMFBuildCommand::Roles::Function) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s, %d"), TEXT("FDevMFBuildCommand::hash()"), *(this->data).ToString(), this->role));
		}
		return this->data["hash"].as_string();
	}
	// region 関数
	public:
	/**
	 *
	 * @return コメント(関数) @immutable
	 */
	const FString& desc() {
		if (this->role != FDevMFBuildCommand::Roles::Function) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s, %d"), TEXT("FDevMFBuildCommand::desc()"), *(this->data).ToString(), this->role));
		}
		return this->data["desc"].as_string();
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
			TArray<FDevMFBuildCommand> l_ret;
			for (auto& under : this->data["params"].entries()) {
				l_ret.Add(FDevMFBuildCommand(under));
			}
			return l_ret;
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
			TArray<FDevMFBuildCommand> l_ret;
			for (auto& under : this->data["statements"].entries()) {
				l_ret.Add(FDevMFBuildCommand(under));
			}
			return l_ret;
		}();
	}
	public:
	/**
	 *
	 * @return 出力(JSON)
	 */
	FFDevJson output() {
		if (this->role != FDevMFBuildCommand::Roles::Function) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s, %d"), TEXT("FDevMFBuildCommand::desc()"), *(this->data).ToString(), this->role));
		}
		return this->data["output"];
	}
	// endregion
	// region 名前
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
	// endregion
	// region 値
	public:
	/**
	 *
	 * @return True = 有効
	 */
	bool as_bool() {
		if (!this->data.is_bool()) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::as_bool()"), *(this->data).ToString(), this->role));
		}
		return this->data.as_bool();
	}
	public:
	/**
	 *
	 * @return シンボル名/コメント @immutable
	 */
	const FString& as_string() {
		if (!this->data.is_string()) {
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
		if (!this->data.is_float()) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::as_float()"), *(this->data).ToString(), this->role));
		}
		return this->data.as_float();
	}
	public:
	/**
	 *
	 * @return 関数の戻り値の使用インデックス
	 */
	int as_int() {
		if (!this->data.is_int()) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::as_int()"), *(this->data).ToString(), this->role));
		}
		return this->data.as_int();
	}
	// endregion
	// region 引数
	public:
	/**
	 *
	 * @return マテリアル関数式の実引数の数
	 */
	int arg_num() {
		if (this->role != FDevMFBuildCommand::Roles::Exp) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::arg_num()"), *(this->data).ToString(), this->role));
		}
		return this->data.at(0).length();
	}
	public:
	/**
	 *
	 * @return マテリアル関数式の実引数
	 */
	FDevMFBuildCommand arg_at(int index) {
		if (this->role != FDevMFBuildCommand::Roles::Exp) {
			throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %d"), TEXT("FDevMFBuildCommand::arg_at"), *(this->data).ToString(), this->role));
		}
		return FDevMFBuildCommand(this->data.at(0).at(index));
	}
	// endregion
};
/**
 * ビルドコマンドランナー
 */
class FDevMFBuildCommandRunner {
	public:
	/**
	 * ビルドコマンドをパース
	 * @return ビルドコマンドリスト(関数/マテリアル)
	 */
	static TMap<FString, FDevMFBuildCommand> parse(FFDevJson data) {
		return [&]() -> TMap<FString, FDevMFBuildCommand> {
			TMap<FString, FDevMFBuildCommand> l_ret;
			for (auto& src : data.keys()) {
				l_ret.Add(src, FDevMFBuildCommand(data[src]));
			}
			return l_ret;
		}();
	}
	public:
	/**
	 * アセットを構築(マテリアル関数)
	 * @param builder マテリアル関数ビルダー
	 * @param entry ビルドコマンド(関数)
	 */
	static void build_mf(FDevMFBuilder* builder, FDevMFBuildCommand entry) {
		builder->clear();
		builder->description(entry.desc());
		for (auto& param : entry.params()) {
			FDevMFBuildCommandRunner::p__emit_command(builder, param);
		}
		for (auto& statement : entry.statements()) {
			FDevMFBuildCommandRunner::p__emit_command(builder, statement);
		}
	}
	public:
	/**
	 * アセットを構築(マテリアル)
	 * @param builder マテリアル関数ビルダー
	 * @param entry ビルドコマンド(マテリアル)
	 */
	static void build_material(FDevMFBuilder* builder, FDevMFBuildCommand entry) {
		builder->clear();
		for (auto& statement : entry.statements()) {
			FDevMFBuildCommandRunner::p__emit_command(builder, statement);
		}
		builder->rebuild_material();
	}
	private:
	/**
	 * ビルダーに対してコマンドを実行
	 * @param builder マテリアル関数ビルダー
	 * @param command ビルドコマンド
	 * @return 式
	 */
	static FDevMFExp p__emit_command(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		FDevMFBuildCommandRunner::p__debug_log(command);
		if (command.role == FDevMFBuildCommand::Roles::Bool) {
			return FDevMFBuildCommandRunner::on_bool(builder, command);
		} else if (command.role == FDevMFBuildCommand::Roles::Number) {
			return FDevMFBuildCommandRunner::on_float(builder, command);
		} else if (command.role == FDevMFBuildCommand::Roles::String) {
			return FDevMFBuildCommandRunner::on_var_ref(builder, command);
		} else if (command.name() == "get") {
			return FDevMFBuildCommandRunner::on_get(builder, command);
		} else {
			return FDevMFBuildCommandRunner::p__emit_exp(builder, command);
		}
	}
	private:
	/**
	 * 式コマンドを実行
	 * @param builder マテリアル関数ビルダー
	 * @param command ビルドコマンド
	 * @return 式
	 * @note XXX on_bool/on_float/on_get/on_callは特殊化によりhandlersに含まれない
	 */
	static FDevMFExp p__emit_exp(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		static TMap<FString, FDevMFExp(*)(FDevMFBuilder*, FDevMFBuildCommand)> handlers = {
			{FString("on_param").Mid(3, FString("on_param").Len() - (3)), &FDevMFBuildCommandRunner::on_param},
			{FString("on_returns").Mid(3, FString("on_returns").Len() - (3)), &FDevMFBuildCommandRunner::on_returns},
			{FString("on_schema_domain").Mid(3, FString("on_schema_domain").Len() - (3)), &FDevMFBuildCommandRunner::on_schema_domain},
			{FString("on_schema_blend").Mid(3, FString("on_schema_blend").Len() - (3)), &FDevMFBuildCommandRunner::on_schema_blend},
			{FString("on_schema_shading").Mid(3, FString("on_schema_shading").Len() - (3)), &FDevMFBuildCommandRunner::on_schema_shading},
			{FString("on_schema_option").Mid(3, FString("on_schema_option").Len() - (3)), &FDevMFBuildCommandRunner::on_schema_option},
			{FString("on_output_emissive_color").Mid(3, FString("on_output_emissive_color").Len() - (3)), &FDevMFBuildCommandRunner::on_output_emissive_color},
			{FString("on_output_opacity").Mid(3, FString("on_output_opacity").Len() - (3)), &FDevMFBuildCommandRunner::on_output_opacity},
			{FString("on_var").Mid(3, FString("on_var").Len() - (3)), &FDevMFBuildCommandRunner::on_var},
			{FString("on_vars").Mid(3, FString("on_vars").Len() - (3)), &FDevMFBuildCommandRunner::on_vars},
			{FString("on_ex_bool").Mid(3, FString("on_ex_bool").Len() - (3)), &FDevMFBuildCommandRunner::on_ex_bool},
			{FString("on_ex_float").Mid(3, FString("on_ex_float").Len() - (3)), &FDevMFBuildCommandRunner::on_ex_float},
			{FString("on_ex_float3").Mid(3, FString("on_ex_float3").Len() - (3)), &FDevMFBuildCommandRunner::on_ex_float3},
			{FString("on_ex_texture").Mid(3, FString("on_ex_texture").Len() - (3)), &FDevMFBuildCommandRunner::on_ex_texture},
			{FString("on_pi").Mid(3, FString("on_pi").Len() - (3)), &FDevMFBuildCommandRunner::on_pi},
			{FString("on_float2").Mid(3, FString("on_float2").Len() - (3)), &FDevMFBuildCommandRunner::on_float2},
			{FString("on_float3").Mid(3, FString("on_float3").Len() - (3)), &FDevMFBuildCommandRunner::on_float3},
			{FString("on_float4").Mid(3, FString("on_float4").Len() - (3)), &FDevMFBuildCommandRunner::on_float4},
			{FString("on_add").Mid(3, FString("on_add").Len() - (3)), &FDevMFBuildCommandRunner::on_add},
			{FString("on_sub").Mid(3, FString("on_sub").Len() - (3)), &FDevMFBuildCommandRunner::on_sub},
			{FString("on_mul").Mid(3, FString("on_mul").Len() - (3)), &FDevMFBuildCommandRunner::on_mul},
			{FString("on_div").Mid(3, FString("on_div").Len() - (3)), &FDevMFBuildCommandRunner::on_div},
			{FString("on_mod").Mid(3, FString("on_mod").Len() - (3)), &FDevMFBuildCommandRunner::on_mod},
			{FString("on_one_minus").Mid(3, FString("on_one_minus").Len() - (3)), &FDevMFBuildCommandRunner::on_one_minus},
			{FString("on_abs").Mid(3, FString("on_abs").Len() - (3)), &FDevMFBuildCommandRunner::on_abs},
			{FString("on_power").Mid(3, FString("on_power").Len() - (3)), &FDevMFBuildCommandRunner::on_power},
			{FString("on_step").Mid(3, FString("on_step").Len() - (3)), &FDevMFBuildCommandRunner::on_step},
			{FString("on_lerp").Mid(3, FString("on_lerp").Len() - (3)), &FDevMFBuildCommandRunner::on_lerp},
			{FString("on_smoothstep").Mid(3, FString("on_smoothstep").Len() - (3)), &FDevMFBuildCommandRunner::on_smoothstep},
			{FString("on_clamp").Mid(3, FString("on_clamp").Len() - (3)), &FDevMFBuildCommandRunner::on_clamp},
			{FString("on_floor").Mid(3, FString("on_floor").Len() - (3)), &FDevMFBuildCommandRunner::on_floor},
			{FString("on_max").Mid(3, FString("on_max").Len() - (3)), &FDevMFBuildCommandRunner::on_max},
			{FString("on_min").Mid(3, FString("on_min").Len() - (3)), &FDevMFBuildCommandRunner::on_min},
			{FString("on_saturate").Mid(3, FString("on_saturate").Len() - (3)), &FDevMFBuildCommandRunner::on_saturate},
			{FString("on_cos").Mid(3, FString("on_cos").Len() - (3)), &FDevMFBuildCommandRunner::on_cos},
			{FString("on_sin").Mid(3, FString("on_sin").Len() - (3)), &FDevMFBuildCommandRunner::on_sin},
			{FString("on_tan").Mid(3, FString("on_tan").Len() - (3)), &FDevMFBuildCommandRunner::on_tan},
			{FString("on_cross").Mid(3, FString("on_cross").Len() - (3)), &FDevMFBuildCommandRunner::on_cross},
			{FString("on_dot").Mid(3, FString("on_dot").Len() - (3)), &FDevMFBuildCommandRunner::on_dot},
			{FString("on_length").Mid(3, FString("on_length").Len() - (3)), &FDevMFBuildCommandRunner::on_length},
			{FString("on_normalize").Mid(3, FString("on_normalize").Len() - (3)), &FDevMFBuildCommandRunner::on_normalize},
			{FString("on_append").Mid(3, FString("on_append").Len() - (3)), &FDevMFBuildCommandRunner::on_append},
			{FString("on_make_float2").Mid(3, FString("on_make_float2").Len() - (3)), &FDevMFBuildCommandRunner::on_make_float2},
			{FString("on_make_float3").Mid(3, FString("on_make_float3").Len() - (3)), &FDevMFBuildCommandRunner::on_make_float3},
			{FString("on_make_float4").Mid(3, FString("on_make_float4").Len() - (3)), &FDevMFBuildCommandRunner::on_make_float4},
			{FString("on_mask").Mid(3, FString("on_mask").Len() - (3)), &FDevMFBuildCommandRunner::on_mask},
			{FString("on_rgb_to_hsv").Mid(3, FString("on_rgb_to_hsv").Len() - (3)), &FDevMFBuildCommandRunner::on_rgb_to_hsv},
			{FString("on_hsv_to_rgb").Mid(3, FString("on_hsv_to_rgb").Len() - (3)), &FDevMFBuildCommandRunner::on_hsv_to_rgb},
			{FString("on_panner").Mid(3, FString("on_panner").Len() - (3)), &FDevMFBuildCommandRunner::on_panner},
			{FString("on_tex_coord").Mid(3, FString("on_tex_coord").Len() - (3)), &FDevMFBuildCommandRunner::on_tex_coord},
			{FString("on_texture").Mid(3, FString("on_texture").Len() - (3)), &FDevMFBuildCommandRunner::on_texture},
			{FString("on_sample").Mid(3, FString("on_sample").Len() - (3)), &FDevMFBuildCommandRunner::on_sample},
			{FString("on_ddx").Mid(3, FString("on_ddx").Len() - (3)), &FDevMFBuildCommandRunner::on_ddx},
			{FString("on_ddy").Mid(3, FString("on_ddy").Len() - (3)), &FDevMFBuildCommandRunner::on_ddy},
			{FString("on_const_by").Mid(3, FString("on_const_by").Len() - (3)), &FDevMFBuildCommandRunner::on_const_by},
			{FString("on_time").Mid(3, FString("on_time").Len() - (3)), &FDevMFBuildCommandRunner::on_time},
			{FString("on_ternary").Mid(3, FString("on_ternary").Len() - (3)), &FDevMFBuildCommandRunner::on_ternary},
		};
		if (handlers.Contains(command.name())) {
			return handlers[command.name()](builder, command);
		} else {
			return FDevMFBuildCommandRunner::on_call(builder, command);
		}
	}
	private:
	/**
	 * デバッグログを出力
	 * @param command ビルドコマンド
	 */
	static void p__debug_log(FDevMFBuildCommand command) {
		if (command.role == FDevMFBuildCommand::Roles::Bool) {

		} else if (command.role == FDevMFBuildCommand::Roles::Number) {

		} else if (command.role == FDevMFBuildCommand::Roles::String) {
			log_info(Logs::Flags::asset, "[#asset] [FDevMFBuildCommandRunner::p__emit_command]: %s", *FString::Printf(TEXT("command: var_ref, name: %s"), *command.as_string()));
		} else if (command.name() == "get") {
			log_info(Logs::Flags::asset, "[#asset] [FDevMFBuildCommandRunner::p__emit_command]: %s", *FString::Printf(TEXT("command: %s, args: %d, output: %d"), *command.name(), command.arg_num(), command.arg_at(1).as_int()));
		} else if (command.name() == "var") {
			log_info(Logs::Flags::asset, "[#asset] [FDevMFBuildCommandRunner::p__emit_command]: %s", *FString::Printf(TEXT("command: %s, args: %d, var: %s"), *command.name(), command.arg_num(), *command.arg_at(0).as_string()));
		} else {
			log_info(Logs::Flags::asset, "[#asset] [FDevMFBuildCommandRunner::p__emit_command]: %s", *FString::Printf(TEXT("command: %s, args: %d"), *command.name(), command.arg_num()));
		}
	}
	// region インデクサー
	public:
	/** on_get */
	static FDevMFExp on_get(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)).new_index(command.arg_at(1).as_int());
	}
	// endregion
	// region 関数シグネチャー
	public:
	/** on_param */
	static FDevMFExp on_param(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->param(command.arg_at(0).as_string(), command.arg_at(1).as_string(), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(2)), command.arg_at(3).as_string());
	}
	public:
	/** on_returns */
	static FDevMFExp on_returns(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->returns(command.arg_at(0).as_string(), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)), command.arg_at(2).as_string());
	}
	// endregion
	// region マテリアル/スキーマ
	public:
	/** on_schema_domain */
	static FDevMFExp on_schema_domain(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		builder->schema_domain(command.arg_at(0).as_string());
		return FDevMFExp::empty();
	}
	public:
	/** on_schema_blend */
	static FDevMFExp on_schema_blend(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		builder->schema_blend(command.arg_at(0).as_string());
		return FDevMFExp::empty();
	}
	public:
	/** on_schema_shading */
	static FDevMFExp on_schema_shading(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		builder->schema_shading(command.arg_at(0).as_string());
		return FDevMFExp::empty();
	}
	public:
	/** on_schema_option */
	static FDevMFExp on_schema_option(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		builder->schema_option(command.arg_at(0).as_string());
		return FDevMFExp::empty();
	}
	// endregion
	// region マテリアル/出力
	public:
	/** on_output_emissive_color */
	static FDevMFExp on_output_emissive_color(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		builder->output_emissive_color(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
		return FDevMFExp::empty();
	}
	public:
	/** on_output_opacity */
	static FDevMFExp on_output_opacity(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		builder->output_opacity(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
		return FDevMFExp::empty();
	}
	// endregion
	// region 変数
	public:
	/** on_var */
	static FDevMFExp on_var(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->var(command.arg_at(0).as_string(), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)));
	}
	public:
	/** on_vars */
	static FDevMFExp on_vars(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->vars([&]() -> TArray<FString> {
			TArray<FString> l_ret;
			for (auto index = 0; index < command.arg_num() - 1; index++) {
				l_ret.Add(command.arg_at(index).as_string());
			}
			return l_ret;
		}(), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(command.arg_num() - 1)));
	}
	public:
	/** on_var_ref */
	static FDevMFExp on_var_ref(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->var_ref(command.as_string());
	}
	// endregion
	// region 公開パラメーター
	public:
	/** on_ex_bool */
	static FDevMFExp on_ex_bool(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->ex_bool(command.arg_at(0).as_string(), command.arg_at(1).as_string(), command.arg_at(2).as_string(), command.arg_at(3).as_bool(), command.arg_at(4).as_string());
	}
	public:
	/** on_ex_float */
	static FDevMFExp on_ex_float(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->ex_float(command.arg_at(0).as_string(), command.arg_at(1).as_string(), command.arg_at(2).as_string(), command.arg_at(3).as_float(), command.arg_at(4).as_string(), command.arg_at(5).as_float(), command.arg_at(6).as_float());
	}
	public:
	/** on_ex_float3 */
	static FDevMFExp on_ex_float3(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->ex_float3(command.arg_at(0).as_string(), command.arg_at(1).as_string(), command.arg_at(2).as_string(), command.arg_at(3).as_float(), command.arg_at(4).as_float(), command.arg_at(5).as_float(), command.arg_at(6).as_string());
	}
	public:
	/** on_ex_texture */
	static FDevMFExp on_ex_texture(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->ex_texture(command.arg_at(0).as_string(), command.arg_at(1).as_string(), command.arg_at(2).as_string(), command.arg_at(3).as_string(), command.arg_at(4).as_string(), command.arg_num() == 6 ? command.arg_at(5).as_string() : "Color");
	}
	// endregion
	// region リテラル
	public:
	/** on_pi */
	static FDevMFExp on_pi(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->literal_f(PI);
	}
	public:
	/** on_bool */
	static FDevMFExp on_bool(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->literal_b(command.as_bool());
	}
	public:
	/** on_float */
	static FDevMFExp on_float(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->literal_f(command.as_float());
	}
	public:
	/** on_float2 */
	static FDevMFExp on_float2(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->literal_f2(command.arg_at(0).as_float(), command.arg_at(1).as_float());
	}
	public:
	/** on_float3 */
	static FDevMFExp on_float3(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->literal_f3(command.arg_at(0).as_float(), command.arg_at(1).as_float(), command.arg_at(2).as_float());
	}
	public:
	/** on_float4 */
	static FDevMFExp on_float4(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->literal_f4(command.arg_at(0).as_float(), command.arg_at(1).as_float(), command.arg_at(2).as_float(), command.arg_at(3).as_float());
	}
	// endregion
	// region 四則演算
	public:
	/** on_add */
	static FDevMFExp on_add(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->add(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_sub */
	static FDevMFExp on_sub(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->sub(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_mul */
	static FDevMFExp on_mul(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->mul(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_div */
	static FDevMFExp on_div(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->div(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_mod */
	static FDevMFExp on_mod(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->mod(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_one_minus */
	static FDevMFExp on_one_minus(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->one_minus(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	// endregion
	// region 算術演算
	public:
	/** on_abs */
	static FDevMFExp on_abs(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->abs(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	public:
	/** on_power */
	static FDevMFExp on_power(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->power(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_step */
	static FDevMFExp on_step(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->step(values.Get<0>(), values.Get<1>());
	}
	// endregion
	// region 線形補完
	public:
	/** on_lerp */
	static FDevMFExp on_lerp(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(2))};
		return builder->lerp(values.Get<0>(), values.Get<1>(), values.Get<2>());
	}
	public:
	/** on_smoothstep */
	static FDevMFExp on_smoothstep(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(2))};
		return builder->smoothstep(values.Get<0>(), values.Get<1>(), values.Get<2>());
	}
	// endregion
	// region 丸め込み
	public:
	/** on_clamp */
	static FDevMFExp on_clamp(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(2))};
		return builder->clamp(values.Get<0>(), values.Get<1>(), values.Get<2>());
	}
	public:
	/** on_floor */
	static FDevMFExp on_floor(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->floor(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	public:
	/** on_max */
	static FDevMFExp on_max(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->max(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_min */
	static FDevMFExp on_min(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->min(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_saturate */
	static FDevMFExp on_saturate(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->saturate(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	// endregion
	// region 三角関数
	public:
	/** on_cos */
	static FDevMFExp on_cos(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->cos(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), command.arg_num() == 2 ? command.arg_at(1).as_float() : 1.0f);
	}
	public:
	/** on_sin */
	static FDevMFExp on_sin(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->sin(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), command.arg_num() == 2 ? command.arg_at(1).as_float() : 1.0f);
	}
	public:
	/** on_tan */
	static FDevMFExp on_tan(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->tan(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), command.arg_num() == 2 ? command.arg_at(1).as_float() : 1.0f);
	}
	// endregion
	// region ベクトル演算
	public:
	/** on_cross */
	static FDevMFExp on_cross(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->cross(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_dot */
	static FDevMFExp on_dot(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->dot(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_length */
	static FDevMFExp on_length(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->length(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	public:
	/** on_normalize */
	static FDevMFExp on_normalize(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->normalize(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	// endregion
	// region ベクトル操作
	public:
	/** on_append */
	static FDevMFExp on_append(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->append(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_make_float2 */
	static FDevMFExp on_make_float2(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->make_float2(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_make_float3 */
	static FDevMFExp on_make_float3(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(2))};
		return builder->make_float3(values.Get<0>(), values.Get<1>(), values.Get<2>());
	}
	public:
	/** on_make_float4 */
	static FDevMFExp on_make_float4(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(2)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(3))};
		return builder->make_float4(values.Get<0>(), values.Get<1>(), values.Get<2>(), values.Get<3>());
	}
	public:
	/** on_mask */
	static FDevMFExp on_mask(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->mask(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), command.arg_at(1).as_string());
	}
	// endregion
	// region カラー操作
	public:
	/** on_rgb_to_hsv */
	static FDevMFExp on_rgb_to_hsv(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->rgb_to_hsv(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	public:
	/** on_hsv_to_rgb */
	static FDevMFExp on_hsv_to_rgb(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->hsv_to_rgb(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	// endregion
	// region テクスチャー操作
	public:
	/** on_panner */
	static FDevMFExp on_panner(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->panner(values.Get<0>(), values.Get<1>());
	}
	public:
	/** on_tex_coord */
	static FDevMFExp on_tex_coord(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->tex_coord(command.arg_at(0).as_int());
	}
	public:
	/** on_texture */
	static FDevMFExp on_texture(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->texture(command.arg_at(0).as_string(), command.arg_num() == 2 ? command.arg_at(1).as_string() : "Color");
	}
	public:
	/** on_sample */
	static FDevMFExp on_sample(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1))};
		return builder->sample(values.Get<0>(), values.Get<1>(), command.arg_num() == 3 ? command.arg_at(2).as_string() : "Color");
	}
	// endregion
	// region ピクセルシェーダー
	public:
	/** on_ddx */
	static FDevMFExp on_ddx(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->ddx(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	public:
	/** on_ddy */
	static FDevMFExp on_ddy(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->ddy(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)));
	}
	// endregion
	// region パラメーターコレクション
	public:
	/** on_const_by */
	static FDevMFExp on_const_by(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->const_by(command.arg_at(0).as_string());
	}
	// endregion
	// region 時間
	public:
	/** on_time */
	static FDevMFExp on_time(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->time();
	}
	// endregion
	// region フロー制御
	public:
	/** on_ternary */
	static FDevMFExp on_ternary(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		TTuple<FDevMFExp, FDevMFExp, FDevMFExp> values = {FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(0)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(1)), FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(2))};
		return builder->ternary(values.Get<0>(), values.Get<1>(), values.Get<2>());
	}
	// endregion
	// region 関数コール
	public:
	/** on_call */
	static FDevMFExp on_call(FDevMFBuilder* builder, FDevMFBuildCommand command) {
		return builder->call(command.name(), [&]() -> TArray<FDevMFExp> {
			TArray<FDevMFExp> l_ret;
			for (auto index = 0; index < command.arg_num(); index++) {
				l_ret.Add(FDevMFBuildCommandRunner::p__emit_command(builder, command.arg_at(index)));
			}
			return l_ret;
		}());
	}
	// endregion
};
