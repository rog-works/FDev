// @tranp.meta: {"version":"0.9.19","module":{"hash":"433aeb8e0b8ebb45156a79cc33ef2577","path":"FDev.Main.Core.Lang.Json.JsonParser"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Lang/String.h"
// #include "enum.h"
// #include "tranp/app/compatible/cpp/classes.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
/**
 * JSONエントリー種別
 */
enum class FDevJsonEntryTypes {
	Boolean = 0,
	Integer = 1,
	Float = 2,
	String = 3,
	Array = 4,
	Object = 5,
	Unknown = 6,
};
/**
 * Json解析情報
 */
class FDevJsonParseInfo {
	public:
	/**
	 * エントリー
	 */
	class Entry {
		public: FDevJsonEntryTypes entry_type;
		public: FString key;
		public: int depth;
		public: int begin;
		public: int end;
		public:
		/**
		 * インスタンスを生成
		 * @param entry_type Jsonエントリー種別
		 * @param key キー名
		 * @param depth 深度
		 * @param begin 読み取り開始位置
		 * @param end 読み取り終了位置
		 */
		Entry(FDevJsonEntryTypes entry_type, const FString& key, int depth, int begin, int end) : entry_type(entry_type), key(key), depth(depth), begin(begin), end(end) {}
	};
	public: TArray<Entry> entries;
	public:
	/**
	 * インスタンスを生成
	 */
	FDevJsonParseInfo() : entries() {}
};
/**
 * JSONパーサー
 */
