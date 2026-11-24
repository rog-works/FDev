// @tranp.meta: {"version":"0.9.25","module":{"hash":"49472999bebca32528a5d46bbeb7c246","path":"App.Editor.Asset.Impl.MFAssetMaker"},"transpiler":{"version":"0.9.12","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "AssetToolsModule.h"
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "Factories/MaterialFactoryNew.h"
#include "Factories/MaterialFunctionFactoryNew.h"
#include "Materials/Material.h"
#include "Materials/MaterialFunction.h"
#include "App/Editor/Asset/AssetMaker.h"
#include "App/Editor/Material/MFBuildCommand.h"
#include "App/Editor/Material/MFBuilder.h"
#include "App/Main/Core/Asset/AssetPaths.h"
#include "MFAssetMaker.generated.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "const/const_asset.h"
/**
 * アセット生成モジュール(マテリアル関数/マテリアル)
 */
UCLASS(BlueprintType)
class FDEVEDITOR_API UFDevMFAssetMaker : public UFDevAssetMaker {
	GENERATED_BODY()
	private: TMap<FString, TTuple<FString, FDevMFBuildCommand>> p__commands;
	public:
	/**
	 * インスタンスを生成
	 */
	UFDevMFAssetMaker() : UFDevAssetMaker(), p__commands() {}
	public:
	/**
	 *
	 * @return コマンド一覧
	 */
	const TMap<FString, TTuple<FString, FDevMFBuildCommand>>& commands() {
		if (this->p__commands.Num() == 0) {
			FFDevJson data = this->assets()->master_of(FDevAssetPaths::to_path("master/app", "mfs"));
			// FIXME 名前とパスが混在して微妙。GetNameの結果に依存するべきではない
			for (auto& [src, command] : FDevMFBuildCommandRunner::parse(data)) {
				this->p__commands.Add(FDevAssetPaths::pick_name(src), {src, command});
			}
		}
		return this->p__commands;
	}
	public:
	/**
	 *
	 * @param name アセット名
	 * @return コマンド
	 */
	FDevMFBuildCommand command_by(const FString& name) {
		return this->commands()[name].Get<1>();
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
		if (asset_path.StartsWith("material/func")) {
			return this->assets()->asset_of<UMaterialFunction>(asset_path);
		} else {
			return this->assets()->asset_of<UMaterial>(asset_path);
		}
	}
	public:
	/**
	 * アセットの更新をスキップするか判定
	 * @param asset アセット
	 * @return True = スキップ
	 */
	bool skip_update(UObject* asset) override {
		return this->fetch_hash(asset) == this->command_by(asset->GetName()).hash();
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
		if (asset_path.StartsWith("material/func")) {
			UMaterialFunctionFactoryNew* factory = NewObject<UMaterialFunctionFactoryNew>(package);
			return FAssetToolsModule::GetModule().Get().CreateAsset(name, FDevAssetPaths::to_ue_save_dir(asset_path), UMaterialFunction::StaticClass(), factory);
		} else {
			UMaterialFactoryNew* factory = NewObject<UMaterialFactoryNew>(package);
			return FAssetToolsModule::GetModule().Get().CreateAsset(name, FDevAssetPaths::to_ue_save_dir(asset_path), UMaterial::StaticClass(), factory);
		}
	}
	public:
	/**
	 * アセットをビルド(実装)
	 * @param asset アセット
	 */
	void build_asset_impl(UObject* asset) override {
		if (asset->IsA(UMaterialFunction::StaticClass())) {
			FDevMFBuilder builder = FDevMFBuilder::from_mf(this->assets(), static_cast<UMaterialFunction*>(asset));
			FDevMFBuildCommandRunner::build_mf((&(builder)), this->command_by(asset->GetName()));
		} else {
			FDevMFBuilder builder = FDevMFBuilder::from_material(this->assets(), static_cast<UMaterial*>(asset));
			FDevMFBuildCommandRunner::build_material((&(builder)), this->command_by(asset->GetName()));
		}
		this->apply_hash(asset, this->command_by(asset->GetName()).hash());
	}
};
