// @tranp.meta: {"version":"0.9.19","module":{"hash":"8deb5356e998110e3d0a7d44f4c1b3e6","path":"FDev.Main.Core.CoreError"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "FDev/Main/Const/ProjectConst.h"
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
class FDevCoreError : public std::exception {
	using std::exception::exception;
	private: FString __message;
	public:
	/**
	 * インスタンスを生成
	 * @param message エラーメッセージ
	 */
	FDevCoreError(const FString& message) : exception(), __message(message) {}
	public:
	/**
	 *
	 * @return エラーメッセージ @immutable
	 */
	const FString& message() const {
		return this->__message;
	}
};
