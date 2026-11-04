// @tranp.meta: {"version":"0.9.19","module":{"hash":"0a2bb34a52758d1a5a69aabafcf07958","path":"FDev.Main.Core.Asset.AssetStorageImpl"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Misc/Paths.h"
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Asset/AssetPaths.h"
#include "FDev/Main/Core/Asset/AssetStorage.h"
#include "FDev/Main/Core/Lang/IO/File.h"
#include "FDev/Main/Core/Lang/Json/Json.h"
#include "FDev/Main/Core/Lang/Json/JsonEntry.h"
#include "FDev/Main/Core/Core.h"
#include "AssetStorageImpl.generated.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/error.h"
// #include "const/const_asset.h"
/**
 * アセットストレージ
 */
UCLASS()
class FDEV_API UFDevAssetStorageImpl : public UFDevIAssetStorage {
	GENERATED_BODY()
	private: UPROPERTY() TMap<FString, UObject*> __caches;
	public:
	/**
	 * インスタンスを生成
	 */
	UFDevAssetStorageImpl() : UFDevIAssetStorage(), __caches() {}
	public:
	/**
	 * アセットが存在するか判定
	 * @param path アセットパス
	 * @return True = 存在
	 */
	bool exists(const FString& path) override {
		return FPackageName::DoesPackageExist(FDevAssetPaths::to_ue_package_path(path));
	}
	public:
	/**
	 * アセットをロード
	 * @param path アセットパス
	 * @param cache True = キャッシュ使用 (default = True)
	 * @return アセット
	 * @throw NotFound 存在しないアセットを指定
	 */
	UObject* load(const FString& path, bool cache = true) override {
		if ((!this->__caches.Contains(path)) || !cache) {
			this->__caches.Add(path, this->load_asset(path));
		}
		return this->__caches[path];
	}
	public:
	/**
	 * アセットをロード
	 * @param path アセットパス
	 * @return アセット
	 * @throw NotFound 存在しないアセットを指定
	 */
	UObject* load_asset(const FString& path) {
		FString ue_asset_path = FDevAssetPaths::to_ue_path(path);
		TSoftObjectPtr<UObject> resolver{FSoftObjectPath(ue_asset_path)};
		UObject* asset = resolver.LoadSynchronous();
		if (!asset) {
			throw FDevCoreError(FString::Printf(TEXT("[Errors::NotFound]: %s, %s"), TEXT("UFDevAssetStorageImpl::load_asset"), *ue_asset_path));
		}
		return asset;
	}
};
/**
 * マスターストレージ
 */
UCLASS()
class FDEV_API UFDevMasterStorageImpl : public UFDevIMasterStorage {
	GENERATED_BODY()
	private: TMap<FString, TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>> __caches;
	public:
	/**
	 * インスタンスを生成
	 */
	UFDevMasterStorageImpl() : UFDevIMasterStorage(), __caches() {}
	public:
	/**
	 * アセットが存在するか判定
	 * @param path アセットパス
	 * @return True = 存在
	 */
	bool exists(const FString& path) override {
		if (this->__caches.Contains(path)) {
			return true;
		}
		if (this->for_origin(path)) {
			return FDevFiles::exiets(FDevAssetPaths::to_master_filepath(path));
		}
		auto [origin_path, internal_path] = this->break_internal_path(path);
		FFDevJson origin = this->load(origin_path);
		return origin.has_key(internal_path);
	}
	public:
	/**
	 * アセットをロード
	 * @param path アセットパス
	 * @param cache True = キャッシュ使用 (default = True)
	 * @return アセット
	 * @throw NotFound 存在しないアセットを指定
	 */
	FFDevJson load(const FString& path, bool cache = true) override {
		if ((!this->__caches.Contains(path)) || !cache) {
			if (this->for_origin(path)) {
				this->__caches.Add(path, this->load_origin(path));
			} else {
				this->__caches.Add(path, this->load_internal(path));
			}
		}
		return FFDevJson((this->__caches[path]).Get());
	}
	public:
	/**
	 * マスターをファイルからロード
	 * @param path アセットパス
	 * @return マスター
	 * @throw NotFound 存在しないアセットを指定
	 */
	TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> load_origin(const FString& path) {
		FString filepath = FDevAssetPaths::to_master_filepath(path);
		return FFDevJson::parse(FDevFiles::load(filepath));
	}
	public:
	/**
	 * マスターの内部データをロード
	 * @param path アセットパス
	 * @return マスター
	 * @throw NotFound 存在しないアセットを指定
	 */
	TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> load_internal(const FString& path) {
		auto [origin_path, internal_path] = this->break_internal_path(path);
		FFDevJson origin = this->load(origin_path);
		return FFDevJson::parse(origin[internal_path].as_string());
	}
	public:
	/**
	 * 対象がオリジンか判定
	 * @param path アセットパス
	 * @return True = オリジン
	 */
	bool for_origin(const FString& path) {
		return FDevString::count(path, "#") == 0;
	}
	public:
	/**
	 * アセットパスからオリジンのパスと内部データのパスに分解
	 * @param path アセットパス
	 * @return (アセットパス, アセットソースパス)
	 */
	TTuple<FString, FString> break_internal_path(const FString& path) {
		int origin_end = path.Find(TEXT("#"));
		return {path.Mid(0, origin_end), path.Mid(origin_end + 1, path.Len() - (origin_end + 1))};
	}
};
