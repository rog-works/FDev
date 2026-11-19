// @tranp.meta: {"version":"0.9.24","module":{"hash":"33bd7847761df45f6c35b3573bebcf3a","path":"App.Main.Core.Lang.IO.Files"},"transpiler":{"version":"0.9.11","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Containers/StringConv.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/BufferArchive.h"
#include "App/Main/Core/Core.h"
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
	static bool exists(const FString& filepath) {
		FString abs_filepath = FPaths::Combine(FPaths::ProjectDir(), filepath);
		return FPaths::FileExists(abs_filepath);
	}
	public:
	/**
	 * ファイルを保存
	 * @param filepath ファイルパス (プロジェクトルートからの相対パス)
	 * @param content コンテンツ
	 * @return True = 保存成功
	 */
	static bool save(const FString& filepath, const FString& content) {
		FString abs_filepath = FPaths::Combine(FPaths::ProjectDir(), filepath);
		int size_8 = FTCHARToUTF8_Convert::ConvertedLength((*content), content.Len());
		FBufferArchive buff_8{};
		buff_8.SetNumZeroed(size_8);
		FTCHARToUTF8_Convert::Convert(reinterpret_cast<UTF8CHAR*>((buff_8.GetData())), size_8, (*content), content.Len());
		return FFileHelper::SaveArrayToFile(buff_8, (*abs_filepath));
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
		FBufferArchive buff{};
		if (!FFileHelper::LoadFileToArray(buff, (*abs_filepath))) {
			throw FDevCoreError(FString::Printf(TEXT("[Errors::NotFound]: %s, %s"), TEXT("FDevFiles::load"), *abs_filepath));
		}
		return FDevFiles::p__to_str(buff);
	}
	// class_method p__to_str
	private:
	/**
	 *
	 * @param buff バイト配列
	 * @return 変換後の文字列
	 */
	static FString p__to_str(FBufferArchive& buff) {
		buff.Add(uint8(0));
		return UTF8_TO_TCHAR(reinterpret_cast<UTF8CHAR*>((buff.GetData())));
	}
};
