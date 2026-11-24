import math

from const.const_asset import AssetSrcs
from const.const_color import ColorCodes
from const.const_material import EasingIndexs
from script.mfs.func.exports.mfs_exports import exports_00
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import ColorParams, IntensityParams, LayoutParams, ParamsBase


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('theme')])


class Definitions:
	@classmethod
	def theme_m1_m2(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.M2)
		IntensityParams(mi).alpha()
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_m2_m1(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.M1)
		IntensityParams(mi).alpha()
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_m23_m1(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base((ColorCodes.M2, ColorCodes.M3), ColorCodes.M1)
		IntensityParams(mi).uv(x=True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_m1_red(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.Red)
		IntensityParams(mi).alpha()
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_m_360(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.M3)
		IntensityParams(mi).uv(x=True, y=True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_m_h23(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.M3)
		IntensityParams(mi).uv(x=True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_m_h32(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M3, ColorCodes.M2)
		IntensityParams(mi).uv(x=True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_m_v23(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.M3)
		IntensityParams(mi).uv(y=True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_gold(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1p4, ColorCodes.Ocher, ColorCodes.M1)
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Metal)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_silver(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1p4, ColorCodes.M1p3, ColorCodes.M1)
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Metal)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_bronze(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1p4, ColorCodes.Orange, ColorCodes.M1)
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Metal)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_jewel(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1p4, ColorCodes.Blue, ColorCodes.M1)
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Metal)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_medicine(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M3, ColorCodes.M1, ColorCodes.Mint)
		IntensityParams(mi).uv(y=True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_blueprint(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.M2m1)
		IntensityParams(mi).uv(y=True).min_max(0.5, 1.0)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_star(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Green, ColorCodes.Yellow)
		IntensityParams(mi).uv(y=True).min_max(0.0, 0.5)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_earth(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Green, ColorCodes.M2)
		IntensityParams(mi).uv(y=True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_grass(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Green, ColorCodes.Skin)
		IntensityParams(mi).uv(y=True).min_max(0.5, 1.0)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_ground(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Ocher, ColorCodes.Brown)
		IntensityParams(mi).uv(y=True).min_max(0.5, 1.0)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_stone(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1p1, ColorCodes.M1p3)
		IntensityParams(mi).uv(y=True).min_max(0.0, 0.75)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_paper(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.M2m1)
		IntensityParams(mi).uv(y=True).min_max(0.5, 1.0)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_animal(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Orange, ColorCodes.Skin)
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Sin180)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_fire(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Yellow, ColorCodes.Red)
		IntensityParams(mi).uv(y=True).min_max(0.0, 0.75)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_lightning(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.Yellow)
		IntensityParams(mi).uv(y=True).min_max(0.25, 0.6)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_heart(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Red, ColorCodes.M3)
		IntensityParams(mi).uv(y=True).min_max(0.0, 0.75)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_night(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Purple, ColorCodes.M3m1)
		IntensityParams(mi).uv(y=True).min_max(0.5, 1.0)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_cool(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.Blue)
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Plastic)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_hot(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.Red)
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Plastic)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_rainbow(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		IntensityParams(mi).uv(y=True)
		mi.decl(exports_00.a_flag_ZZ_color_spectrum, True)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_plastic(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.M1p3, ColorCodes.M1p4)
		ThemeParams(mi).intensity_offset()
		IntensityParams(mi).circle().curve(EasingIndexs.Sin180)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_coin(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.Ocher, ColorCodes.M1p4)
		ThemeParams(mi).intensity_offset()
		IntensityParams(mi).circle().curve(EasingIndexs.Plastic)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_bulb(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Ocher, ColorCodes.Yellow, ColorCodes.M1)
		IntensityParams(mi).circle().min_max(0.0, 0.85)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_pin(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).mirror()
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.Red)
		IntensityParams(mi).uv(x=True, y=True).min_max(0.1, 1.0).curve(EasingIndexs.Sin180)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_blood(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.Red, ColorCodes.Brown)
		ThemeParams(mi).intensity_offset()
		IntensityParams(mi).circle().curve(EasingIndexs.Sin180)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_water(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.M1, ColorCodes.M2m1, ColorCodes.Blue)
		ThemeParams(mi).intensity_offset()
		IntensityParams(mi).circle().curve(EasingIndexs.Sin180)
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def theme_smash(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ColorParams(mi).base(ColorCodes.Yellow, ColorCodes.Green)
		IntensityParams(mi).circle().min_max(0.4, 1.0)
		return AssetSrcs.UIMaster.value, mi


class ThemeParams(ParamsBase):
	def intensity_offset(self) -> None:
		self.mi.decl(exports_00.intensity_ZZ_length_scale, 2.0 / (1.0 / math.sqrt(2.0)))
		self.mi.decl(exports_00.intensity_ZZ_offset_x, -0.5)
		self.mi.decl(exports_00.intensity_ZZ_offset_y, 0.5)
