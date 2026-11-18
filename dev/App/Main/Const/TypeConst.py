from enum import Enum

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UENUM


@Embed.alias('E', prefix=True)
@UENUM()
class Classifications(Enum):
	"""型の種別"""
	Unknown = 0
	Scalar = 1
	Array = 2
	Map = 3
	Struct = 4
	Object = 5
	Function = 6
	TypeVar = 7


@Embed.alias('E', prefix=True)
@UENUM()
class Scalars(Enum):
	"""値型の種別"""
	NoScalar = 0
	Boolean = 1
	Byte = 2
	Integer = 3
	Int64 = 4
	Float = 5
	Double = 6
	String = 7
	Name = 8
	Text = 9
