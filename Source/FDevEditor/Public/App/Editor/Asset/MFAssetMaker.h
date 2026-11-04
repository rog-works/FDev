// @tranp.meta: {"version":"0.9.19","module":{"hash":"04c92998a163bf1df6c3d5e75add4198","path":"App.Editor.Asset.MFAssetMaker"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/NameTypes.h"
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
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
 * アセット生成モジュール(マテリアル関数)
 */
UCLASS(BlueprintType)
class FDEVEDITOR_API UMFAssetMaker : public UAssetMaker {
	GENERATED_BODY()
	private: TMap<FString, TTuple<FString, MFBuildCommand>> __commands;
	public:
	/**
	 * インスタンスを生成
	 */
	UMFAssetMaker() : UAssetMaker(), __commands() {}
	public:
	/**
	 *
	 * @return コマンド一覧
	 */
	const TMap<FString, TTuple<FString, MFBuildCommand>>& commands() {
		if (this->__commands.Num() == 0) {
			FFDevJson data = this->assets()->master_of(FDevAssetPaths::to_path("master/app", "mfs"));
			// FIXME 名前とパスが混在して微妙。GetFNameの結果に依存するべきではない
			for (auto& [src, command] : MFBuildCommandRunner::parse(data)) {
				this->__commands.Add(FDevAssetPaths::pick_name(src), {src, command});
			}
		}
		return this->__commands;
	}
	public:
	/**
	 *
	 * @param name アセット名
	 * @return コマンド
	 */
	MFBuildCommand command_by(const FString& name) {
		return this->commands()[name].Get<1>();
	}
	public:
	/**
	 * アセットパスに変換
	 * @param src ソースパス
	 * @return アセットパス
	 */
	FString to_asset_path(const FString& src) override {
		return FDevAssetPaths::to_path("material/func", src);
	}
	public:
	/**
	 *
	 * @return 全アセットのソースパスリスト
	 */
	TArray<FString> all_srcs() override {
		return [&]() -> TArray<FString> {
			TArray<FString> __ret;
			for (auto& [_, entry] : this->commands()) {
				__ret.Add(entry.Get<0>());
			}
			return __ret;
		}();
	}
	public:
	/**
	 * アセットを解決
	 * @param asset_path アセットパス
	 * @return アセット
	 */
	UObject* resolve_asset(const FString& asset_path) override {
		return this->assets()->asset_of<UMaterialFunction>(asset_path);
	}
	public:
	/**
	 * アセットの更新をスキップするか判定
	 * @param asset アセット
	 * @return True = スキップ
	 * @note 既存データのDescription末尾の関数のハッシュ値を基に更新可否を判定
	 */
	bool skip_update(UObject* asset) override {
		UMaterialFunction* mf = static_cast<UMaterialFunction*>(asset);
		return this->fetch_hash(asset) == this->command_by(mf->GetName()).hash();
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
		UMaterialFunction* asset = NewObject<UMaterialFunction>(package, UMaterialFunction::StaticClass(), FName(name));
		asset->SetFlags(EObjectFlags::RF_Public | EObjectFlags::RF_Standalone);
		return asset;
	}
	public:
	/**
	 * アセットをビルド(実装)
	 * @param asset アセット
	 */
	void build_asset_impl(UObject* asset) override {
		UMaterialFunction* mf = static_cast<UMaterialFunction*>(asset);
		FString name = mf->GetFName().ToString();
		MFBuilder builder{this->assets(), mf};
		MFBuildCommandRunner::run((&(builder)), this->command_by(name));
		this->apply_hash(asset, this->command_by(mf->GetName()).hash());
	}
};
