// @tranp.meta: {"version":"0.9.19","module":{"hash":"96c40442bd8547e616ca330dc39c48af","path":"App.Main.Core.Lang.Convertion"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/Object.h"
#include "App/Main/Core/Core.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "compatible/error.h"
/**
 *
 * @param value_at 値(アドレス)
 * @return 値
 */
template<typename T>
T* safe_addr(T* value_at) {
	if (!value_at) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("safe_addr")));
	}
	return value_at;
}
/**
 *
 * @param value_at 値(弱参照)
 * @return 値
 */
template<typename T>
T* safe_weak(T* value_at) {
	if (!(value_at && value_at)) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("safe_weak")));
	}
	return value_at;
}
/**
 *
 * @param value_at 値(共有ポインター)
 * @return 値
 */
template<typename T>
TSharedPtr<T, ESPMode::NotThreadSafe> safe_shared(TSharedPtr<T, ESPMode::NotThreadSafe> value_at) {
	if (!value_at) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("safe_shared")));
	}
	return value_at;
}
/**
 *
 * @param obj 値(UObject)
 * @return 値
 */
template<typename T_Obj>
T_Obj* safe_obj(T_Obj* obj) {
	if (!(obj && IsValidChecked(obj))) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("safe_obj")));
	}
	return obj;
}
