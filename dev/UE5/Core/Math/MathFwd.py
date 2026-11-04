# @see Engine/Source/Runtime/Core/Public/Math/MathFwd.h

from typing import Annotated, ClassVar, Self

from numpy import atan2 as np_atan2
from numpy import linalg as np_linalg
from numpy import pi as np_pi
from numpy import power as np_pow
from numpy import sqrt as np_sqrt
from tranp.app.compatible.cpp.classes import double
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import GenStruct
from UE5.CoreUObject.UObject.ObjectMacros import UPROPERTY, USTRUCT, BlueprintType

PI = np_pi


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT(BlueprintType)
class Vector(GenStruct):
	"""ベクトル(3D/double)"""

	X: Annotated[double, UPROPERTY()]
	Y: Annotated[double, UPROPERTY()]
	Z: Annotated[double, UPROPERTY()]

	def __init__(self, x: float | double = 0.0, y: float | double = 0.0, z: float | double = 0.0) -> None:
		"""インスタンスを生成

		Args:
			x: X座標 (default = 0.0)
			y: Y座標 (default = 0.0)
			z: Z座標 (default = 0.0)
		"""
		self.X = double(x)
		self.Y = double(y)
		self.Z = double(z)

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: {self.ToString()}>'

	def __str__(self) -> str:
		"""Returns: シリアライズ表現"""
		return self.ToString()

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return hash((self.X, self.Y, self.Z))

	def __eq__(self, other: 'Vector | float | double') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector):
			return self.X == other.X and self.Y == other.Y and self.Z == other.Z
		else:
			return self.X == other and self.Y == other and self.Z == other

	def __ne__(self, other: 'Vector | float | double') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		return not self.__eq__(other)

	def __add__(self, other: 'Vector | float | double | int') -> 'Vector':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector):
			return Vector(self.X + other.X, self.Y + other.Y, self.Z + other.Z)
		else:
			return Vector(self.X + other, self.Y + other, self.Z + other)

	def __sub__(self, other: 'Vector | float | double | int') -> 'Vector':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector):
			return Vector(self.X - other.X, self.Y - other.Y, self.Z - other.Z)
		else:
			return Vector(self.X - other, self.Y - other, self.Z - other)

	def __mul__(self, other: 'Vector | float | double | int') -> 'Vector':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector):
			return Vector(self.X * other.X, self.Y * other.Y, self.Z * other.Z)
		else:
			return Vector(self.X * other, self.Y * other, self.Z * other)

	def __truediv__(self, other: 'Vector | float | double | int') -> 'Vector':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector):
			return Vector(self.X / other.X, self.Y / other.Y, self.Z / other.Z)
		else:
			return Vector(self.X / other, self.Y / other, self.Z / other)

	def Length(self) -> double:
		"""Returns: Sqrt"""
		return double(np_sqrt(self.X * self.X + self.Y * self.Y + self.Z * self.Z))

	def Normalize(self) -> None:
		"""単位ベクトル化"""
		normalized = self / float(np_linalg.norm(self.X, self.Y))
		self.X = normalized.X
		self.Y = normalized.Y
		self.Z = normalized.Z

	def ToString(self) -> str:
		"""str: 文字列表現"""
		return f'({self.X}, {self.Y}, {self.Z})'


@Embed.alias('FVector')
class Vector_:
	"""ベクトル(定数定義)"""

	UpVector: ClassVar = Vector(0.0, 0.0, 1.0)


