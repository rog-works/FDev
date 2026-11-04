// @tranp.meta: {"version":"0.9.19","module":{"hash":"5fe70756d99154caef265cbcfb0e03c1","path":"FDev.Main.Core.Lang.String"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Misc/StringBuilder.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Core.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/classes.h"
// #include "tranp/app/compatible/python/embed.h"
/**
 * 文字列操作ユーティリティー
 */
class FDevString {
	protected: inline static char _Zero = '0';
	protected: inline static char _Nine = '9';
	protected: inline static char _a = 'a';
	protected: inline static char _z = 'z';
	protected: inline static char _A = 'A';
	protected: inline static char _Z = 'Z';
	protected: inline static char _Underscore = '_';
	protected: inline static char _Minus = '-';
	protected: inline static char _Dot = '.';
	protected: inline static char _Backslash = '\\';
	public:
	/**
	 * 指定の文字列が含まれる数を計測
	 * @param string 文字列
	 * @param subject カウント対象の文字列 ※UEの仕様上char型にするメリットが低いためstr型とする
	 * @return 含まれる数
	 * @note @see str.count
	 */
	static int count(const FString& string, const FString& subject) {
		int index = 0;
		int count = 0;
		int string_size = string.Len();
		int subject_size = subject.Len();
		while (index <= (string_size - subject_size)) {
			int found = string.Find(subject, ESearchCase::IgnoreCase, ESearchDir::FromStart, index);
			if (found == -1) {
				break;
			}
			index = found + subject_size;
			count += 1;
		}
		return count;
	}
	public:
	/**
	 * トリム(左)
	 * @param string 文字列
	 * @param chara 対象の文字
	 * @return トリム後の文字列
	 */
	static FString ltrim(const FString& string, char chara) {
		int found = -1;
		for (auto i = 0; i < string.Len(); i += 1) {
			if (string[i] != chara) {
				break;
			}
			found = i + 1;
		}
		if (found == string.Len()) {
			return "";
		}
		return found != -1 ? string.Mid(found, string.Len() - (found)) : string;
	}
	public:
	/**
	 * トリム(右)
	 * @param string 文字列
	 * @param chara 対象の文字
	 * @return トリム後の文字列
	 */
	static FString rtrim(const FString& string, char chara) {
		int found = -1;
		for (auto i = 0; i < string.Len(); i += 1) {
			int index = string.Len() - 1 - i;
			if (string[index] != chara) {
				break;
			}
			found = index;
		}
		if (found == 0) {
			return "";
		}
		return found != -1 ? string.Mid(0, found) : string;
	}
	public:
	/**
	 * トリム
	 * @param string 文字列
	 * @param chara 対象の文字
	 * @return トリム後の文字列
	 */
	static FString trim(const FString& string, char chara) {
		return FDevString::rtrim(FDevString::ltrim(string, chara), chara);
	}
	public:
	/**
	 * 文字列が数字か判定
	 * @param string 文字列
	 * @param begin 開始インデックス (default = -1)
	 * @param end 終了インデックス (default = -1)
	 * @return True = 数字
	 */
	static bool is_number(const FString& string, int begin = -1, int end = -1) {
		int length = string.Len();
		int _begin = FMath::Min(length, FMath::Max(0, begin));
		int _end = FMath::Min(length, FMath::Max(_begin, end != -1 ? end : length));
		for (auto index = _begin; index < _end; index += 1) {
			if (index == _begin && string[index] == FDevString::_Minus) {
				continue;
			} else if (string[index] >= FDevString::_Zero && string[index] <= FDevString::_Nine) {
				continue;
			} else if (string[index] == FDevString::_Dot) {
				continue;
			} else {
				return false;
			}
		}
		return true;
	}
	public:
	/**
	 * 文字列が名前か判定
	 * @param string 文字列
	 * @param begin 開始インデックス (default = -1)
	 * @param end 終了インデックス (default = -1)
	 * @return True = 名前
	 */
	static bool is_name(const FString& string, int begin = -1, int end = -1) {
		int length = string.Len();
		int _begin = FMath::Min(length, FMath::Max(0, begin));
		int _end = FMath::Min(length, FMath::Max(_begin, end != -1 ? end : length));
		for (auto index = _begin; index < _end; index += 1) {
			if ((index > _begin && string[index] >= FDevString::_Zero && string[index] <= FDevString::_Nine)) {
				continue;
			} else if ((string[index] >= FDevString::_a && string[index] <= FDevString::_z)) {
				continue;
			} else if ((string[index] >= FDevString::_A && string[index] <= FDevString::_Z)) {
				continue;
			} else if ((string[index] == FDevString::_Underscore)) {
				continue;
			} else {
				return false;
			}
		}
		return true;
	}
	public:
	/**
	 * 区切り文字で文字列のリストを結合
	 * @param strings 文字列リスト
	 * @param delimiter 区切り文字
	 * @return 結合後の文字列
	 * @note @see str.join
	 */
	static FString join(const TArray<FString>& strings, const FString& delimiter) {
		if (strings.Num() == 0) {
			return "";
		}
		TStringBuilder<256> builder{};
		for (auto i = 0; i < strings.Num(); i += 1) {
			if (i > 0) {
				builder.Append(delimiter);
				builder.Append(strings[i]);
			} else {
				builder.Append(strings[i]);
			}
		}
		return builder.ToString();
	}
	public:
	/**
	 * 区切り文字で文字列を分割する
	 * @param string 文字列
	 * @param delimiter 区切り文字
	 * @return 分割した文字列
	 * @note @see str.split
	 */
	static TArray<FString> split(const FString& string, const FString& delimiter) {
		TArray<FString> parts = {};
		int pos0 = 0;
		while (pos0 < string.Len()) {
			int pos1 = string.Find(delimiter, ESearchCase::IgnoreCase, ESearchDir::FromStart, pos0);
			if (pos1 == -1) {
				pos1 = string.Len();
			}
			parts.Add(string.Mid(pos0, pos1 - (pos0)));
			pos0 = pos1 + delimiter.Len();
		}
		// 対象の文字列が空文字、または末尾が区切り文字の場合は空文字を要素に追加する
		if (string.Len() == 0 || string.EndsWith(delimiter)) {
			parts.Add("");
		}
		return parts;
	}
	public:
	/**
	 * 文字列内の任意の文字に対してエスケープを施す
	 * @param string 対象
	 * @param chara エスケープ対象の文字
	 * @return エスケープ後の文字列
	 */
	static FString escape(const FString& string, char chara) {
		FString target = FString("") + chara;
		if (FDevString::count(string, target) == 0 && FDevString::count(string, "\\") == 0) {
			return string;
		}
		TStringBuilder<256> builder{};
		int begin = 0;
		int end = begin;
		while (end < string.Len()) {
			if (string[end] == chara || string[end] == FDevString::_Backslash) {
				builder.Append(string.Mid(begin, end - (begin)));
				builder.AppendChar(FDevString::_Backslash);
				builder.AppendChar(string[end]);
				begin = end + 1;
			}
			end += 1;
		}
		if (begin < end) {
			builder.Append(string.Mid(begin, end - (begin)));
		}
		return builder.ToString();
	}
	public:
	/**
	 * 文字列内のエスケープを解除する
	 * @param string 対象
	 * @return エスケープ解除後の文字列
	 */
	static FString unescape(const FString& string) {
		if (FDevString::count(string, "\\") == 0) {
			return string;
		}
		TStringBuilder<256> builder{};
		int begin = 0;
		FString escape = "\\";
		while (begin < string.Len()) {
			int end = string.Find(escape, ESearchCase::IgnoreCase, ESearchDir::FromStart, begin);
			if (end == -1) {
				builder.Append(string.Mid(begin, string.Len() - (begin)));
				break;
			}
			builder.Append(string.Mid(begin, end - (begin)));
			builder.AppendChar(string[end + 1]);
			begin = end + 2;
		}
		return builder.ToString();
	}
	public:
	/**
	 * 文字コードから文字に変換
	 * @param code 文字コード(Unicode)
	 * @return 文字
	 * @note FStringにUnicodeの私用領域(0xFxxx)を直接渡すと文字化けするためTCHARを中継して変換
	 */
	static FString from_code(int code) {
		return FString("") + TCHAR(code);
	}
	// class_method find_strict
	public:
	/**
	 * 指定の文字列との前方一致
	 * @param string 文字列
	 * @param suffix 接尾辞
	 * @param begin 開始インデックス (default = 0)
	 * @param end 終了インデックス (default = 0)
	 * @return True = 一致
	 * @note
	 * ```
	 * * CaseSensitive版。通常の用途ではstr.startswithの使用を推奨
	 * * 開始/終了インデックスの負の値には対応しない
	 * @see str.endswith
	 * ```
	 */
	static bool startswith_strict(const FString& string, const FString& prefix, int begin = 0, int end = 0) {
		if (begin < end && end > 0) {
			return FDevString::find_strict(string, prefix, begin, end) == begin;
		} else if (begin > 0 && end == 0) {
			return FDevString::find_strict(string, prefix, begin) == begin;
		} else {
			return FDevString::find_strict(string, prefix, 0) == 0;
		}
	}
	public:
	/**
	 * 指定の文字列との後方一致
	 * @param string 文字列
	 * @param suffix 接尾辞
	 * @param begin 開始インデックス (default = 0)
	 * @param end 終了インデックス (default = 0)
	 * @return True = 一致
	 * @note
	 * ```
	 * * CaseSensitive版。通常の用途ではstr.endswithの使用を推奨
	 * * 開始/終了インデックスの負の値には対応しない
	 * @see str.endswith
	 * ```
	 */
	static bool endswith_strict(const FString& string, const FString& suffix, int begin = 0, int end = 0) {
		if (begin < end && end > 0) {
			int expect_at = FMath::Max(begin, end - suffix.Len());
			return FDevString::find_strict(string, suffix, expect_at, end) == expect_at;
		} else if (begin > 0 && end == 0) {
			int expect_at = FMath::Max(begin, string.Len() - suffix.Len());
			return FDevString::find_strict(string, suffix, expect_at) == expect_at;
		} else {
			int expect_at = FMath::Max(0, string.Len() - suffix.Len());
			return FDevString::find_strict(string, suffix, expect_at) == expect_at;
		}
	}
	public:
	/**
	 * 指定の文字列が含まれる数を計測
	 * @param string 文字列
	 * @param subject カウント対象の文字列
	 * @param begin 開始インデックス (default = 0)
	 * @param end 終了インデックス (default = 0)
	 * @return 含まれる数
	 * @note
	 * ```
	 * * CaseSensitive版。通常の用途ではstr.countの使用を推奨
	 * * 開始/終了インデックスの負の値には対応しない
	 * @see count
	 * ```
	 */
	static int count_strict(const FString& string, const FString& subject, int begin = 0, int end = 0) {
		int index = begin;
		int count = 0;
		int string_size = end == 0 ? string.Len() : end;
		int subject_size = subject.Len();
		while (index <= (string_size - subject_size)) {
			int found = FDevString::find_strict(string, subject, index, string_size);
			if (found == -1) {
				break;
			}
			index = found + subject_size;
			count += 1;
		}
		return count;
	}
	// class_method replace_strict
	public:
	/**
	 * 文字列を置換
	 * @param string 文字列
	 * @param delimiter 区切り文字
	 * @return 文字列リスト
	 * @note
	 * ```
	 * * CaseSensitive版。通常の用途ではstr.splitの使用を推奨
	 * @see split
	 * ```
	 */
	static TArray<FString> split_strict(const FString& string, const FString& delimiter) {
		TArray<FString> parts = {};
		int pos0 = 0;
		while (pos0 < string.Len()) {
			int pos1 = FDevString::find_strict(string, delimiter, pos0);
			if (pos1 == -1) {
				pos1 = string.Len();
			}
			parts.Add(string.Mid(pos0, pos1 - (pos0)));
			pos0 = pos1 + delimiter.Len();
		}
		// 対象の文字列が空文字、または末尾が区切り文字の場合は空文字を要素に追加する
		if (string.Len() == 0 || FDevString::endswith_strict(string, delimiter)) {
			parts.Add("");
		}
		return parts;
	}
};
