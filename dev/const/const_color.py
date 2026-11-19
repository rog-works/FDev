from enum import Enum


class Colors(Enum):
	"""カラー"""
	M1 = '1st'
	M1p1 = '1st_1'
	M1p2 = '1st_2'
	M1p3 = '1st_3'
	M1p4 = '1st_4'
	M1Wrap = '1st_wrap'
	M1p1Wrap = '1st_1_wrap'
	M1p2Wrap = '1st_2_wrap'
	M1p3Wrap = '1st_3_wrap'
	M2 = '2nd'
	M2m1 = '2nd-1'
	M2m05 = '2nd-05'
	M2p1 = '2nd_1'
	M3 = '3rd'
	M3m1 = '3rd-1'
	M3p1 = '3rd_1'
	Red = 'red'
	Green = 'green'
	Blue = 'blue'
	Yellow = 'yellow'
	Purple = 'purple'
	Mint = 'mint'
	Orange = 'orange'
	Brown = 'brown'
	Ocher = 'ocher'
	Skin = 'skin'

	@property
	def code(self) -> int:
		"""Returns: カラーコード"""
		return ColorCodes.__dict__[self.name].value

	@property
	def outline(self) -> bool:
		"""Returns: True = アウトライン有り"""
		return self in [Colors.M1Wrap, Colors.M1p1Wrap, Colors.M1p2Wrap, Colors.M1p3Wrap]


class ColorCodes(Enum):
	"""カラーコード

	Note:
		```
		* ベクターパラメーターとして使うため、sRGBに変換した値を設定
		* 同じ数値が存在するため、数値からEnumに逆変換することは出来ない点に注意
		```
	"""
	M1 = 0xFFFFFFFF
	M1p1 = 0xC8C8C8FF  # type: ignore 0xe5e5e5ff
	M1p2 = 0x9C9C9CFF  # type: ignore 0xcdcdcdff
	M1p3 = 0x373737FF  # type: ignore 0x808080ff
	M1p4 = 0x000000ff  # type: ignore 0x000000ff
	M1Wrap = M1
	M1p1Wrap = M1p1
	M1p2Wrap = M1p2
	M1p3Wrap = M1p3
	M2 = 0x0067FFFF  # type: ignore 0x00aaffff
	M2m1 = 0x37A8FFFF  # type: ignore 0x80d4ffff
	M2m05 = 0x087DFFFF  # type: ignore 0x33baffff
	M2p1 = 0x003F9AFF  # type: ignore 0x0088ccff
	M3 = 0xFF219AFF  # type: ignore 0xff65ccff
	M3m1 = 0xFF50B8FF  # type: ignore 0xff98ddff
	M3p1 = 0xFF0980FF  # type: ignore 0xff34bcff
	White = 0xFFFFFFFF  # type: ignore 0xffffffff
	Black = 0x000000FF  # type: ignore 0x000000ff
	Gray = 0x373737FF  # type: ignore 0x808080ff
	Red = 0x730000FF  # type: ignore 0xb30000ff
	Green = 0x007300FF  # type: ignore 0x00b300ff
	Blue = 0x003CFFFF  # type: ignore 0x0285ffff
	Yellow = 0xFACE00FF  # type: ignore 0xfde800ff
	Purple = 0x2500FFFF  # type: ignore 0x6a00ffff
	Mint = 0x00FF6CFF  # type: ignore 0x00ffaeff
	Orange = 0x731200FF  # type: ignore 0xb34b00ff
	Brown = 0x1F0800FF  # type: ignore 0x623100ff
	Ocher = 0xAB6900FF  # type: ignore 0xd6ac02ff
	Skin = 0xFFBE8AFF  # type: ignore 0xffe0c2ff


class Themes(Enum):
	"""テーマカラー"""
	# アニメーション用
	M1M2 = 'm1_m2'
	M2M1 = 'm2_m1'
	M23M1 = 'm23_m1'
	M1Red = 'm1_red'
	# プライマリー
	M360 = 'm_360'
	Mh23 = 'm_h23'
	Mh32 = 'm_h32'
	Mv23 = 'm_v23'
	# テーマ
	Gold = 'gold'
	Silver = 'silver'
	Bronze = 'bronze'
	Jewel = 'jewel'
	Medicine = 'medicine'
	Blueprint = 'blueprint'
	Star = 'star'
	Earth = 'earth'
	Grass = 'grass'
	Ground = 'ground'
	Stone = 'stone'
	Paper = 'paper'
	Animal = 'animal'
	Fire = 'fire'
	Lightning = 'lightning'
	Heart = 'heart'
	Night = 'night'
	Cool = 'cool'
	Hot = 'hot'
	Rainbow = 'rainbow'
	Plastic = 'plastic'
	Coin = 'coin'
	Bulb = 'bulb'
	Pin = 'pin'
	Blood = 'blood'
	Water = 'water'
	Smash = 'smash'

	@property
	def outline(self) -> bool:
		"""Returns: True = アウトライン有り"""
		return self not in [Themes.M1M2, Themes.M2M1, Themes.M23M1, Themes.M1Red, Themes.M360, Themes.Mh23, Themes.Mh32, Themes.Mv23]
