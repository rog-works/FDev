// @tranp.meta: {"version":"0.9.19","module":{"hash":"a69f03c5ace6eae81ccb849ba771464e","path":"App.Main.Core.Lang.Json.Json"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "Misc/StringBuilder.h"
#include "UObject/Object.h"
#include "UObject/ObjectMacros.h"
#include "App/Main/Const/ProjectConst.h"
#include "App/Main/Core/Lang/DSN/DSN.h"
#include "App/Main/Core/Lang/Json/JsonEntry.h"
#include "App/Main/Core/Lang/Json/JsonParser.h"
#include "App/Main/Core/Lang/String.h"
#include "App/Main/Core/Core.h"
#include "Json.generated.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/classes.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/cvar.h"
// #include "compatible/error.h"
/**
 * JSON
 * @note
 * ```
 * ### 留意事項
 * * 文字列は2重引用符以外のエスケープを行わない (外部入力の文字列を扱うのは基本的にNG)
 * * 数値は10進数のみ扱う
 * * 配列の要素挿入は出来ず、追加のみ対応
 * * オブジェクトのみキーリストを管理
 * ### メンバー変数としての公開は禁止
 * * 理由: 初期状態が不確定になり、安全性を担保出来なくなるため @see UE5.CoreUObject.UObject.Object.UObject.post_init_properties
 * * Jsonのコピーは非常に軽量なため、過剰な回避策を実装するより、関数を通して共有する方が遥かに安価で安全
 * ```
 */
