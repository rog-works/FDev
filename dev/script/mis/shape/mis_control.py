from const.const_asset import AssetNames
from const.const_color import ColorCodes
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import ColorParams, LayoutParams, ShapeParams


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('shape_control')])


class Definitions:
	@classmethod
	def shape_control_select_caret(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).invert(0.5).offset().to(0.0, -0.1)
		ShapeParams(mi).cupsule(0.15, 0.0, 0.75).rotation(135.0)
		ColorParams(mi).base(ColorCodes.M2)
		return AssetNames.UIMaster.value, mi
