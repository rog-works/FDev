# @see Engine/Source/Runtime/Core/Public/Math/Color.h

from typing import Annotated, ClassVar

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import GenStruct
from UE5.CoreUObject.UObject.ObjectMacros import UPROPERTY, USTRUCT


@Embed.struct
@Embed.alias('F', prefix=True)
class Color:
	"""カラー(int版)

	Note:
		* RGB値からsRGBに変換(?)
		* ピクセルバッファにのみ使用する予定があった ※備忘録
	"""

	R: int
	G: int
	B: int
	A: int

	def __init__(self, r: int, g: int, b: int, a: int = 255) -> None:
		"""インスタンスを生成

		Args:
			r: 赤
			g: 緑
			b: 青
			a: α値 (default = 255)
		"""
		self.R = r
		self.G = g
		self.B = b
		self.A = a


@Embed.struct
@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class LinearColor(GenStruct):
	"""リニアカラー"""

	R: Annotated[float, UPROPERTY()]
	G: Annotated[float, UPROPERTY()]
	B: Annotated[float, UPROPERTY()]
	A: Annotated[float, UPROPERTY()]

	def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0, a: float = 0.0) -> None:
		"""インスタンスを生成

		Args:
			r: R (default = 0.0)
			g: G (default = 0.0)
			b: B (default = 0.0)
			a: A (default = 0.0)
		"""
		self.R = r
		self.G = g
		self.B = b
		self.A = a

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: {str(self)}>'

	def __str__(self) -> str:
		"""Returns: 文字列表現"""
		value = int(self.R * 255) << 24 | int(self.G * 255) << 16 | int(self.B * 255) << 8 | int(self.A * 255)
		code = hex(value)[2:]
		return '0x{fill}{code}'.format(fill='0' * (8 - len(code)), code=code)

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return hash((self.R, self.G, self.B, self.A))

	def __eq__(self, other: 'LinearColor') -> bool:
		"""Args: other: 対象 Returns: True = 一致"""
		return other.R == self.R and other.G == self.G and other.B == self.B and other.A == self.A

	def __ne__(self, other: 'LinearColor') -> bool:
		"""Args: other: 対象 Returns: True = 相違"""
		return not self.__eq__(other)

	def __add__(self, other: 'float | LinearColor') -> 'LinearColor':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, LinearColor):
			return LinearColor(self.R + other.R, self.G + other.G, self.B + other.B, self.A + other.A)
		else:
			return LinearColor(self.R + other, self.G + other, self.B + other, self.A + other)

	def __mul__(self, other: 'float | LinearColor') -> 'LinearColor':
		"""Args: other: 対象 Returns: 結果"""
		if isinstance(other, LinearColor):
			return LinearColor(self.R * other.R, self.G * other.G, self.B * other.B, self.A * other.A)
		else:
			return LinearColor(self.R * other, self.G * other, self.B * other, self.A * other)

	@classmethod
	def FromSRGBColor(cls, color: Color) -> 'LinearColor':
		"""sRGBを元にインスタンスを生成

		Args:
			color: カラー(sRGB)
		Returns:
			インスタンス
		"""
		return cls(color.R / 255.0, color.G / 255.0, color.B / 255.0, color.A / 255.0)

	@classmethod
	def LerpUsingHSV(cls, a: Annotated['LinearColor', Embed.immutable], b: Annotated['LinearColor', Embed.immutable], alpha: float) -> 'LinearColor':
		"""AからBに線形補完

		Args:
			a: 色(A) @immutable
			b: 色(B) @immutable
			alpha: α値
		Returns:
			インスタンス
		"""
		b_alpha = max(0.0, min(1.0, alpha))
		a_alpha = 1.0 - b_alpha
		return (a * a_alpha) + (b * b_alpha)


@Embed.python
@Embed.struct
@Embed.alias('FLinearColor')
class LinearColors:
	"""Note: 自身の型のクラス変数はPythonでは成り立たないためクラスを分離"""

	White: ClassVar[LinearColor] = LinearColor(1.0, 1.0, 1.0, 1.0)
	Gray: ClassVar[LinearColor] = LinearColor(0.5, 0.5, 0.5, 1.0)
	Black: ClassVar[LinearColor] = LinearColor(0.0, 0.0, 0.0, 1.0)
	Transparent: ClassVar[LinearColor] = LinearColor(0.0, 0.0, 0.0, 0.0)
	Red: ClassVar[LinearColor] = LinearColor(1.0, 0.0, 0.0, 1.0)
	Green: ClassVar[LinearColor] = LinearColor(0.0, 1.0, 0.0, 1.0)
	Blue: ClassVar[LinearColor] = LinearColor(0.0, 0.0, 1.0, 1.0)
	Yellow: ClassVar[LinearColor] = LinearColor(1.0, 1.0, 0.0, 1.0)
