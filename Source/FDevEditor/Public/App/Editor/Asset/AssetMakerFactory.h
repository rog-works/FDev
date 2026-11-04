// @tranp.meta: {"version":"0.9.19","module":{"hash":"d2ad1a4cab04d07a3112c8669b21cbd5","path":"App.Editor.Asset.AssetMakerFactory"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "App/Editor/Asset/AssetMaker.h"
#include "App/Editor/Asset/MFAssetMaker.h"
#include "App/Main/Core/Asset/Assets.h"
#include "App/Main/Core/Asset/AssetStorageImpl.h"
#include "AssetMakerFactory.generated.h"
// #include "enum.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// enum MakerTags
/**
 * アセット生成モジュールファクトリー
 */
UCLASS()
class FDEVEDITOR_API UAssetMakerFactory : public UObject {
	GENERATED_BODY()
	public:
	/**
	 * アセット生成モジュールを生成
	 * @param tag モジュールタグ
	 * @param outer 管理オブジェクト
	 * @return アセット生成モジュール
	 */
	static UAssetMaker* create(const FString& tag, UObject* outer) {
		return UAssetMakerFactory::from_class(UAssetMakerFactory::to_uclass(tag), outer);
	}
	public:
	/**
	 * アセット生成モジュールを生成
	 * @param uclass クラスの型情報
	 * @param outer 管理オブジェクト
	 * @return アセット生成モジュール
	 */
	UFUNCTION(BlueprintCallable, meta=(DefaultToSelf="outer"))
	static UAssetMaker* from_class(UClass* uclass, UObject* outer) {
		UAssetMaker* instance = NewObject<UAssetMaker>(outer, uclass);
		instance->injection(UAssetMakerFactory::new_assets(outer));
		return instance;
	}
	public:
	/**
	 * モジュールタグからクラスの型情報を解決
	 * @param tag モジュールタグ
	 * @return クラスの型情報
	 */
	static UClass* to_uclass(const FString& tag) {
		static TMap<FString, UClass*> to_uclasses = {{"mfs", UMFAssetMaker::StaticClass()}};
		return to_uclasses[tag];
	}
	public:
	/**
	 *
	 * @param outer 管理オブジェクト
	 * @return アセットマネージャー
	 */
	static UFDevAssets* new_assets(UObject* outer) {
		UFDevAssets* assets = NewObject<UFDevAssets>(outer);
		assets->injection(NewObject<UFDevAssetStorageImpl>(outer), NewObject<UFDevMasterStorageImpl>(outer));
		return assets;
	}
};