@Embed.struct
@Embed.alias('FVector2f')
@Embed.ignore(GenStruct)
@USTRUCT()
class Vector2(GenStruct):
	"""ベクトル(2D/float)"""

	X: Annotated[float, UPROPERTY()]
	Y: Annotated[float, UPROPERTY()]

	def __init__(self, x: float | double = 0.0, y: float | double = 0.0) -> None:
		"""インスタンスを生成

		Args:
			x: X座標 (default = 0.0)
			y: Y座標 (default = 0.0)
		"""
		self.X = float(x)
		self.Y = float(y)

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: {self.ToString()}>'

	def __str__(self) -> str:
		"""Returns: シリアライズ表現"""
		return self.ToString()

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return hash((self.X, self.Y))

	def __eq__(self, other: 'Vector2 | float | double') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2):
			return self.X == other.X and self.Y == other.Y
		else:
			return self.X == other and self.Y == other

	def __ne__(self, other: 'Vector2 | float | double') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		return not self.__eq__(other)

	def __add__(self: Self, other: 'Vector2 | float | double | int') -> 'Self':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2):
			return self.__class__(self.X + other.X, self.Y + other.Y)
		else:
			return self.__class__(self.X + other, self.Y + other)

	def __sub__(self: Self, other: 'Vector2 | float | double | int') -> Self:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2):
			return self.__class__(self.X - other.X, self.Y - other.Y)
		else:
			return self.__class__(self.X - other, self.Y - other)

	def __mul__(self: Self, other: 'Vector2 | float | double | int') -> Self:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2):
			return self.__class__(self.X * other.X, self.Y * other.Y)
		else:
			return self.__class__(self.X * other, self.Y * other)

	def __truediv__(self: Self, other: 'Vector2 | float | double | int') -> Self:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2):
			return self.__class__(self.X / other.X, self.Y / other.Y)
		else:
			return self.__class__(self.X / other, self.Y / other)

	def Length(self) -> float:
		"""Returns: Sqrt"""
		return float(np_sqrt(self.X * self.X + self.Y * self.Y))

	def Normalize(self) -> None:
		"""単位ベクトル化"""
		normalized = self / float(np_linalg.norm(self.X, self.Y))
		self.X = normalized.X
		self.Y = normalized.Y

	def ToString(self) -> str:
		"""str: 文字列表現"""
		return f'({self.X}, {self.Y})'


