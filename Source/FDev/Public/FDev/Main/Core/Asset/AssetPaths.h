// @tranp.meta: {"version":"0.9.20","module":{"hash":"bfe8c2f6297a21cdeab5346ac3e4c2b5","path":"FDev.Main.Core.Asset.AssetPaths"},"transpiler":{"version":"0.9.7","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Misc/Paths.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Lang/DSN/DSN.h"
#include "FDev/Main/Core/Core.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/error.h"
// #include "const/const_asset.h"
/**
 * ユーティリティー(アセットパス)
 */
class FDevAssetPaths {
	// region 一般
	public:
	/**
	 * アセットソースパスをアセットパスに変換
	 * @param domain アセットドメイン
	 * @param src アセットソースパス(ドメイン相対)
	 * @return アセットパス
	 */
	static FString to_path(const FString& domain, const FString& src) {
		return FString::Printf(TEXT("%s/%s"), *domain, *src);
	}
	// endregion
	// region UEアセット
	public:
	/**
	 * アセットパスからアセット名を取得
	 * @param path アセットパス
	 * @return アセット名
	 * @throw InvalidArguments ドット/シャープを含むパスを指定
	 */
	static FString pick_name(const FString& path) {
		if (FDevString::count(path, ".") != 0 || FDevString::count(path, "#") != 0) {
			throw FDevCoreError(FString::Printf(TEXT("[Errors::InvalidArguments]: %s, %s"), TEXT("FDevAssetPaths::pick_name"), *path));
		}
		return path.Mid(path.Find(TEXT("/"), ESearchCase::IgnoreCase, ESearchDir::FromEnd) + 1, path.Len() - (path.Find(TEXT("/"), ESearchCase::IgnoreCase, ESearchDir::FromEnd) + 1));
	}
	public:
	/**
	 * アセットパスからパッケージパスに変換
	 * @param path アセットパス
	 * @return UEアセットパス(パッケージ)
	 * @note 相対パスの場合はプロジェクト用のパスと見做して接頭辞('/Game/')を補完
	 */
	static FString to_ue_package_path(const FString& path) {
		if (!path.StartsWith("/")) {
			return FDevDSN::joined(FDevPackageConst::Game, path, "/");
		} else {
			return path;
		}
	}
	public:
	/**
	 * アセットパスからUEアセットパスに変換
	 * @param path アセットパス
	 * @return UEアセットパス
	 * @note 相対パスの場合はプロジェクト用のパスと見做して接頭辞('/Game/')を補完
	 */
	static FString to_ue_path(const FString& path) {
		int begin_name = path.Find(TEXT("/"), ESearchCase::IgnoreCase, ESearchDir::FromEnd);
		FString asset_name = begin_name > 0 ? path.Mid(begin_name + 1, path.Len() - (begin_name + 1)) : path;
		FString ue_path = FDevDSN::joined(path, asset_name);
		if (!path.StartsWith("/")) {
			return FDevDSN::joined(FDevPackageConst::Game, ue_path, "/");
		} else {
			return ue_path;
		}
	}
	// endregion
	// region UEアセット/アセット生成
	public:
	/**
	 * アセットパスから保存先のディレクトリーパスに変換 ※誤変換を避けるため、アセット生成以外で利用しないこと
	 * @param path アセットパス
	 * @return UEアセットパス(ディレクトリー)
	 * @throw InvalidArguments フルパスを指定
	 */
	static FString to_ue_save_dir(const FString& path) {
		if (path.StartsWith("/")) {
			throw FDevCoreError(FString::Printf(TEXT("[Errors::InvalidArguments]: %s, %s"), TEXT("FDevAssetPaths::to_ue_save_dir"), *path));
		}
		return FDevDSN::joined(FDevPackageConst::Game, path.Mid(0, path.Find(TEXT("/"), ESearchCase::IgnoreCase, ESearchDir::FromEnd)), "/");
	}
	public:
	/**
	 * アセットパスから保存先のパッケージパスに変換 ※誤変換を避けるため、アセット生成以外で利用しないこと
	 * @param path アセットパス
	 * @return UEアセットパス(パッケージ)
	 * @throw InvalidArguments フルパスを指定
	 */
	static FString to_ue_save_package_path(const FString& path) {
		if (path.StartsWith("/")) {
			throw FDevCoreError(FString::Printf(TEXT("[Errors::InvalidArguments]: %s, %s"), TEXT("FDevAssetPaths::to_ue_save_package_path"), *path));
		}
		return FDevDSN::joined(FDevPackageConst::Game, path, "/");
	}
	public:
	/**
	 * UEアセットパス(パッケージ)から保存先のファイルパスに変換 ※誤変換を避けるため、アセット生成以外で利用しないこと
	 * @param ue_path UEアセットパス(パッケージ)
	 * @return ファイルパス
	 * @throw InvalidArguments 不正なパスを指定
	 */
	static FString to_ue_save_filepath(const FString& ue_path) {
		if (!ue_path.StartsWith(FDevPackageConst::Game)) {
			throw FDevCoreError(FString::Printf(TEXT("[Errors::InvalidArguments]: %s, %s"), TEXT("FDevAssetPaths::to_ue_save_filepath"), *ue_path));
		}
		return FPackageName::LongPackageNameToFilename(ue_path, FPackageName::GetAssetPackageExtension());
	}
	// endregion
	// region マスター
	public:
	/**
	 * アセットソースパスをアセットパス(マスター/内部)に変換
	 * @param domain アセットドメイン
	 * @param src アセットソースパス(ドメイン相対)
	 * @return アセットパス(マスター/内部)
	 */
	static FString to_master_internal(const FString& domain, const FString& src) {
		return FString::Printf(TEXT("%s#%s"), *domain, *src);
	}
	public:
	/**
	 * アセットパスからファイルパスに変換(マスター)
	 * @param path アセットパス
	 * @return ファイルパス(マスター)
	 */
	static FString to_master_filepath(const FString& path) {
		return FString::Printf(TEXT("Content/%s.json.data"), *path);
	}
	// endregion
};
