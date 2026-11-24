from const.const_asset import AssetSrcs
from const.const_color import ColorCodes
from const.const_layout import Bounds, OutlineCenters, OutlineSizes, Paddings
from const.const_material import SquareEdges
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import ColorParams, IntensityParams, LayoutParams, ShapeParams, to_min_max


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('shape_surface')])


class Definitions:
	@classmethod
	def shape_surface_body(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).safe_zone()
		ShapeParams(mi).round(Bounds.PanelCornar.value).edges(SquareEdges.LBRB).to_pixel()
		ColorParams(mi).base(ColorCodes.M1).opacity_with(intensity=True)
		IntensityParams(mi).uv(y=True, invert=True).min_max(*to_min_max(0.75, 1.0))
		# outline
		ShapeParams(mi).outline(OutlineSizes.S)
		ColorParams(mi).outline(ColorCodes.M2, ColorCodes.M3)
		IntensityParams(mi).minimal().outline().clock().invert()
		return AssetSrcs.UIMaster.value, mi

	@classmethod
	def shape_surface_shadow(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# XXX 2ドット重ねることで隙間を防止
		ShapeParams(mi).round(Bounds.PanelCornar.value + Paddings.Shadow.value - 2.0, anti=False).cornar_min(Paddings.Shadow.value).edges(SquareEdges.LBRB).to_pixel()
		ShapeParams(mi).ring(Paddings.Shadow.value + 2.0).center(OutlineCenters.Shadow).to_pixel()
		ColorParams(mi).shadow().opacity_with(intensity=True)
		IntensityParams(mi).shape()
		return AssetSrcs.UIMaster.value, mi
