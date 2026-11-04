# @see Engine/Source/Runtime/Engine/Classes/Engine/Texture.h

from enum import Enum

from tranp.app.compatible.cpp.classes import uint8
from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UENUM, BlueprintType


@UENUM()
class TextureCompressionSettings(Enum):
	"""圧縮設定

	Note:
		```
		TC_Default: Default (BC1 or BC3 with A)
		TC_SingleFloat: Single Float (R32F)
		XXX 何故かEが接頭辞に付かない点に注意
		@see TextureDefines.h
		```
	"""
	TC_Default = 0
	TC_SingleFloat = 15


@UENUM()
class TextureMipGenSettings(Enum):
	"""Mipmap設定

	Note:
		```
		TMGS_NoMipmaps: Mipmap無し
		XXX 何故かEが接頭辞に付かない点に注意
		@see TextureDefines.h
		```
	"""
	TMGS_NoMipmaps = 13


@UENUM()
class TextureFilter(Enum):
	"""フィルター

	Note:
		```
		TF_Nearest: 近似補完? ※余計な補完を除外したい時に使う
		XXX 何故かEが接頭辞に付かない点に注意
		@see TextureDefines.h
		```
	"""
	TF_Nearest = 0


@Embed.alias('E', prefix=True)
@UENUM()
class TextureSourceFormat(Enum):
	"""ピクセルフォーマット

	Note:
		```
		TSF_BGRA8: 一般的なフォーマット(4ch/4byte)
		TSF_R32F: 浮動小数点用(Rch/4byte) ※TC_SingleFloatとセットで使う
		```
	"""
	TSF_BGRA8 = 2
	TSF_R32F = 11


@Embed.alias('F', prefix=True)
@UCLASS(BlueprintType)
class TextureSource:
	"""テクスチャーソース"""

	size_x: int
	size_y: int

	def __init__(self) -> None:
		"""インスタンスを生成"""
		# @python
		self.size_x = 256
		self.size_y = 256

	def Init(self, size_x: int, size_y: int, slices: int, mips: int, pixel_format: TextureSourceFormat, pixels: CP[uint8]) -> None:
		"""インスタンスを初期化

		Args:
			size_x: 横幅
			size_y: 縦幅
			slices: スライス数 ※通常は1で良い
			mips: LOD階層 ※通常は1で良い
			pixel_format: ピクセルフォーマット
			pixels: ピクセルバッファ
		"""
		self.size_x = size_x
		self.size_y = size_y

	def GetSizeX(self) -> int:
		"""Returns: 横幅"""
		return self.size_x

	def GetSizeY(self) -> int:
		"""Returns: 縦幅"""
		return self.size_y


@Embed.alias('U', prefix=True)
@UCLASS(BlueprintType)
class Texture(UObject):
	"""テクスチャー"""
	...


@Embed.alias('U', prefix=True)
@UCLASS(BlueprintType)
class Texture2D(Texture):
	"""テクスチャー(2D)"""

	Source: TextureSource
	CompressionSettings: TextureCompressionSettings
	MipGenSettings: TextureMipGenSettings
	Filter: TextureFilter
	NeverStream: bool
	SRGB: int

	def __init__(self) -> None:
		"""インスタンスを作成"""
		super().__init__()
		self.Source = TextureSource()
		self.CompressionSettings = TextureCompressionSettings.TC_Default
		self.MipGenSettings = TextureMipGenSettings.TMGS_NoMipmaps
		self.Filter = TextureFilter.TF_Nearest
		# True = LODを無視して常に最高品質で扱う。実質的に浮動小数点用
		self.NeverStream = False
		self.SRGB = 1

	def UpdateResource(self) -> None:
		"""リソースを更新 Note: ピクセルバッファ等の更新を適用"""