@Embed.struct
@Embed.alias('F', prefix=True)
@USTRUCT()
class Vector2D(Vector2):
	"""ベクトル(2D/double)"""

	X: Annotated[double, UPROPERTY()]
	Y: Annotated[double, UPROPERTY()]

	def __init__(self, x: float | double = 0.0, y: float | double = 0.0) -> None:
		"""インスタンスを生成

		Args:
			x: X座標 (default = 0.0)
			y: Y座標 (default = 0.0)
		"""
		self.X = double(x)
		self.Y = double(y)

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: {self.ToString()}>'

	def __str__(self) -> str:
		"""Returns: シリアライズ表現"""
		return self.ToString()

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return hash((self.X, self.Y))

	def __eq__(self, other: 'Vector2D | float | double') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2D):
			return self.X == other.X and self.Y == other.Y
		else:
			return self.X == other and self.Y == other

	def __ne__(self, other: 'Vector2D | float | double') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		return not self.__eq__(other)

	def __add__(self: Self, other: 'Vector2D | float | double | int') -> 'Self':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2D):
			return self.__class__(self.X + other.X, self.Y + other.Y)
		else:
			return self.__class__(self.X + other, self.Y + other)

	def __sub__(self: Self, other: 'Vector2D | float | double | int') -> Self:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2D):
			return self.__class__(self.X - other.X, self.Y - other.Y)
		else:
			return self.__class__(self.X - other, self.Y - other)

	def __mul__(self: Self, other: 'Vector2D | float | double | int') -> Self:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2D):
			return self.__class__(self.X * other.X, self.Y * other.Y)
		else:
			return self.__class__(self.X * other, self.Y * other)

	def __truediv__(self: Self, other: 'Vector2D | float | double | int') -> Self:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, Vector2D):
			return self.__class__(self.X / other.X, self.Y / other.Y)
		else:
			return self.__class__(self.X / other, self.Y / other)

	def Length(self) -> double:
		"""Returns: Sqrt"""
		return double(np_sqrt(self.X * self.X + self.Y * self.Y))

	def Normalize(self) -> None:
		"""単位ベクトル化"""
		normalized = self / double(np_linalg.norm(self.X, self.Y))
		self.X = normalized.X
		self.Y = normalized.Y

	def ToString(self) -> str:
		"""str: 文字列表現"""
		return f'({self.X}, {self.Y})'


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class IntVector(GenStruct):
	"""ベクトル(3D/int)"""

	X: Annotated[int, UPROPERTY()]
	Y: Annotated[int, UPROPERTY()]
	Z: Annotated[int, UPROPERTY()]

	def __init__(self, x: int = 0, y: int = 0, z: int = 0) -> None:
		"""インスタンスを生成

		Args:
			x: X座標 (default = 0)
			y: Y座標 (default = 0)
			z: Z座標 (default = 0)
		"""
		self.X = int(x)
		self.Y = int(y)
		self.Z = int(z)

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: {self.ToString()}>'

	def __str__(self) -> str:
		"""Returns: シリアライズ表現"""
		return self.ToString()

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return hash((self.X, self.Y, self.Z))

	def __eq__(self, other: 'IntVector | int') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, IntVector):
			return self.X == other.X and self.Y == other.Y and self.Z == other.Z
		else:
			return self.X == other and self.Y == other and self.Z == other

	def __ne__(self, other: 'IntVector | int') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		return not self.__eq__(other)

	def __add__(self, other: 'IntVector | double | int') -> 'IntVector':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, IntVector):
			return IntVector(self.X + other.X, self.Y + other.Y, self.Z + other.Z)
		else:
			return IntVector(self.X + int(other), self.Y + int(other), self.Z + int(other))

	def __sub__(self, other: 'IntVector | double | int') -> 'IntVector':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, IntVector):
			return IntVector(self.X - other.X, self.Y - other.Y, self.Z - other.Z)
		else:
			return IntVector(self.X - int(other), self.Y - int(other), self.Z - int(other))

	def Length(self) -> int:
		"""Returns: Sqrt"""
		return int(np_sqrt(self.X * self.X + self.Y * self.Y + self.Z * self.Z))

	def ToString(self) -> str:
		"""str: 文字列表現"""
		return f'({self.X}, {self.Y}, {self.Z})'


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class IntVector2(GenStruct):
	"""ベクトル(2D/int)"""

	X: Annotated[int, UPROPERTY()]
	Y: Annotated[int, UPROPERTY()]

	def __init__(self, x: int = 0, y: int = 0) -> None:
		"""インスタンスを生成

		Args:
			x: X座標 (default = 0)
			y: Y座標 (default = 0)
		"""
		self.X = int(x)
		self.Y = int(y)

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: {self.ToString()}>'

	def __str__(self) -> str:
		"""Returns: シリアライズ表現"""
		return self.ToString()

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return hash((self.X, self.Y))

	def __eq__(self, other: 'IntVector2 | int') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, IntVector2):
			return self.X == other.X and self.Y == other.Y
		else:
			return self.X == other and self.Y == other

	def __ne__(self, other: 'IntVector2 | int') -> bool:
		"""Args: other: 対象 Returns: 結果"""
		return not self.__eq__(other)

	def __add__(self, other: 'IntVector2 | float | double | int') -> 'IntVector2':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, IntVector2):
			return IntVector2(self.X + other.X, self.Y + other.Y)
		else:
			return IntVector2(self.X + int(other), self.Y + int(other))

	def __sub__(self, other: 'IntVector2 | float | double | int') -> 'IntVector2':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, IntVector2):
			return IntVector2(self.X - other.X, self.Y - other.Y)
		else:
			return IntVector2(self.X - int(other), self.Y - int(other))

	def Length(self) -> int:
		"""Returns: Sqrt"""
		return int(np_sqrt(self.X * self.X + self.Y * self.Y))

	def ToString(self) -> str:
		"""str: 文字列表現"""
		return f'({self.X}, {self.Y})'


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class Rotator(GenStruct):
	"""ローテーター(double)"""

	Pitch: Annotated[double, UPROPERTY()]
	Yaw: Annotated[double, UPROPERTY()]
	Roll: Annotated[double, UPROPERTY()]

	def __init__(self, pitch: float | double = 0.0, yaw: float | double = 0.0, roll: float | double = 0.0) -> None:
		"""インスタンスを生成

		Args:
			pitch: Y軸回転 (default = 0.0)
			yew: Z軸回転 (default = 0.0)
			roll: X軸回転 (default = 0.0)
		"""
		self.Pitch = double(pitch)
		self.Yaw = double(yaw)
		self.Roll = double(roll)

	@Embed.alias('Vector')
	def ToVector(self) -> Vector:
		"""Returns: ベクトル Note: XXX Pythonでは(0.0)のベクトルを返却"""
		return Vector()


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class Quat(GenStruct):
	"""クオータニオン(double)"""

	X: Annotated[double, UPROPERTY()]
	Y: Annotated[double, UPROPERTY()]
	Z: Annotated[double, UPROPERTY()]
	W: Annotated[double, UPROPERTY()]

	def __init__(self, x: float | double = 0.0, y: float | double = 0.0, z: float | double = 0.0, w: float | double = 0.0) -> None:
		"""インスタンスを生成

		Args:
			x: X軸成分 (default = 0.0)
			y: Y軸成分 (default = 0.0)
			z: Z軸成分 (default = 0.0)
			w: W軸成分 (default = 0.0)
		"""
		self.X = double(x)
		self.Y = double(y)
		self.Z = double(z)
		self.W = double(w)


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class Transform(GenStruct):
	"""トランスフォーム"""

	Rotation: Annotated[Quat, UPROPERTY()]
	Translation: Annotated[Vector, UPROPERTY()]
	Scale3D: Annotated[Vector, UPROPERTY()]

	def __init__(self, rotation: Quat | None = None, translation: Vector | None = None, scale: Vector | None = None) -> None:
		"""インスタンスを生成

		Args:
			rotation: 回転 (default = None)
			translation: 座標 (default = None)
			scale: スケール (default = None)
		Note:
			XXX オブジェクトのデフォルト引数はバグの温床となるため設定禁止
		"""
		self.Rotation = rotation if rotation else Quat()
		self.Translation = translation if translation else Vector()
		self.Scale3D = scale if scale else Vector()

	def GetRotation(self) -> 'Quat':
		"""回転を取得

		Returns:
			回転
		"""
		return self.Rotation

	def GetTranslation(self) -> Vector:
		"""座標を取得

		Returns:
			座標
		"""
		return self.Translation

	def GetScale3D(self) -> Vector:
		"""スケールを取得

		Returns:
			スケール
		"""
		return self.Scale3D


