// @tranp.meta: {"version":"0.9.19","module":{"hash":"335ab90c3cca0ce89e6d0b67e8841f19","path":"FDev.Main.Core.Lang.IO.File"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Containers/StringConv.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Core.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/classes.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "tranp/app/lang/convertion.h"
// #include "compatible/error.h"
/**
 * ファイル操作ヘルパー
 */
class FDevFiles {
	public:
	/**
	 * ファイルが存在するか判定
	 * @param filepath ファイルパス (プロジェクトルートからの相対パス)
	 * @return True = 存在
	 */
	static bool exiets(const FString& filepath) {
		FString abs_filepath = FPaths::Combine(FPaths::ProjectDir(), filepath);
		return FPaths::FileExists(abs_filepath);
	}
	public:
	/**
	 * ファイルを読み込み
	 * @param filepath ファイルパス (プロジェクトルートからの相対パス)
	 * @return コンテンツ
	 * @throw NotFound ファイルが存在しない
	 */
	static FString load(const FString& filepath) {
		FString abs_filepath = FPaths::Combine(FPaths::ProjectDir(), filepath);
		TArray<uint8> buffer = FDevFiles::__make_buffer();
		TArray<uint8>& output = buffer;
		bool ok = FFileHelper::LoadFileToArray(output, (*abs_filepath));
		if (!ok) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotFound]: %s, %s"), TEXT("FDevFiles::load"), *abs_filepath));
		}
		return FDevFiles::__to_str(output);
	}
	// class_method __make_buffer
	private:
	/**
	 *
	 * @return バイト配列
	 */
	static TArray<uint8> __make_buffer() {
		return {};
	}
	// class_method __to_str
	private:
	/**
	 *
	 * @param output 出力
	 * @return 変換後の文字列
	 */
	static FString __to_str(TArray<uint8>& output) {
		output.Add(static_cast<uint8>(0));
		return UTF8_TO_TCHAR(reinterpret_cast<const char*>((output).GetData()));
	}
};
