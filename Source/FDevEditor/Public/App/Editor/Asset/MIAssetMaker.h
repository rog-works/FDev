// @tranp.meta: {"version":"0.9.24","module":{"hash":"709bbfc8e80cd8925b630cb01233e377","path":"App.Editor.Asset.MIAssetMaker"},"transpiler":{"version":"0.9.11","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "AssetToolsModule.h"
#include "Templates/SharedPointer.h"
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "UnrealEd/Factories/MaterialInstanceConstantFactoryNew.h"
#include "Materials/Material.h"
#include "Materials/MaterialInstanceConstant.h"
#include "App/Editor/Asset/AssetMaker.h"
#include "App/Editor/Material/MIBuilder.h"
#include "App/Main/Core/Asset/AssetPaths.h"
#include "App/Main/Core/Lang/Json/Json.h"
#include "MIAssetMaker.generated.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "const/const_asset.h"
/**
 * アセット生成モジュール(マテリアルインスタンス)
 */
UCLASS(BlueprintType)
class FDEVEDITOR_API UFDevMIAssetMaker : public UFDevAssetMaker {
	GENERATED_BODY()
	private: TMap<FString, TTuple<FString, FFDevJson>> p__commands;
	public:
	/**
	 * インスタンスを生成
	 */
	UFDevMIAssetMaker() : UFDevAssetMaker(), p__commands() {}
	public:
	/**
	 *
	 * @return コマンド一覧
	 */
	const TMap<FString, TTuple<FString, FFDevJson>>& commands() {
		if (this->p__commands.Num() == 0) {
			FFDevJson data = this->assets()->master_of(FDevAssetPaths::to_path("master/app", "mis"));
			// FIXME 名前とパスが混在して微妙。GetFNameの結果に依存するべきではない
			this->p__commands = [&]() -> TMap<FString, TTuple<FString, FFDevJson>> {
				TMap<FString, TTuple<FString, FFDevJson>> l_ret;
				for (auto& src : data.keys()) {
					l_ret.Add(FDevAssetPaths::pick_name(src), {src, data[src]});
				}
				return l_ret;
			}();
		}
		return this->p__commands;
	}
	public:
	/**
	 * アセットパスに変換
	 * @param src ソースパス
	 * @return アセットパス
	 */
	FString to_asset_path(const FString& src) override {
		return FDevAssetPaths::to_path("material", src);
	}
	public:
	/**
	 *
	 * @return 全アセットのソースパスリスト
	 */
	TArray<FString> all_srcs() override {
		return [&]() -> TArray<FString> {
			TArray<FString> l_ret;
			for (auto& [l_, entry] : this->commands()) {
				l_ret.Add(entry.Get<0>());
			}
			return l_ret;
		}();
	}
	public:
	/**
	 * アセットを解決
	 * @param asset_path アセットパス
	 * @return アセット
	 */
	UObject* resolve_asset(const FString& asset_path) override {
		return this->assets()->asset_of<UMaterialInstanceConstant>(asset_path);
	}
	public:
	/**
	 * アセットの更新をスキップするか判定
	 * @param asset アセット
	 * @return True = スキップ
	 * @note アセット内に保存したメタデータのハッシュ値を基に更新可否を判定
	 */
	bool skip_update(UObject* asset) override {
		FString name = asset->GetFName().ToString();
		return this->fetch_hash(asset) == this->commands()[name].Get<1>()["hash"].as_string();
	}
	public:
	/**
	 * アセットを生成(実装)
	 * @param package パッケージ
	 * @param asset_path アセットパス
	 * @return アセット
	 */
	UObject* new_asset_impl(UPackage* package, const FString& asset_path) override {
		FString name = FDevAssetPaths::pick_name(asset_path);
		FString via_src = FDevMIBuildCommandRunner::via_src(this->commands()[name].Get<1>());
		UMaterial* via = this->assets()->asset_of<UMaterial>(FDevAssetPaths::to_path("material", via_src));
		UMaterialInstanceConstantFactoryNew* factory = NewObject<UMaterialInstanceConstantFactoryNew>(package);
		factory->InitialParent = TObjectPtr<UMaterialInterface>(via);
		UObject* asset = FAssetToolsModule::GetModule().Get().CreateAsset(name, FDevAssetPaths::to_ue_save_dir(asset_path), UMaterialInstanceConstant::StaticClass(), factory);
		return CastChecked<UMaterialInstanceConstant>(asset);
	}
	public:
	/**
	 * アセットをビルド(実装)
	 * @param asset アセット
	 */
	void build_asset_impl(UObject* asset) override {
		UMaterialInstanceConstant* mi = static_cast<UMaterialInstanceConstant*>(asset);
		FString name = mi->GetFName().ToString();
		FDevMIBuilder builder{this->assets(), mi};
		FDevMIBuildCommandRunner::run((&(builder)), this->commands()[name].Get<1>());
		this->apply_hash(asset, this->commands()[name].Get<1>()["hash"].as_string());
	}
};
