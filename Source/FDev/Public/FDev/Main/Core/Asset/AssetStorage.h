// @tranp.meta: {"version":"0.9.20","module":{"hash":"28f89eca6ddc183e4bd80f72a6d4db92","path":"FDev.Main.Core.Asset.AssetStorage"},"transpiler":{"version":"0.9.7","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Lang/Json/Json.h"
#include "FDev/Main/Core/Core.h"
#include "AssetStorage.generated.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/error.h"
/**
 * アセットストレージ(インターフェイス)
 */
UCLASS(Abstract)
class FDEV_API UFDevIAssetStorage : public UObject {
	GENERATED_BODY()
	public:
	/**
	 * アセットが存在するか判定
	 * @param path アセットパス
	 * @return True = 存在
	 */
	virtual bool exists(const FString& path) {
		throw FDevCoreError(TEXT("[Errors::MustBeImplemented]:"));
	}
	public:
	/**
	 * アセットをロード
	 * @param path アセットパス
	 * @param cache True = キャッシュ使用 (default = True)
	 * @return アセット
	 * @throw NotFound 存在しないアセットを指定
	 */
	virtual UObject* load(const FString& path, bool cache = true) {
		throw FDevCoreError(TEXT("[Errors::MustBeImplemented]:"));
	}
};
/**
 * マスターストレージ(インターフェイス)
 */
UCLASS(Abstract)
class FDEV_API UFDevIMasterStorage : public UObject {
	GENERATED_BODY()
	public:
	/**
	 * アセットが存在するか判定
	 * @param path アセットパス
	 * @return True = 存在
	 */
	virtual bool exists(const FString& path) {
		throw FDevCoreError(TEXT("[Errors::MustBeImplemented]:"));
	}
	public:
	/**
	 * アセットをロード
	 * @param path アセットパス
	 * @param cache True = キャッシュ使用 (default = True)
	 * @return アセット
	 * @throw NotFound 存在しないアセットを指定
	 */
	virtual FFDevJson load(const FString& path, bool cache = true) {
		throw FDevCoreError(TEXT("[Errors::MustBeImplemented]:"));
	}
};
