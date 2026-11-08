// @tranp.meta: {"version":"0.9.20","module":{"hash":"682f31c9ffcd8dc39c6c4b5ebd5808f6","path":"FDev.Editor.Asset.AssetMakerFactory"},"transpiler":{"version":"0.9.7","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "FDev/Editor/Asset/AssetMaker.h"
#include "FDev/Editor/Asset/MFAssetMaker.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Asset/Assets.h"
#include "FDev/Main/Core/Asset/AssetStorageImpl.h"
#include "AssetMakerFactory.generated.h"
// #include "enum.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// enum MakerTags
/**
 * アセット生成モジュールファクトリー
 */
UCLASS()
class FDEVEDITOR_API UFDevAssetMakerFactory : public UObject {
	GENERATED_BODY()
	public:
	/**
	 * アセット生成モジュールを生成
	 * @param tag モジュールタグ
	 * @param outer 管理オブジェクト
	 * @return アセット生成モジュール
	 */
	static UFDevAssetMaker* create(const FString& tag, UObject* outer) {
		return UFDevAssetMakerFactory::from_class(UFDevAssetMakerFactory::to_uclass(tag), outer);
	}
	public:
	/**
	 * アセット生成モジュールを生成
	 * @param uclass クラスの型情報
	 * @param outer 管理オブジェクト
	 * @return アセット生成モジュール
	 */
	UFUNCTION(BlueprintCallable, meta=(DefaultToSelf="outer"))
	static UFDevAssetMaker* from_class(UClass* uclass, UObject* outer) {
		UFDevAssetMaker* instance = NewObject<UFDevAssetMaker>(outer, uclass);
		instance->injection(UFDevAssetMakerFactory::new_assets(outer));
		return instance;
	}
	public:
	/**
	 * モジュールタグからクラスの型情報を解決
	 * @param tag モジュールタグ
	 * @return クラスの型情報
	 */
	static UClass* to_uclass(const FString& tag) {
		static TMap<FString, UClass*> to_uclasses = {{"mfs", UFDevMFAssetMaker::StaticClass()}};
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
