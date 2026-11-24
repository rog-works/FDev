// @tranp.meta: {"version":"0.9.25","module":{"hash":"70938c0d265f3cf2249277268c733a6e","path":"App.Main.Core.CoreError"},"transpiler":{"version":"0.9.12","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
// #include "typing.h"
// #include "tranp/app/compatible/python/embed.h"
/**
 * 例外(アプリケーション)
 * @note
 * ```
 * * トランスパイル後に参照されるクラスのため、Python上は原則使用禁止
 * @see compatible.error.CompatibleError
 * @see data/template/statement/throw.j2
 * ```
 */
class CoreError : public std::exception {
	using std::exception::exception;
	private: FString p__message;
	public:
	/**
	 * インスタンスを生成
	 * @param message エラーメッセージ
	 */
	CoreError(const FString& message) : exception(), p__message(message) {}
	public:
	/**
	 *
	 * @return エラーメッセージ @immutable
	 */
	const FString& message() const {
		return this->p__message;
	}
};
