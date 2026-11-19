from const.const_asset import AssetNames
from const.const_color import ColorCodes
from const.const_layout import OutlineSizes, Paddings
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import ColorParams, IntensityParams, LayoutParams, ShapeParams


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('shape_icon')])


class Definitions:
	@classmethod
	def shape_icon_balloon_caption(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).padding(Paddings.Icon.value)
		ShapeParams(mi).balloon()
		ColorParams(mi).base(ColorCodes.M3)
		return AssetNames.UIMaster.value, mi

	@classmethod
	def shape_icon_balloon_shadow(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).padding(Paddings.Icon.value)
		LayoutParams(mi).offset().lb(Paddings.Icon.value).to_pixel()
		ShapeParams(mi).balloon()
		ColorParams(mi).shadow()
		return AssetNames.UIMaster.value, mi

	@classmethod
	def shape_icon_circle(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).padding(Paddings.Icon.value)
		ShapeParams(mi).circle()
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.M1)
		IntensityParams(mi).alpha()
		# outline
		ShapeParams(mi).outline(OutlineSizes.S)
		ColorParams(mi).outline(ColorCodes.M2)
		return AssetNames.UIMaster.value, mi

	@classmethod
	def shape_icon_circle_shadow(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).padding(Paddings.Icon.value)
		LayoutParams(mi).offset().lb(Paddings.Icon.value).to_pixel()
		ShapeParams(mi).circle()
		ColorParams(mi).shadow()
		return AssetNames.UIMaster.value, mi