USTRUCT()
struct FDEV_API FFDevJson {
	GENERATED_BODY()
	public: inline static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> EmptyEntry = FDevJsonEntry::new_empty();
	public: FDevJsonEntry* cursor;
	public:
	/**
	 * インスタンスを生成
	 * @param entry JSONエントリー | None (default = None)
	 */
	FFDevJson(FDevJsonEntry* entry = nullptr) : cursor(entry ? entry : (FFDevJson::EmptyEntry).Get()) {}
	// method __repr__
	public:
	/**
	 *
	 * @return 文字列表現
	 */
	FString ToString() const {
		if (this->is_scalar()) {
			return FString::Printf(TEXT("<Json[%s]: %s%s @ %p>"), *this->type_name(), *this->serialize(), *FString(this->cursor->read_only ? " readonly" : ""), this->cursor);
		} else {
			return FString::Printf(TEXT("<Json[%s]: [%d]%s @ %p>"), *this->type_name(), this->length(), *FString(this->cursor->read_only ? " readonly" : ""), this->cursor);
		}
	}
	// region ファクトリー
	public:
	/**
	 * JSON文字列を基にインスタンスを生成(読み取り専用)
	 * @param json_str JSON文字列
	 * @return JSONエントリー
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> parse(const FString& json_str) {
		FDevJsonParseInfo info{};
		FDevJsonParser::parse(json_str, (&(info)));
		TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> returned = FDevJsonEntry::new_entry(info.entries[0].entry_type, true, true);
		returned->build_entry(json_str, info, 0);
		return returned;
	}
	public:
	/**
	 *
	 * @param value 値, read_only: True = 読み取り専用 (default = False)
	 * @return JSONエントリー
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_bool(bool value, bool read_only = false) {
		TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> returned = FDevJsonEntry::new_entry(FDevJsonEntryTypes::Boolean, true, read_only);
		returned->set_bool(value);
		return returned;
	}
	public:
	/**
	 *
	 * @param value 値, read_only: True = 読み取り専用 (default = False)
	 * @return JSONエントリー
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_int(int value, bool read_only = false) {
		TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> returned = FDevJsonEntry::new_entry(FDevJsonEntryTypes::Integer, true, read_only);
		returned->set_int(value);
		return returned;
	}
	public:
	/**
	 *
	 * @param value 値, read_only: True = 読み取り専用 (default = False)
	 * @return JSONエントリー
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_float(float value, bool read_only = false) {
		TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> returned = FDevJsonEntry::new_entry(FDevJsonEntryTypes::Float, true, read_only);
		returned->set_float(value);
		return returned;
	}
	public:
	/**
	 *
	 * @param value 値, read_only: True = 読み取り専用 (default = False)
	 * @return JSONエントリー
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_string(const FString& value, bool read_only = false) {
		TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> returned = FDevJsonEntry::new_entry(FDevJsonEntryTypes::String, true, read_only);
		// XXX unescapeした文字列を保持するのが正なのでescapeはしないこと
		returned->set_string(value);
		return returned;
	}
	public:
	/**
	 *
	 * @param value 値
	 * @return JSONエントリー
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_array() {
		return FDevJsonEntry::new_entry(FDevJsonEntryTypes::Array, true, false);
	}
	public:
	/**
	 *
	 * @param value 値
	 * @return JSONエントリー
	 */
	static TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_object() {
		return FDevJsonEntry::new_entry(FDevJsonEntryTypes::Object, true, false);
	}
	// endregion
	// region スキーマ
	public:
	/**
	 *
	 * @return True = 空データ
	 */
	bool is_empty() const {
		return this->cursor == (FFDevJson::EmptyEntry).Get();
	}
	public:
	/**
	 *
	 * @return True = ルートオブジェクト
	 */
	bool is_root() const {
		return this->cursor->is_root;
	}
	public:
	/**
	 *
	 * @return True = 読み取り専用
	 */
	bool read_only() const {
		return this->cursor->read_only;
	}
	public:
	/**
	 *
	 * @return JSONエントリー種別
	 */
	FDevJsonEntryTypes entry_type() const {
		return this->cursor->entry_type;
	}
	public:
	/**
	 *
	 * @return True = Array/Object
	 */
	bool iterable() const {
		return this->cursor->entry_type == FDevJsonEntryTypes::Array || this->cursor->entry_type == FDevJsonEntryTypes::Object;
	}
	public:
	/**
	 *
	 * @return True = スカラー型
	 */
	bool is_scalar() const {
		return !this->iterable();
	}
	public:
	/**
	 *
	 * @return True = Boolean
	 */
	bool is_bool() const {
		return this->cursor->entry_type == FDevJsonEntryTypes::Boolean;
	}
	public:
	/**
	 *
	 * @return True = Integer
	 */
	bool is_int() const {
		return this->cursor->entry_type == FDevJsonEntryTypes::Integer;
	}
	public:
	/**
	 *
	 * @return True = Float
	 */
	bool is_float() const {
		return this->cursor->entry_type == FDevJsonEntryTypes::Float;
	}
	public:
	/**
	 *
	 * @return True = String
	 */
	bool is_string() const {
		return this->cursor->entry_type == FDevJsonEntryTypes::String;
	}
	public:
	/**
	 *
	 * @return True = Array
	 */
	bool is_array() const {
		return this->cursor->entry_type == FDevJsonEntryTypes::Array;
	}
	public:
	/**
	 *
	 * @return True = Object
	 */
	bool is_object() const {
		return this->cursor->entry_type == FDevJsonEntryTypes::Object;
	}
	public:
	/**
	 *
	 * @return 型の名前 @immutable @test
	 */
	const FString& type_name() const {
		static TMap<FDevJsonEntryTypes, FString> to_type_names = {
			{FDevJsonEntryTypes::Boolean, "bool"},
			{FDevJsonEntryTypes::Integer, "int"},
			{FDevJsonEntryTypes::Float, "float"},
			{FDevJsonEntryTypes::String, "String"},
			{FDevJsonEntryTypes::Array, "Array"},
			{FDevJsonEntryTypes::Object, "FDevJson"},
		};
		return to_type_names[this->cursor->entry_type];
	}
	// endregion
	// region 要素参照
	public:
	/**
	 * 配下要素を取得
	 * @param key 要素キー
	 * @return インスタンス
	 * @throw NotAllowed Array/Object以外で使用
	 * @throw OutOfBounds 存在しないエントリーを指定
	 */
	FFDevJson operator[](const FString& key) const {
		return this->by(key);
	}
	public:
	/**
	 *
	 * @return 配下要素の数
	 * @throw NotAllowed Array/Object以外で実行
	 */
	int length() const {
		if (!this->iterable()) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::length()"), *(*this).ToString()));
		}
		return this->cursor->length();
	}
	public:
	/**
	 *
	 * @return キーリスト @immutable
	 * @throw NotAllowed Object以外で使用
	 */
	const TArray<FString>& keys() const {
		if (this->cursor->entry_type != FDevJsonEntryTypes::Object) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::keys()"), *(*this).ToString()));
		}
		return this->cursor->keys;
	}
	public:
	/**
	 *
	 * @return 配下要素リスト
	 * @throw NotAllowed Array/Object以外で使用
	 */
	TArray<FFDevJson> entries() {
		if (!this->iterable()) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::entries()"), *(*this).ToString()));
		}
		return [&]() -> TArray<FFDevJson> {
			TArray<FFDevJson> __ret;
			for (auto& entry : this->cursor->entries) {
				__ret.Add(FFDevJson((entry).Get()));
			}
			return __ret;
		}();
	}
	public:
	/**
	 * 指定のJSONパスを持つ要素が存在するか判定
	 * @param jsonpath JSONパス
	 * @return True = 存在
	 */
	bool exists(const FString& jsonpath) const {
		TArray<FString> routes = FDevDSN::elements(jsonpath);
		FDevJsonEntry* cursor = this->cursor;
		for (auto i = 0; i < routes.Num(); i += 1) {
			FFDevJson curr{cursor};
			if (curr.has_key(routes[i])) {
				return false;
			}
			cursor = curr.by(routes[i]).cursor;
		}
		return true;
	}
	public:
	/**
	 * 指定のキーを持つ配下要素が存在するか判定
	 * @param key キー
	 * @return True = 存在
	 * @throw NotAllowed Array/Object以外で使用
	 */
	bool has_key(const FString& key) const {
		if (this->cursor->entry_type == FDevJsonEntryTypes::Array) {
			return String::is_number(key) && FCString::Atoi(*key) >= 0 && FCString::Atoi(*key) < this->length();
		} else if (this->cursor->entry_type == FDevJsonEntryTypes::Object) {
			return this->cursor->keys.Contains(key);
		} else {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::has_key"), *(*this).ToString()));
		}
	}
	public:
	/**
	 * 指定位置のキーを取得
	 * @param index インデックス
	 * @return キー
	 * @throw NotAllowed Array/Object以外で使用
	 * @throw OutOfBounds 存在しないエントリーを指定
	 */
	FString key_at(int index) const {
		if (this->cursor->entry_type == FDevJsonEntryTypes::Array) {
			return LexToString(index);
		} else if (this->cursor->entry_type == FDevJsonEntryTypes::Object) {
			return this->cursor->keys[index];
		} else {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::key_at"), *(*this).ToString()));
		}
	}
	public:
	/**
	 * 配下要素を取得
	 * @param index インデックス
	 * @return インスタンス
	 * @throw NotAllowed Array/Object以外で使用
	 * @throw OutOfBounds 存在しないエントリーを指定
	 */
	FFDevJson at(int index) const {
		if (!this->iterable()) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::at"), *(*this).ToString()));
		}
		return FFDevJson((this->cursor->entries[index]).Get());
	}
	public:
	/**
	 * 配下要素を取得
	 * @param key シンボル名
	 * @return インスタンス
	 * @throw NotAllowed Array/Object以外で使用
	 * @throw OutOfBounds 存在しないエントリーを指定
	 */
	FFDevJson by(const FString& key) const {
		if (this->cursor->entry_type == FDevJsonEntryTypes::Array) {
			return FFDevJson((this->cursor->entries[FCString::Atoi(*key)]).Get());
		} else if (this->cursor->entry_type == FDevJsonEntryTypes::Object) {
			int index = this->cursor->keys.Find(key);
			return FFDevJson((this->cursor->entries[index]).Get());
		} else {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::by"), *(*this).ToString()));
		}
	}
	public:
	/**
	 * JSONパスと一致するエントリーを取得
	 * @param jsonpath JSONパス
	 * @return インスタンス
	 * @throw OutOfBounds 存在しないエントリーを指定
	 */
	FFDevJson fetch(const FString& jsonpath) {
		TArray<FString> routes = FDevDSN::elements(jsonpath);
		FDevJsonEntry* cursor = this->cursor;
		for (auto i = 0; i < routes.Num(); i += 1) {
			cursor = FFDevJson(cursor).by(routes[i]).cursor;
		}
		return FFDevJson(cursor);
	}
	// endregion
	// region 実体参照
	public:
	/**
	 *
	 * @return カーソルのアドレスID
	 */
	uint64 cursor_id() {
		return (uint64((this->cursor)));
	}
	public:
	/**
	 *
	 * @return 実体のアドレス
	 */
	void* entity_at() {
		if (this->cursor->entry_type == FDevJsonEntryTypes::Boolean) {
			return (&(this->cursor->as_bool));
		} else if (this->cursor->entry_type == FDevJsonEntryTypes::Integer) {
			return (&(this->cursor->as_int));
		} else if (this->cursor->entry_type == FDevJsonEntryTypes::Float) {
			return (&(this->cursor->as_float));
		} else if (this->cursor->entry_type == FDevJsonEntryTypes::String) {
			return (&(this->cursor->as_string));
		} else {
			return (this);
		}
	}
	public:
	/**
	 *
	 * @return 値
	 * @throw NotAllowed Boolean以外で使用
	 */
	bool as_bool() {
		if (this->cursor->entry_type != FDevJsonEntryTypes::Boolean) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::as_bool()"), *(*this).ToString()));
		}
		return this->cursor->as_bool;
	}
	public:
	/**
	 *
	 * @return 値
	 * @throw NotAllowed Integer以外で使用
	 */
	int as_int() {
		if (this->cursor->entry_type != FDevJsonEntryTypes::Integer) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::as_int()"), *(*this).ToString()));
		}
		return this->cursor->as_int;
	}
	public:
	/**
	 *
	 * @return 値
	 * @throw NotAllowed Float以外で使用
	 */
	float as_float() {
		if (this->cursor->entry_type != FDevJsonEntryTypes::Float) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::as_float()"), *(*this).ToString()));
		}
		return this->cursor->as_float;
	}
	public:
	/**
	 *
	 * @return 値 @immutable
	 * @throw NotAllowed String以外で使用
	 */
	const FString& as_string() {
		if (this->cursor->entry_type != FDevJsonEntryTypes::String) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::as_string()"), *(*this).ToString()));
		}
		return this->cursor->as_string;
	}
	// endregion
	// region 要素更新
	public:
	/**
	 * 値を更新
	 * @param value 値 @immutable
	 * @throw NotAllowed 読み取り専用
	 */
	template<typename T_Value>
	void set_value(const T_Value& value) {
		if (this->cursor->read_only) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::set_value"), *(*this).ToString()));
		}
		if constexpr (std::is_same_v<T_Value, bool>) {
			this->cursor->set_bool(value);
		} else if constexpr (std::is_same_v<T_Value, int>) {
			this->cursor->set_int(value);
		} else if constexpr (std::is_same_v<T_Value, float>) {
			this->cursor->set_float(value);
		} else if constexpr (std::is_same_v<T_Value, FString>) {
			this->cursor->set_string(value);
		} else if constexpr (std::is_same_v<T_Value, FFDevJson>) {
			this->cursor->copy_value(static_cast<FFDevJson>(value).cursor);
		} else if constexpr (std::is_same_v<T_Value, TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>>) {
			this->cursor->copy_value((static_cast<TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>>(value)).Get());
		} else {
			static_assert(std::is_same_v<T_Value, void>, "Unmatch type");
		}
	}
	public:
	/**
	 * 配列の要素を追加/反映
	 * @param index インデックス value: 値 @immutable
	 * @throw NotAllowed 読み取り専用
	 * @throw NotAllowed Array以外で使用
	 * @throw InvalidArguments 対象外のインデックスを指定
	 * @note XXX CSP[JsonEntry]を指定した場合はisolateせずそのまま登録する
	 */
	template<typename T_Value>
	void apply_at(int index, const T_Value& value) {
		if (this->cursor->read_only) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::apply_at"), *(*this).ToString()));
		} else if (this->cursor->entry_type != FDevJsonEntryTypes::Array) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::apply_at"), *(*this).ToString()));
		} else if (!(index >= 0 && index <= this->length() + 1)) {
			throw CoreError(FString::Printf(TEXT("[Errors::InvalidArguments]: %s, %s, %d"), TEXT("FFDevJson::apply_at"), *(*this).ToString(), index));
		}
		if (index < this->length()) {
			this->at(index).set_value(value);
			return;
		}
		if constexpr (std::is_same_v<T_Value, bool>) {
			this->cursor->append(FFDevJson::new_bool(value));
		} else if constexpr (std::is_same_v<T_Value, int>) {
			this->cursor->append(FFDevJson::new_int(value));
		} else if constexpr (std::is_same_v<T_Value, float>) {
			this->cursor->append(FFDevJson::new_float(value));
		} else if constexpr (std::is_same_v<T_Value, FString>) {
			this->cursor->append(FFDevJson::new_string(value));
		} else if constexpr (std::is_same_v<T_Value, FFDevJson>) {
			this->cursor->append(static_cast<FFDevJson>(value).cursor->isolate(this->read_only()));
		} else if constexpr (std::is_same_v<T_Value, TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>>) {
			TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_entry = static_cast<TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>>(value);
			new_entry->freeze(this->read_only());
			this->cursor->append(new_entry);
		} else {
			static_assert(std::is_same_v<T_Value, void>, "Unmatch type");
		}
	}
	public:
	/**
	 * オブジェクトの要素を追加/反映
	 * @param key キー value: 値 @immutable
	 * @throw NotAllowed 読み取り専用
	 * @throw NotAllowed Object以外で使用
	 * @note XXX CSP[JsonEntry]を指定した場合はisolateせずそのまま登録する
	 */
	template<typename T_Value>
	void apply_of(const FString& key, const T_Value& value) {
		if (this->cursor->read_only) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::apply_of"), *(*this).ToString()));
		} else if (this->cursor->entry_type != FDevJsonEntryTypes::Object) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::apply_of"), *(*this).ToString()));
		}
		if (this->has_key(key)) {
			this->by(key).set_value(value);
			return;
		}
		if constexpr (std::is_same_v<T_Value, bool>) {
			this->cursor->join(key, FFDevJson::new_bool(value));
		} else if constexpr (std::is_same_v<T_Value, int>) {
			this->cursor->join(key, FFDevJson::new_int(value));
		} else if constexpr (std::is_same_v<T_Value, float>) {
			this->cursor->join(key, FFDevJson::new_float(value));
		} else if constexpr (std::is_same_v<T_Value, FString>) {
			this->cursor->join(key, FFDevJson::new_string(value));
		} else if constexpr (std::is_same_v<T_Value, FFDevJson>) {
			this->cursor->join(key, static_cast<FFDevJson>(value).cursor->isolate(this->read_only()));
		} else if constexpr (std::is_same_v<T_Value, TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>>) {
			TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> new_entry = static_cast<TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe>>(value);
			new_entry->freeze(this->read_only());
			this->cursor->join(key, new_entry);
		} else {
			static_assert(std::is_same_v<T_Value, void>, "Unmatch type");
		}
	}
	public:
	/**
	 * 読み取り設定を変更
	 * @param on True = 読み取り専用 (default = True)
	 * @throw NotAllowed ルート要素以外で使用
	 */
	void freeze(bool on = true) {
		if (!this->is_root()) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::freeze"), *(*this).ToString()));
		}
		this->cursor->freeze(on);
	}
	// endregion
	// region 要素削除
	public:
	/**
	 * 配列の指定インデックスを削除
	 * @param index インデックス
	 * @throw NotAllowed 読み取り専用
	 * @throw NotAllowed Array以外で使用
	 * @throw OutOfBounds 存在しないエントリーを指定
	 */
	void remove_at(int index) {
		if (this->cursor->read_only) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::remove_at"), *(*this).ToString()));
		} else if (this->cursor->entry_type != FDevJsonEntryTypes::Array) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::remove_at"), *(*this).ToString()));
		}
		this->cursor->remove_at(index);
	}
	public:
	/**
	 * オブジェクトの指定キーを削除
	 * @param key キー
	 * @throw NotAllowed 読み取り専用
	 * @throw NotAllowed Object以外で使用
	 * @throw OutOfBounds 存在しないエントリーを指定
	 */
	void remove_of(const FString& key) {
		if (this->cursor->read_only) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::remove_of"), *(*this).ToString()));
		} else if (this->cursor->entry_type != FDevJsonEntryTypes::Object) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::remove_of"), *(*this).ToString()));
		}
		this->cursor->remove_of(key);
	}
	public:
	/**
	 * 配下要素を全て削除
	 * @throw NotAllowed 読み取り専用
	 */
	void clear() {
		if (this->cursor->read_only) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::clear"), *(*this).ToString()));
		}
		this->cursor->clear();
	}
	// endregion
	// region 複製
	public:
	/**
	 * 自身を基点に複製。読み取り属性は接続先に依存。接続先が無い場合は自身の設定を引き継ぐ
	 * @param owner 接続先のインスタンス | None (default = None)
	 * @return JSONエントリー
	 */
	TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> isolate(FFDevJson* owner = nullptr) {
		return this->cursor->isolate(owner ? owner->read_only() : this->cursor->read_only);
	}
	// endregion
	// region シリアライズ
	public:
	/**
	 * JSONシリアライズ
	 * @return JSONエントリー
	 */
	TSharedPtr<FDevJsonEntry, ESPMode::NotThreadSafe> to_json() {
		return this->cursor->isolate(this->read_only());
	}
	public:
	/**
	 * JSONデシリアライズ
	 * @param json JSON
	 * @throw NotAllowed 読み取り専用
	 */
	void from_json(FFDevJson json) {
		if (this->cursor->read_only) {
			throw CoreError(FString::Printf(TEXT("[Errors::NotAllowed]: %s, %s"), TEXT("FFDevJson::from_json"), *(*this).ToString()));
		}
		this->cursor->copy_value(json.cursor);
	}
	public:
	/**
	 *
	 * @return JSON文字列
	 */
	FString serialize() const {
		TStringBuilder<256> builder{};
		this->__build_string(this->cursor, (&(builder)));
		return builder.ToString();
	}
	private:
	/**
	 *
	 * @param entry JSON, builder: ストリングビルダー
	 */
	static void __build_string(FDevJsonEntry* entry, TStringBuilder<256>* builder) {
		if (entry->entry_type == FDevJsonEntryTypes::Boolean) {
			builder->Append(entry->as_bool ? "true" : "false");
		} else if (entry->entry_type == FDevJsonEntryTypes::Integer) {
			builder->Append(LexToString(entry->as_int));
		} else if (entry->entry_type == FDevJsonEntryTypes::Float) {
			builder->Append(LexToString(entry->as_float));
		} else if (entry->entry_type == FDevJsonEntryTypes::String) {
			builder->Append("\"");
			builder->Append(String::escape(entry->as_string, '"'));
			builder->Append("\"");
		} else if (entry->entry_type == FDevJsonEntryTypes::Array) {
			builder->Append("[");
			int index = 0;
			for (auto& in_entry : entry->entries) {
				if (index > 0) {
					builder->Append(",");
				}
				FFDevJson::__build_string((in_entry).Get(), builder);
				index++;
			}
			builder->Append("]");
		} else {
			builder->Append("{");
			int index = 0;
			for (auto& in_entry : entry->entries) {
				if (index > 0) {
					builder->Append(",");
				}
				builder->Append("\"");
				builder->Append(entry->keys[index]);
				builder->Append("\":");
				FFDevJson::__build_string((in_entry).Get(), builder);
				index++;
			}
			builder->Append("}");
		}
	}
	// endregion
};
