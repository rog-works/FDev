from tranp.app.compatible.cpp.cvar import CP, CSP, CW
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import IsValidChecked, UObject

from compatible.error import Errors
from FDev.Main.Const.ProjectConst import Aliases


@Embed.alias(Aliases.General.value, prefix=True)
def safe_addr[T](value_at: CP[T] | None) -> CP[T]:
	"""Args: value_at: 値(アドレス) Returns: 値 Raises: AccessViolation"""
	if not value_at:
		raise Errors.AccessViolation(safe_addr)

	return value_at


@Embed.alias(Aliases.General.value, prefix=True)
def safe_weak[T](value_at: CW[T] | None) -> CP[T]:
	"""Args: value_at: 値(弱参照) Returns: 値 Raises: AccessViolation"""
	if not (value_at and value_at.addr):
		raise Errors.AccessViolation(safe_weak)

	return value_at.addr


@Embed.alias(Aliases.General.value, prefix=True)
def safe_shared[T](value_at: CSP[T] | None) -> CSP[T]:
	"""Args: value_at: 値(共有ポインター) Returns: 値 Raises: AccessViolation"""
	if not value_at:
		raise Errors.AccessViolation(safe_shared)

	return value_at


@Embed.alias(Aliases.General.value, prefix=True)
def safe_obj[T_Obj: UObject](obj: CW[T_Obj] | None) -> CP[T_Obj]:
	"""Args: obj: 値(UObject) Returns: 値 Raises: AccessViolation"""
	if not (obj and IsValidChecked(obj.addr)):
		raise Errors.AccessViolation(safe_obj)

	return obj.addr
