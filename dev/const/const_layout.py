from enum import Enum


class Paddings(Enum):
	"""パディング"""
	SafeZone = 0.5


class Opacities(Enum):
	"""透過率"""
	Zero = 0.0
	Opaque = 1.0
	Inactive = 0.5
	Underlay = 0.2
	Shadow = 0.25


class OutlineSizes(Enum):
	"""輪郭線のサイズ"""
	S = 2.0
	M = 3.0
	StraightS = 1.0


class OutlineCenters(Enum):
	"""輪郭線の中心位置"""
	Default = 0.5
	Line = 0.85
	Shadow = 1.0
