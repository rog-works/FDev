// @tranp.meta: {"version":"0.9.19","module":{"hash":"f5cacc04b9e917b169eb5f90495e7bf8","path":"FDev.Main.Core.Lang.Convertion"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/Object.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Core.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// #include "compatible/error.h"
/**
 *
 * @param value_at 値(アドレス)
 * @return 値
 */
template<typename T>
T* FDevsafe_addr(T* value_at) {
	if (!value_at) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("FDevsafe_addr")));
	}
	return value_at;
}
/**
 *
 * @param value_at 値(弱参照)
 * @return 値
 */
template<typename T>
T* FDevsafe_weak(T* value_at) {
	if (!(value_at && value_at)) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("FDevsafe_weak")));
	}
	return value_at;
}
/**
 *
 * @param value_at 値(共有ポインター)
 * @return 値
 */
template<typename T>
TSharedPtr<T, ESPMode::NotThreadSafe> FDevsafe_shared(TSharedPtr<T, ESPMode::NotThreadSafe> value_at) {
	if (!value_at) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("FDevsafe_shared")));
	}
	return value_at;
}
/**
 *
 * @param obj 値(UObject)
 * @return 値
 */
template<typename T_Obj>
T_Obj* FDevsafe_obj(T_Obj* obj) {
	if (!(obj && IsValidChecked(obj))) {
		throw CoreError(FString::Printf(TEXT("[Errors::AccessViolation]: %s"), TEXT("FDevsafe_obj")));
	}
	return obj;
}
