// @tranp.meta: {"version":"0.9.19","module":{"hash":"e3242c7ef1f9e987fbd21e8bde6ba00d","path":"FDev.Main.Core.Lang.DSN.DSN"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Core.h"
// #include "typing.h"
// #include "tranp/app/compatible/python/embed.h"
/**
 * DSN(Dot Separator Name)
 */
class FDevDSN {
	public: inline static FString Delimiter = ".";
	public:
	/**
	 * 関連があるか判定(要素単位で前方一致、または同じ)
	 * @param base パス(基準)
	 * @param path パス(比較対象)
	 * @param delimiter 区切り文字 (default = '.')
	 * @return True = 適合
	 */
	static bool is_association(const FString& base, const FString& path, const FString& delimiter = Delimiter) {
		if (base.Len() > path.Len()) {
			return false;
		} else if (base.Len() == 0) {
			return true;
		} else if (base == path) {
			return true;
		}
		int base_count = FDevDSN::count(base, delimiter);
		if (base_count > FDevDSN::count(path, delimiter)) {
			return false;
		} else if (!path.StartsWith(base)) {
			return false;
		}
		FString base_tail = FDevDSN::pick(base, base_count - 1, delimiter);
		FString path_head = FDevDSN::pick(path, base_count - 1, delimiter);
		return base_tail == path_head;
	}
	public:
	/**
	 * 配下要素か判定
	 * @param base パス(基準)
	 * @param path パス(比較対象)
	 * @param delimiter 区切り文字 (default = '.')
	 * @return True = 適合
	 */
	static bool is_under(const FString& base, const FString& path, const FString& delimiter = Delimiter) {
		return FDevDSN::count(base, delimiter) + 1 == FDevDSN::count(path, delimiter) && FDevDSN::is_association(base, path);
	}
	public:
	/**
	 * 要素数を取得
	 * @param path パス
	 * @param delimiter 区切り文字 (default = '.')
	 * @return 要素数
	 */
	static int count(const FString& path, const FString& delimiter = Delimiter) {
		return path.Len() == 0 ? 0 : FDevString::count(path, delimiter) + 1;
	}
	public:
	/**
	 * パスから要素リストに分解
	 * @param path パス
	 * @param delimiter 区切り文字 (default = '.')
	 * @return 要素リスト
	 */
	static TArray<FString> elements(const FString& path, const FString& delimiter = Delimiter) {
		if (path.Len() == 0) {
			return {};
		} else {
			return FDevString::split(path, delimiter);
		}
	}
	public:
	/**
	 * パス/要素を連結してパスを生成
	 * @param elems パス/要素リスト
	 * @param delimiter 区切り文字 (default = '.')
	 * @return 連結したパス
	 */
	static FString join(const TArray<FString>& elems, const FString& delimiter = Delimiter) {
		return FDevString::join(elems, delimiter);
	}
	public:
	/**
	 * パスを連結
	 * @param a パスA
	 * @param b パスB
	 * @param delimiter 区切り文字 (default = '.')
	 * @return 連結したパス
	 */
	static FString joined(const FString& a, const FString& b, const FString& delimiter = Delimiter) {
		if (a.Len() == 0) {
			return b;
		} else if (b.Len() == 0) {
			return a;
		} else {
			return a + delimiter + b;
		}
	}
	public:
	/**
	 * 指定位置の要素を取得
	 * @param path パス
	 * @param index インデックス
	 * @param delimiter 区切り文字 (default = '.')
	 * @return 要素
	 */
	static FString pick(const FString& path, int index, const FString& delimiter = Delimiter) {
		if (path.Len() == 0) {
			return "";
		}
		int begin = 0;
		for (auto i = 0; i < index + 1; i += 1) {
			int end = path.Find(delimiter, ESearchCase::IgnoreCase, ESearchDir::FromStart, begin);
			if (i == index && end == -1) {
				return path.Mid(begin, path.Len() - (begin));
			} else if (end == -1) {
				return "";
			} else if (i == index) {
				return path.Mid(begin, end - (begin));
			}
			begin = end + 1;
		}
		return "";
	}
	public:
	/**
	 * 先頭の要素を取得
	 * @param path パス
	 * @param delimiter 区切り文字 (default = '.')
	 * @return 要素
	 */
	static FString first(const FString& path, const FString& delimiter = Delimiter) {
		return FDevDSN::pick(path, 0, delimiter);
	}
	public:
	/**
	 * 末尾の要素を取得
	 * @param path パス
	 * @param delimiter 区切り文字 (default = '.')
	 * @return 要素
	 */
	static FString last(const FString& path, const FString& delimiter = Delimiter) {
		if (path.Len() == 0 || FDevString::count(path, delimiter) == 0) {
			return path;
		}
		int begin = path.Find(delimiter, ESearchCase::IgnoreCase, ESearchDir::FromEnd) + 1;
		return path.Mid(begin, path.Len() - (begin));
	}
	public:
	/**
	 * パスを左から詰める(先頭 -> 末尾)
	 * @param path パス
	 * @param count 要素数
	 * @param delimiter 区切り文字 (default = '.')
	 * @return パス
	 */
	static FString pad_left(const FString& path, int count, const FString& delimiter = Delimiter) {
		if (FDevString::count(path, delimiter) < count) {
			return "";
		}
		int begin = 0;
		for (auto _ = 0; _ < count; _ += 1) {
			begin = path.Find(delimiter, ESearchCase::IgnoreCase, ESearchDir::FromStart, begin) + 1;
		}
		return path.Mid(begin, path.Len() - (begin));
	}
	public:
	/**
	 * パスを右から詰める(末尾 -> 先頭)
	 * @param path パス
	 * @param count 要素数
	 * @param delimiter 区切り文字 (default = '.')
	 * @return パス
	 */
	static FString pad_right(const FString& path, int count, const FString& delimiter = Delimiter) {
		if (FDevString::count(path, delimiter) < count) {
			return "";
		}
		int end = path.Len() - 1;
		for (auto _ = 0; _ < count; _ += 1) {
			end = path.Find(delimiter, ESearchCase::IgnoreCase, ESearchDir::FromEnd, end) - 1;
		}
		return path.Mid(0, end + 1);
	}
	public:
	/**
	 * パスを指定方向から詰める(+: 左, -: 右)
	 * @param path パス
	 * @param shift シフト数
	 * @param delimiter 区切り文字 (default = '.')
	 * @return パス
	 */
	static FString padding(const FString& path, int shift, const FString& delimiter = Delimiter) {
		if (shift > 0) {
			return FDevDSN::pad_left(path, shift, delimiter);
		} else if (shift < 0) {
			return FDevDSN::pad_right(path, -shift, delimiter);
		} else {
			return path;
		}
	}
};
