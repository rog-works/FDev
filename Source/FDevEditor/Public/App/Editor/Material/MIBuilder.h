// @tranp.meta: {"version":"0.9.25","module":{"hash":"ae72c99210a7e3f604eb20f9eea3bb51","path":"App.Editor.Material.MIBuilder"},"transpiler":{"version":"0.9.12","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Math/Color.h"
#include "Misc/Guid.h"
#include "UObject/NameTypes.h"
#include "Engine/Texture.h"
#include "Materials/MaterialInstanceConstant.h"
#include "App/Main/Core/Asset/AssetPaths.h"
#include "App/Main/Core/Asset/Assets.h"
#include "App/Main/Core/Lang/Convertion.h"
#include "App/Main/Core/Lang/Json/Json.h"
#include "App/Main/Core/Core.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "compatible/error.h"
// #include "const/const_asset.h"
/**
 * アセットビルダー(マテリアルインスタンス)
 */
class FDevMIBuilder {
	private: UFDevAssets* p__assets;
	private: UMaterialInstanceConstant* p__mi;
	public: TMap<FString, bool> bools;
	public: TMap<FString, float> floats;
	public: TMap<FString, FLinearColor> vectors;
	public: TMap<FString, UTexture*> textures;
	public:
	/**
	 * インスタンスを生成
	 * @param assets アセットマネージャー
	 * @param mi マテリアルインスタンス
	 */
	FDevMIBuilder(UFDevAssets* assets, UMaterialInstanceConstant* mi) : p__assets(assets), p__mi(mi), bools(), floats(), vectors(), textures() {}
	public:
	/**
	 *
	 * @return アセットマネージャー
	 */
	UFDevAssets* assets() {
		return FDevsafe_addr(this->p__assets);
	}
	public:
	/**
	 *
	 * @return マテリアルインスタンス
	 */
	UMaterialInstanceConstant* mi() {
		return FDevsafe_addr(this->p__mi);
	}
	public:
	/**
	 *
	 * @param name パラメーター名, enable: True = 有効
	 */
	void a_bool(const FString& name, bool enable) {
		this->bools.Add(name, enable);
	}
	public:
	/**
	 *
	 * @param name パラメーター名, value: 値
	 */
	void a_float(const FString& name, float value) {
		this->floats.Add(name, value);
	}
	public:
	/**
	 *
	 * @param name パラメーター名, x: X, y: Y, z: Z
	 */
	void a_vector(const FString& name, float x, float y, float z) {
		this->vectors.Add(name, FLinearColor(x, y, z, 1.0f));
	}
	public:
	/**
	 *
	 * @param name パラメーター名, src: 画像ソースパス
	 */
	void a_texture(const FString& name, const FString& src) {
		this->textures.Add(name, this->assets()->asset_of<UTexture>(FDevAssetPaths::to_path("image/texture", src)));
	}
	public:
	/**
	 * パラメーターを構築
	 */
	void build() {
		// パラメーターの削除
		this->mi()->ClearParameterValuesEditorOnly();
		FStaticParameterSet static_params = this->mi()->GetStaticParameters();
		FStaticParameterSetRuntimeData& static_collection = static_params.GetRuntime();
		static_collection.Empty();
		static_params.Empty();
		// パラメーターを構築
		for (auto& [key, value] : this->floats) {
			this->mi()->SetScalarParameterValueEditorOnly(FMaterialParameterInfo(FName(key)), value);
		}
		for (auto& [key, vector] : this->vectors) {
			this->mi()->SetVectorParameterValueEditorOnly(FMaterialParameterInfo(FName(key)), vector);
		}
		for (auto& [key, texture] : this->textures) {
			this->mi()->SetTextureParameterValueEditorOnly(FMaterialParameterInfo(FName(key)), texture);
		}
		for (auto& [key, enable] : this->bools) {
			FStaticSwitchParameter bool_param{FMaterialParameterInfo(FName(key)), enable, true, FGuid::NewGuid()};
			static_collection.StaticSwitchParameters.Add(bool_param);
		}
		FMaterialUpdateContext context{};
		this->mi()->UpdateStaticPermutation(static_params, (&(context)));
	}
};
/**
 * マテリアルインスタンスビルドコマンドランナー
 */
class FDevMIBuildCommandRunner {
	public:
	/**
	 * 生成元のマテリアルのソースパスを取得
	 * @param data コマンドデータ
	 * @return アセットソースパス(ドメイン相対/マテリアル)
	 */
	static FString via_src(FFDevJson data) {
		return data["via"].as_string();
	}
	public:
	/**
	 * 実行処理
	 * @param builder マテリアルインスタンスビルダー
	 * @param data コマンドデータ
	 */
	static void run(FDevMIBuilder* builder, FFDevJson data) {
		FFDevJson exports = data["exports"];
		for (auto& key : exports.keys()) {
			FFDevJson com = exports[key];
			if (com.is_bool()) {
				builder->a_bool(key, com.as_bool());
			} else if (com.is_float()) {
				builder->a_float(key, com.as_float());
			} else if (com.is_array()) {
				builder->a_vector(key, com.at(0).as_float(), com.at(1).as_float(), com.at(2).as_float());
			} else if (com.is_string()) {
				builder->a_texture(key, com.as_string());
			} else {
				throw CoreError(FString::Printf(TEXT("[Errors::Never]: %s, %s, %s"), TEXT("FDevMIBuildCommandRunner::run"), *key, *(com).ToString()));
			}
		}
		builder->build();
	}
};
