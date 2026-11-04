// @tranp.meta: {"version":"0.9.19","module":{"hash":"9309682daba5026f2711e81b5f73d93a","path":"FDev.Main.Core.Lang.Json.JsonEntry"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Lang/Json/JsonParser.h"
#include "FDev/Main/Core/Lang/String.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/classes.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
/**
 * JSONエントリー
 */
class FDevJsonEntry {
	public: FDevJsonEntryTypes entry_type;
	public: bool is_root;
	public: bool read_only;
	public: bool as_bool;
	public: int as_int;
	public: float as_float;
	public: FString as_string;
	public: TArray<FString> keys;
	public: TArray<TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>> entries;
	public:
	/**
	 * インスタンスを生成
	 * @param is_root True = ルート要素 (default = False)
	 * @param read_only True = 読み取り専用 (default = False)
	 */
	FDevJsonEntry(bool is_root = false, bool read_only = false) : entry_type(FDevJsonEntryTypes::Boolean), is_root(is_root), read_only(read_only), as_bool(false), as_int(0), as_float(0.0f), as_string(""), keys(), entries() {}
	// method __repr__
	// region ファクトリー
	public:
	/**
	 * インスタンスを生成
	 * @param entry_type JSONエントリー種別
	 * @param is_root True = ルート要素
	 * @param read_only True = 読み取り専用
	 * @return インスタンス
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_entry(FDevJsonEntryTypes entry_type, bool is_root, bool read_only) {
		TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> instance = MakeShared<FDevJsonEntry, ESPMode::NotThreadSafe>(is_root, read_only);
		instance->entry_type = entry_type;
		return instance;
	}
	public:
	/**
	 *
	 * @return インスタンス(空)
	 * @note 外部からはJson.EmptyEntryを使用
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_empty() {
		return FDevJsonEntry::new_entry(FDevJsonEntryTypes::Object, true, true);
	}
	// endregion
	// region スキーマ
	public:
	/**
	 *
	 * @return 配下要素の数
	 * @note Array/Object専用
	 */
	int length() const {
		return this->entries.Num();
	}
	// endregion
	// region セッター
	public:
	/**
	 *
	 * @param value 値
	 */
	void set_bool(bool value) {
		this->clear();
		this->entry_type = FDevJsonEntryTypes::Boolean;
		this->as_bool = value;
	}
	public:
	/**
	 *
	 * @param value 値
	 */
	void set_int(int value) {
		this->clear();
		this->entry_type = FDevJsonEntryTypes::Integer;
		this->as_int = value;
	}
	public:
	/**
	 *
	 * @param value 値
	 */
	void set_float(float value) {
		this->clear();
		this->entry_type = FDevJsonEntryTypes::Float;
		this->as_float = value;
	}
	public:
	/**
	 *
	 * @param value 値
	 */
	void set_string(const FString& value) {
		this->clear();
		this->entry_type = FDevJsonEntryTypes::String;
		this->as_string = value;
	}
	// endregion
	// region 要素追加・削除
	public:
	/**
	 * エントリーを追加(Array専用)
	 * @param entry インスタンス
	 */
	void append(TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> entry) {
		entry->is_root = false;
		this->entries.Add(entry);
	}
	public:
	/**
	 * エントリーを追加(Object専用)
	 * @param key エントリー名
	 * @param entry インスタンス
	 */
	void join(const FString& key, TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> entry) {
		entry->is_root = false;
		this->keys.Add(key);
		this->entries.Add(entry);
	}
	public:
	/**
	 * エントリーを削除(Array専用)
	 * @param index インデックス
	 */
	void remove_at(int index) {
		this->entries.RemoveAt(index);
	}
	public:
	/**
	 * エントリーを削除(Object専用)
	 * @param key エントリー名
	 */
	void remove_of(const FString& key) {
		int index = this->keys.Find(key);
		this->keys.RemoveAt(index);
		this->entries.RemoveAt(index);
	}
	public:
	/**
	 * エントリーを初期化
	 */
	void clear() {
		this->as_bool = false;
		this->as_int = 0;
		this->as_float = 0.0f;
		this->as_string = "";
		this->keys.Empty();
		this->entries.Empty();
	}
	// endregion
	// region 構築・複製
	public:
	/**
	 * 読み取り設定を変更(ルート要素専用)
	 * @param on True = 読み取り専用 (default = True)
	 */
	void freeze(bool on = true) {
		this->read_only = on;
		for (auto& entry : this->entries) {
			entry->freeze(on);
		}
	}
	public:
	/**
	 * 自身を基点に複製
	 * @param read_only True = 読み取り専用
	 * @return インスタンス
	 */
	TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> isolate(bool read_only) {
		TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> returned = FDevJsonEntry::new_entry(this->entry_type, true, read_only);
		returned->copy_value((this));
		return returned;
	}
	public:
	/**
	 * 解析情報を基にインスタンスを構築
	 * @param json_str JSON文字列
	 * @param info JSON解析情報 @immutable
	 * @param index 処理インデックス
	 * @return 進行ステップ数
	 */
	int build_entry(const FString& json_str, const FDevJsonParseInfo& info, int index) {
		FDevJsonEntryTypes entry_type = info.entries[index].entry_type;
		int begin = info.entries[index].begin;
		int end = info.entries[index].end;
		if (entry_type == FDevJsonEntryTypes::Boolean) {
			this->set_bool(json_str.Mid(begin, end - (begin)) == "true");
			return 1;
		} else if (entry_type == FDevJsonEntryTypes::Integer) {
			// XXX マスターデータのカラーコード用に32bit最上位バイトの対応
			this->set_int(static_cast<int>(FCString::Atoi64(*json_str.Mid(begin, end - (begin)))));
			return 1;
		} else if (entry_type == FDevJsonEntryTypes::Float) {
			this->set_float(FCString::Atof(*json_str.Mid(begin, end - (begin))));
			return 1;
		} else if (entry_type == FDevJsonEntryTypes::String) {
			this->set_string(FDevString::unescape(json_str.Mid(begin + 1, end - 1 - (begin + 1))));
			return 1;
		}
		int step = 1;
		int depth = info.entries[index].depth;
		while (index + step < info.entries.Num()) {
			int in_index = index + step;
			if (depth + 1 != info.entries[in_index].depth) {
				break;
			}
			TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> in_entry = FDevJsonEntry::new_entry(info.entries[in_index].entry_type, false, true);
			int in_step = in_entry->build_entry(json_str, info, in_index);
			if (this->entry_type == FDevJsonEntryTypes::Array) {
				this->append(in_entry);
			} else {
				this->join(info.entries[in_index].key, in_entry);
			}
			step += in_step;
		}
		return step;
	}
	public:
	/**
	 * 複製元の値をディープコピー。read_onlyは自身の設定を伝搬
	 * @param from_entry 複製元
	 */
	void copy_value(FDevJsonEntry* from_entry) {
		if (this->entry_type != from_entry->entry_type) {
			this->clear();
		}
		if (from_entry->entry_type == FDevJsonEntryTypes::Boolean) {
			this->set_bool(from_entry->as_bool);
		} else if (from_entry->entry_type == FDevJsonEntryTypes::Integer) {
			this->set_int(from_entry->as_int);
		} else if (from_entry->entry_type == FDevJsonEntryTypes::Float) {
			this->set_float(from_entry->as_float);
		} else if (from_entry->entry_type == FDevJsonEntryTypes::String) {
			this->set_string(from_entry->as_string);
		} else if (from_entry->entry_type == FDevJsonEntryTypes::Array) {
			this->entry_type = FDevJsonEntryTypes::Array;
			this->__resize_array(from_entry);
			for (auto index = 0; index < from_entry->length(); index += 1) {
				this->entries[index]->copy_value((from_entry->entries[index]).Get());
			}
		} else {
			this->entry_type = FDevJsonEntryTypes::Object;
			this->__resize_object(from_entry);
			for (auto index = 0; index < from_entry->length(); index += 1) {
				this->entries[index]->copy_value((from_entry->entries[index]).Get());
			}
		}
	}
	private:
	/**
	 * 複製元に合わせてリサイズ(Array)
	 * @param from_entry 複製元
	 */
	void __resize_array(FDevJsonEntry* from_entry) {
		int curr_size = this->length();
		int next_size = from_entry->length();
		if (curr_size < next_size) {
			for (auto i = 0; i < next_size - curr_size; i += 1) {
				int index = curr_size + i;
				TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> add_entry = FDevJsonEntry::new_entry(from_entry->entries[index]->entry_type, false, this->read_only);
				this->append(add_entry);
			}
		} else if (curr_size > next_size) {
			for (auto i = 0; i < curr_size - next_size; i += 1) {
				this->entries.RemoveAt(next_size);
			}
		}
	}
	private:
	/**
	 * 複製元に合わせてリサイズ(Object)
	 * @param from_entry 複製元
	 */
	void __resize_object(FDevJsonEntry* from_entry) {
		int curr_size = this->length();
		int next_size = from_entry->length();
		if (curr_size < next_size) {
			for (auto i = 0; i < next_size - curr_size; i += 1) {
				int index = curr_size + i;
				TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> add_entry = FDevJsonEntry::new_entry(from_entry->entries[index]->entry_type, false, this->read_only);
				this->join(from_entry->keys[index], add_entry);
			}
		} else if (curr_size > next_size) {
			for (auto i = 0; i < curr_size - next_size; i += 1) {
				this->entries.RemoveAt(next_size);
				this->keys.RemoveAt(next_size);
			}
		}
	}
	// endregion
};
