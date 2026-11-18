// @tranp.meta: {"version":"0.9.23","module":{"hash":"5871ef28617cd4d63ec5ed5296c4e49e","path":"App.Main.Core.Logs"},"transpiler":{"version":"0.9.10","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include <functional>
// #include "enum.h"
// #include "typing.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/enum.h"
// #include "helper/env/py_environ.h"
/**
 * ロガー
 */
class FDevLogs {
	/**
	 * ログ出力フラグ
	 * @note XXX 最上位バイトを使うとC++でコンパイルエラーになるため使用禁止
	 */
	public: enum class FDevFlags {
		asset = 0x00000002,
		editor = 0x00000800,
		all = 0x0fffffff,
	};
	/**
	 * ログの入出力先
	 */
	public: enum class FDevDestinations {
		defaults = 0x0001,
		all = 0xffff,
	};
	public: inline static bool enabled = true;
	private: inline static int p__dest_in = (int(FDevDestinations::defaults));
	private: inline static int p__dest_out = (int(FDevDestinations::defaults));
	private: inline static int p__flags = (int(FDevFlags::all));
	// region 出力フラグ管理
	// class_method ok
	public:
	/**
	 *
	 * @param flag ログ出力フラグ
	 * @return True = 出力有効
	 * @note @cpp
	 */
	static bool ok(FDevFlags flag) {
		return FDevLogs::enabled && (FDevLogs::p__dest_in & FDevLogs::p__dest_out) != 0 && (FDevLogs::p__flags & (int(flag))) != 0;
	}
	public:
	/**
	 *
	 * @param destination 入力元
	 * @return True = 出力有効
	 */
	static bool dest_in_ok(FDevDestinations destination) {
		return (FDevLogs::p__dest_in & (int(destination))) != 0;
	}
	public:
	/**
	 * 入力元追加
	 * @param destination 入力元
	 */
	static void dest_in_on(FDevDestinations destination) {
		FDevLogs::p__dest_in |= (int(destination));
	}
	public:
	/**
	 * 入力元削除
	 * @param destination 入力元
	 */
	static void dest_in_off(FDevDestinations destination) {
		FDevLogs::p__dest_in &= ~(int(destination));
	}
	public:
	/**
	 * 出力先変更
	 * @param destination 出力先 (default = defaults)
	 */
	static void dest_out(FDevDestinations destination = FDevDestinations::defaults) {
		FDevLogs::p__dest_out = (int(destination));
	}
	public:
	/**
	 *
	 * @param flag ログ出力フラグ
	 * @return True = 出力有効(個別)
	 */
	static bool flag_ok(FDevFlags flag) {
		return (FDevLogs::p__flags & (int(flag))) != 0;
	}
	public:
	/**
	 * 出力追加
	 * @param flag ログ出力フラグ
	 */
	static void on(FDevFlags flag) {
		FDevLogs::p__flags |= (int(flag));
	}
	public:
	/**
	 * 出力削除
	 * @param flag ログ出力フラグ
	 */
	static void off(FDevFlags flag) {
		FDevLogs::p__flags &= ~(int(flag));
	}
	// endregion
	// region ログ出力
	// class_method warning
	// class_method error
	// class_method asset
	// class_method editor
	// class_method p__put
	// endregion
};
