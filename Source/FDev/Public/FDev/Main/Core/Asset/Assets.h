// @tranp.meta: {"version":"0.9.20","module":{"hash":"9a4937c47a46629e31cfc17e72ca3afb","path":"FDev.Main.Core.Asset.Assets"},"transpiler":{"version":"0.9.7","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Asset/AssetStorage.h"
#include "FDev/Main/Core/Lang/Convertion.h"
#include "FDev/Main/Core/Lang/Json/Json.h"
#include "Assets.generated.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "const/const_asset.h"
/**
 * アセットマネージャー
 */
UCLASS()
class FDEV_API UFDevAssets : public UObject {
	GENERATED_BODY()
	private: UFDevIAssetStorage* p__asset_storage;
	private: UFDevIMasterStorage* p__master_storage;
	public:
	/**
	 * インスタンスを生成
	 */
	UFDevAssets() : UObject(), p__asset_storage(nullptr), p__master_storage(nullptr) {}
	public:
	/**
	 * 依存を注入
	 */
	void injection(UFDevIAssetStorage* asset_storage, UFDevIMasterStorage* master_storage) {
		this->p__asset_storage = asset_storage;
		this->p__master_storage = master_storage;
	}
	public:
	/**
	 *
	 * @return アセットストレージ
	 */
	UFDevIAssetStorage* asset_storage() {
		return FDevsafe_addr(this->p__asset_storage);
	}
	public:
	/**
	 *
	 * @return マスターストレージ
	 */
	UFDevIMasterStorage* master_storage() {
		return FDevsafe_addr(this->p__master_storage);
	}
	public:
	/**
	 * アセットが存在するか判定
	 * @param path アセットパス
	 * @return True = 存在
	 */
	UFUNCTION()
	bool exists(const FString& path) {
		if (path.StartsWith("master")) {
			return this->master_storage()->exists(path);
		} else {
			return this->asset_storage()->exists(path);
		}
	}
	public:
	/**
	 * アセットを解決
	 * @param asset_type アセットの型
	 * @param path アセットパス
	 * @param cache True = キャッシュ使用 (default = True)
	 * @return アセット
	 * @throw NotFound 存在しないアセットを指定
	 */
	template<typename T_Obj>
	T_Obj* asset_of(const FString& path, bool cache = true) {
		return CastChecked<T_Obj>(this->asset_storage()->load(path, cache));
	}
	public:
	/**
	 * アセット(マスター)を解決
	 * @param path アセットパス
	 * @param cache True = キャッシュ使用 (default = True)
	 * @return アセット
	 * @throw NotFound 存在しないアセットを指定
	 */
	FFDevJson master_of(const FString& path, bool cache = true) {
		return this->master_storage()->load(path, cache);
	}
};
