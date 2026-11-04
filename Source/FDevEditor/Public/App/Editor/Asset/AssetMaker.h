// @tranp.meta: {"version":"0.9.19","module":{"hash":"cf5740af16ac651adf7c6cd5ce9f09a4","path":"App.Editor.Asset.AssetMaker"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "AssetRegistry/AssetRegistryModule.h"
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "UObject/SavePackage.h"
#include "App/Main/Const/ProjectConst.h"
#include "App/Main/Core/Asset/AssetPaths.h"
#include "App/Main/Core/Asset/Assets.h"
#include "App/Main/Core/Lang/Convertion.h"
#include "App/Main/Core/Core.h"
#include "AssetMaker.generated.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/error.h"
/**
 * アセット生成モジュール(基底)
 */
UCLASS(Abstract, BlueprintType)
class FDEVEDITOR_API UFDevAssetMaker : public UObject {
	GENERATED_BODY()
	private: UFDevAssets* __assets;
	public:
	/**
	 * インスタンスを生成
	 */
	UFDevAssetMaker() : UObject(), __assets(nullptr) {}
	public:
	/**
	 * 依存を注入
	 */
	void injection(UFDevAssets* assets) {
		this->__assets = assets;
	}
	public:
	/**
	 *
	 * @return アセットマネージャー
	 */
	UFDevAssets* assets() {
		return safe_addr(this->__assets);
	}
	public:
	/**
	 * アセットパスに変換
	 * @param src ソースパス
	 * @return アセットパス
	 */
	virtual FString to_asset_path(const FString& src) {
		return src;
	}
	public:
	/**
	 *
	 * @return 全アセットのソースパスリスト
	 */
	virtual TArray<FString> all_srcs() {
		return {};
	}
	public:
	/**
	 * アセットを生成
	 * @param src ソースパス
	 * @param force True = 強制実行 (default = False)
	 * @return True = 生成・更新
	 * @throw Fatal アセットの生成に失敗
	 */
	UFUNCTION(BlueprintCallable)
	bool create_in_editor(const FString& src, bool force = false) {
		return this->create(src, force);
	}
	public:
	/**
	 * アセットを一括生成
	 * @param force True = 強制実行 (default = False)
	 * @return 生成・更新対象リスト
	 * @throw Fatal アセットの生成に失敗
	 */
	UFUNCTION(BlueprintCallable)
	TArray<FString> create_all_in_editor(bool force = false) {
		return this->create_all(force);
	}
	public:
	/**
	 * アセットを一括生成
	 * @param force True = 強制実行 (default = False)
	 * @return 生成・更新対象リスト
	 * @throw Fatal アセットの生成に失敗
	 */
	TArray<FString> create_all(bool force = false) {
		TArray<FString> updates = {};
		for (auto& src : this->all_srcs()) {
			if (this->create(src, force)) {
				updates.Add(src);
			}
		}
		return updates;
	}
	public:
	/**
	 * アセットを生成
	 * @param src ソースパス
	 * @param force True = 強制実行 (default = False)
	 * @return True = 生成・更新
	 * @throw Fatal アセットの生成に失敗
	 */
	bool create(const FString& src, bool force = false) {
		FString asset_path = this->to_asset_path(src);
		UObject* asset = this->find_asset(asset_path);
		if (!force && asset && this->skip_update(asset)) {
			return false;
		} else if (asset == nullptr) {
			this->run_new(asset_path);
			return true;
		} else {
			this->run_update(asset);
			return true;
		}
	}
	public:
	/**
	 * アセットを検索
	 * @param asset_path アセットパス
	 * @return アセット | None
	 */
	UObject* find_asset(const FString& asset_path) {
		if (!this->assets()->exists(asset_path)) {
			return nullptr;
		}
		return this->resolve_asset(asset_path);
	}
	public:
	/**
	 * アセットを解決
	 * @param asset_path アセットパス
	 * @return アセット
	 */
	virtual UObject* resolve_asset(const FString& asset_path) {
		throw CoreError(TEXT("[Errors::MustBeImplemented]:"));
	}
	public:
	/**
	 * アセットの更新をスキップするか判定
	 * @param asset アセット
	 * @return True = スキップ
	 */
	virtual bool skip_update(UObject* asset) {
		return false;
	}
	public:
	/**
	 * 実行処理(生成)
	 * @param asset_path アセットパス
	 */
	void run_new(const FString& asset_path) {
		UObject* asset = this->new_asset(asset_path);
		this->build_asset(asset);
		this->save_asset(asset);
	}
	public:
	/**
	 * 実行処理(更新)
	 * @param asset アセット
	 */
	void run_update(UObject* asset) {
		this->build_asset(asset);
		this->save_asset(asset);
	}
	public:
	/**
	 * アセットを生成
	 * @param asset_path アセットパス
	 * @return アセット
	 */
	UObject* new_asset(const FString& asset_path) {
		UPackage* package = CreatePackage((*FDevAssetPaths::to_ue_save_package_path(asset_path)));
		package->FullyLoad();
		return this->new_asset_impl(package, asset_path);
	}
	public:
	/**
	 * アセットを生成(実装)
	 * @param package パッケージ
	 * @param asset_path アセットパス
	 * @return アセット
	 */
	virtual UObject* new_asset_impl(UPackage* package, const FString& asset_path) {
		throw CoreError(TEXT("[Errors::MustBeImplemented]:"));
	}
	public:
	/**
	 * アセットをビルド
	 * @param asset アセット
	 */
	void build_asset(UObject* asset) {
		this->build_asset_impl(asset);
		asset->PostEditChange();
		FAssetRegistryModule::AssetCreated(asset);
		asset->MarkPackageDirty();
	}
	public:
	/**
	 * アセットをビルド(実装)
	 * @param asset アセット
	 */
	virtual void build_asset_impl(UObject* asset) {
		throw CoreError(TEXT("[Errors::MustBeImplemented]:"));
	}
	public:
	/**
	 * アセットをストレージに保存
	 * @param asset アセット
	 * @throw Fatal アセットの生成に失敗
	 */
	void save_asset(UObject* asset) {
		UPackage* package = asset->GetPackage();
		FString filepath = FDevAssetPaths::to_ue_save_filepath(package->GetFName().ToString());
		FSavePackageArgs save_args{};
		save_args.TopLevelFlags = EObjectFlags::RF_Public | EObjectFlags::RF_Standalone;
		if (!package->SavePackage(package, asset, (*filepath), save_args)) {
			throw CoreError(FString::Printf(TEXT("[Errors::Fatal]: %s, %s, %s"), TEXT("UFDevAssetMaker::save_asset"), *asset->GetPathName(), *filepath));
		}
	}
	public:
	/**
	 * アセットのメタデータからハッシュ値を取得
	 * @param asset アセット
	 * @return ハッシュ値
	 */
	FString fetch_hash(UObject* asset) {
		return asset->GetPackage()->GetMetaData().GetValue(asset, (*FString("hash")));
	}
	public:
	/**
	 * アセットのメタデータにハッシュ値を設定
	 * @param asset アセット
	 * @param hash ハッシュ値
	 */
	void apply_hash(UObject* asset, const FString& hash) {
		asset->GetPackage()->GetMetaData().SetValue(asset, (*FString("hash")), (*hash));
	}
};
