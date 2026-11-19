from enum import Enum


class MFImages(Enum):
	"""マテリアル関数用画像

	Attributes:
		Noise: ノイズ
		NoiseLinear: ノイズ (LinearColor版)
		Easings: イージングカーブ
	"""
	Noise = 'solid_noise'
	NoiseLinear = 'solid_noise_linear'
	Easings = 'easings'


class MFImageSizes(Enum):
	"""基準サイズ

	Attributes:
		EasingCurve: イージングカーブテクスチャーの縦横幅
	"""
	EasingCurve = 256.0


class ParametersValues(Enum):
	"""パラメーターコレクション"""
	DPIScale = 0.6666


class EasingIndexs(Enum):
	"""イージングメソッド Note: @see const.const_anim.Easings"""
	Linear90 = 0.0
	Linear180 = 1.0
	Sin90 = 2.0
	Sin180 = 3.0
	Metal = 4.0
	Plastic = 5.0
	Min = 0.0
	Max = 5.0


class SquareEdges(Enum):
	"""四角形出力フラグ(角)"""
	LT = 1.0
	RT = 2.0
	LB = 4.0
	RB = 8.0
	All = LT + RT + LB + RB
	LBRB = LB + RB
	LTLB = LT + LB
	LTRTRB = LT + RT + RB


class SquareSides(Enum):
	"""四角形出力フラグ(辺)"""
	L = 1.0
	T = 2.0
	R = 4.0
	B = 8.0
	TB = T + B
	LRB = L + R + B


class Layers(Enum):
	"""レイヤー"""
	Main = '00'
	Bg = 'b1'
	Tag = 'ZZ'