class FDevJsonParser {
	public:
	/**
	 * JSON文字列を解析
	 * @param json_str JSON文字列
	 * @param info JSON解析情報
	 */
	static void parse(const FString& json_str, FDevJsonParseInfo* info) {
		FDevJsonParser::_parse_entry(json_str, 0, "", 0, info);
	}
	protected:
	/**
	 * JSON文字列を解析(エントリー)
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @param key キー名
	 * @param depth 深度
	 * @param info JSON解析情報
	 * @return 読み取り終了位置
	 */
	static int _parse_entry(const FString& json_str, int begin, const FString& key, int depth, FDevJsonParseInfo* info) {
		int end = begin;
		auto [at_type, begin_value] = FDevJsonParser::_analyze_type(json_str, begin);
		end = begin_value;
		if (at_type == FDevJsonEntryTypes::Boolean) {
			end = FDevJsonParser::_parse_boolean(json_str, begin_value, key, depth, info);
		} else if (at_type == FDevJsonEntryTypes::Float) {
			end = FDevJsonParser::_parse_float(json_str, begin_value, key, depth, info);
		} else if (at_type == FDevJsonEntryTypes::String) {
			end = FDevJsonParser::_parse_string(json_str, begin_value, key, depth, info);
		} else if (at_type == FDevJsonEntryTypes::Array) {
			end = FDevJsonParser::_parse_array(json_str, begin_value, key, depth, info);
		} else if (at_type == FDevJsonEntryTypes::Object) {
			end = FDevJsonParser::_parse_object(json_str, begin_value, key, depth, info);
		}
		return end;
	}
	protected:
	/**
	 * JSON文字列を解析(エントリー/Boolean)
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @param key キー名
	 * @param depth 深度
	 * @param info JSON解析情報
	 * @return 読み取り終了位置
	 */
	static int _parse_boolean(const FString& json_str, int begin, const FString& key, int depth, FDevJsonParseInfo* info) {
		if (json_str[begin] == 'f') {
			info->entries.Add(FDevJsonParseInfo::Entry(FDevJsonEntryTypes::Boolean, key, depth, begin, begin + 5));
			return begin + 5;
		} else {
			info->entries.Add(FDevJsonParseInfo::Entry(FDevJsonEntryTypes::Boolean, key, depth, begin, begin + 4));
			return begin + 4;
		}
	}
	protected:
	/**
	 * JSON文字列を解析(エントリー/Float)
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @param key キー名
	 * @param depth 深度
	 * @param info JSON解析情報
	 * @return 読み取り終了位置
	 */
	static int _parse_float(const FString& json_str, int begin, const FString& key, int depth, FDevJsonParseInfo* info) {
		FDevJsonEntryTypes entry_type = FDevJsonEntryTypes::Integer;
		int end = begin;
		while (end < json_str.Len()) {
			if (entry_type == FDevJsonEntryTypes::Integer && json_str[end] == '.') {
				entry_type = FDevJsonEntryTypes::Float;
			}
			end += 1;
			if (!FDevString::is_number(json_str, begin, end + 1)) {
				break;
			}
		}
		info->entries.Add(FDevJsonParseInfo::Entry(entry_type, key, depth, begin, end));
		return end;
	}
	protected:
	/**
	 * JSON文字列を解析(エントリー/String)
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @param key キー名
	 * @param depth 深度
	 * @param info JSON解析情報
	 * @return 読み取り終了位置
	 */
	static int _parse_string(const FString& json_str, int begin, const FString& key, int depth, FDevJsonParseInfo* info) {
		FString quote = "\"";
		int end = json_str.Find(quote, ESearchCase::IgnoreCase, ESearchDir::FromStart, begin);
		while (end < json_str.Len()) {
			int found = json_str.Find(quote, ESearchCase::IgnoreCase, ESearchDir::FromStart, end + 1);
			if (found == -1) {
				end = json_str.Len();
				break;
			}
			end = found;
			if (json_str[end - 1] != '\\') {
				break;
			}
		}
		info->entries.Add(FDevJsonParseInfo::Entry(FDevJsonEntryTypes::String, key, depth, begin, end + 1));
		return end + 1;
	}
	protected:
	/**
	 * JSON文字列を解析(エントリー/Array)
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @param key キー名
	 * @param depth 深度
	 * @param info JSON解析情報
	 * @return 読み取り終了位置
	 */
	static int _parse_array(const FString& json_str, int begin, const FString& key, int depth, FDevJsonParseInfo* info) {
		int info_begin = info->entries.Num();
		int end = json_str.Find(TEXT("["), ESearchCase::IgnoreCase, ESearchDir::FromStart, begin);
		end += 1;
		int element_at = 0;
		while (end < json_str.Len()) {
			auto [entry_type, block_end] = FDevJsonParser::_analyze_type(json_str, end, "]");
			if (entry_type == FDevJsonEntryTypes::Unknown || json_str[end] == ']') {
				end = FMath::Max(end, block_end);
				break;
			}
			end = FDevJsonParser::_parse_entry(json_str, end, LexToString(element_at), depth + 1, info);
			element_at += 1;
		}
		info->entries.Insert(FDevJsonParseInfo::Entry(FDevJsonEntryTypes::Array, key, depth, begin, end + 1), info_begin);
		return end + 1;
	}
	protected:
	/**
	 * JSON文字列を解析(エントリー/Object)
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @param key キー名
	 * @param depth 深度
	 * @param info JSON解析情報
	 * @return 読み取り終了位置
	 */
	static int _parse_object(const FString& json_str, int begin, const FString& key, int depth, FDevJsonParseInfo* info) {
		int info_begin = info->entries.Num();
		int end = json_str.Find(TEXT("{"), ESearchCase::IgnoreCase, ESearchDir::FromStart, begin);
		end += 1;
		while (end < json_str.Len()) {
			auto [entry_type, block_end] = FDevJsonParser::_analyze_type(json_str, end, "}");
			if (entry_type != FDevJsonEntryTypes::String || json_str[end] == '}') {
				end = FMath::Max(end, block_end);
				break;
			}
			auto [in_key, begin_value] = FDevJsonParser::_parse_key(json_str, end);
			end = FDevJsonParser::_parse_entry(json_str, begin_value, in_key, depth + 1, info);
		}
		info->entries.Insert(FDevJsonParseInfo::Entry(FDevJsonEntryTypes::Object, key, depth, begin, end + 1), info_begin);
		return end + 1;
	}
	protected:
	/**
	 * JSON文字列を解析(キー)
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @return キー, 読み取り終了位置
	 */
	static TTuple<FString, int> _parse_key(const FString& json_str, int begin) {
		int key_begin = json_str.Find(TEXT("\""), ESearchCase::IgnoreCase, ESearchDir::FromStart, begin);
		int end = json_str.Find(TEXT("\""), ESearchCase::IgnoreCase, ESearchDir::FromStart, key_begin + 1);
		FString key = json_str.Mid(key_begin + 1, end - (key_begin + 1));
		return {key, end + 1};
	}
	protected:
	/**
	 * JSONエントリーの種別を解析
	 * @param json_str JSON文字列
	 * @param begin 読み取り開始位置
	 * @param end_token 終端記号 (default = '')
	 * @return JSONエントリーの種別, 読み取り終了位置
	 */
	static TTuple<FDevJsonEntryTypes, int> _analyze_type(const FString& json_str, int begin, const FString& end_token = "") {
		int end = begin;
		while (end < json_str.Len()) {
			if (json_str[end] == 'f' || json_str[end] == 't') {
				return {FDevJsonEntryTypes::Boolean, end};
			} else if (json_str[end] == '"') {
				return {FDevJsonEntryTypes::String, end};
			} else if (json_str[end] == '[') {
				return {FDevJsonEntryTypes::Array, end};
			} else if (json_str[end] == '{') {
				return {FDevJsonEntryTypes::Object, end};
			} else if (FDevString::is_number(json_str, end, end + 1)) {
				return {FDevJsonEntryTypes::Float, end};
			} else if (end_token.Len() > 0 && json_str[end] == end_token[0]) {
				return {FDevJsonEntryTypes::Unknown, end};
			}
			end += 1;
		}
		return {FDevJsonEntryTypes::Unknown, -1};
	}
};
