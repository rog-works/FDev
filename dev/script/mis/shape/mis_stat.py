from const.const_asset import AssetSrcs
from const.const_color import ColorCodes
from script.mfs.func.exports.mfs_exports import exports_ui_main
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import ColorParams, IntensityParams, ShapeParams


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('shape_stat')])


class Definitions:
	@classmethod
	def shape_stat_meter(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ShapeParams(mi).square()
		ColorParams(mi).base(ColorCodes.M2, ColorCodes.M2m1)
		IntensityParams(mi).uv(x=True)
		# blend
		mi.decl(exports_ui_main.a_flag_blend_00_and_b1_on_b1, True)

		with mi.for_bg():
			ShapeParams(mi).round(1.0)
			ColorParams(mi).base(ColorCodes.M1p1)

		return AssetSrcs.UIMaster.value, mi
