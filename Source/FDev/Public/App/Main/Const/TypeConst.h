// @tranp.meta: {"version":"0.9.24","module":{"hash":"1e3ce69844a3c14fc6159d251f0e5946","path":"App.Main.Const.TypeConst"},"transpiler":{"version":"0.9.11","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/ObjectMacros.h"
#include "TypeConst.generated.h"
// #include "enum.h"
// #include "tranp/app/compatible/python/embed.h"
/**
 * 型の種別
 */
UENUM()
enum class EFDevClassifications : uint8 {
	Unknown = 0,
	Scalar = 1,
	Array = 2,
	Map = 3,
	Struct = 4,
	Object = 5,
	Function = 6,
	TypeVar = 7,
};
/**
 * 値型の種別
 */
UENUM()
enum class EFDevScalars : uint8 {
	NoScalar = 0,
	Boolean = 1,
	Byte = 2,
	Integer = 3,
	Int64 = 4,
	Float = 5,
	Double = 6,
	String = 7,
	Name = 8,
	Text = 9,
};