@Embed.alias('F', prefix=True)
class Math:
	"""算術演算ユーティリティー @see Engine/Source/Runtime/Core/Public/Math/UnrealMathUtility.h"""

	@classmethod
	def Clamp(cls, value: float | double, v_min: float | double, v_max: float | double) -> float:
		"""値をクランプ

		Args:
			value: 値
			v_min: 最小値
			v_max: 最大値
		Returns:
			演算結果
		"""
		return min(v_max, max(v_min, value))

	@classmethod
	def Pow(cls, a: float | double, b: float | double) -> float:
		"""Power

		Args:
			a: 値(A)
			b: 値(B)
		Returns:
			演算結果
		"""
		return float(np_pow(a, b))

	# region 角度

	@classmethod
	def Atan2(cls, y: float | double, x: float | double) -> float:
		"""atan2

		Args:
			y: Y座標
			x: X座標
		Returns:
			ラジアン(-PI ~ 0 ~ PI)
		"""
		return float(np_atan2(y, x))

	@classmethod
	def DegreesToRadians(cls, degree: float | double) -> float:
		"""角度からラジアンに変換

		Args:
			degree: 角度(0 ~ 360)
		Returns:
			ラジアン(0 ~ PI * 2)
		"""
		return degree * PI / 180.0

	# endregion


@Embed.alias('F', prefix=True)
class Vector4:
	"""ベクトル(4次元) Note: XXX 現状、実装はない点に注意"""

	X: float
	Y: float
	Z: float
	W: float

	def __init__(self, vector: Vector | None = None, w: float = 0.0) -> None:
		"""インスタンスを生成

		Args:
			vector: ベクトル
			w: W軸
		"""
		self.X = vector.X if vector else 0.0
		self.Y = vector.Y if vector else 0.0
		self.Z = vector.Z if vector else 0.0
		self.W = w


@Embed.alias('F', prefix=True)
class IntRect:
	"""矩形(int)"""
	...


@Embed.alias('F', prefix=True)
class Matrix:
	"""行列"""

	def TransformFVector4(self, vector: Annotated[Vector4, Embed.immutable]) -> Vector4:
		"""行列変換 Args: vector: ベクトル Returns: 結果 XXX 実際の返却型はFPlaneだが、Pythonではオウム返しするためVector4で返却"""
		return vector
