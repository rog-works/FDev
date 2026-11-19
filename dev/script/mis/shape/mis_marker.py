from const.const_asset import AssetNames
from script.mfs.mfs_10_exports import exports_00
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import LayoutParams, ParamsBase, ShapeParams


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('shape_marker')])


class Definitions:
	@classmethod
	def shape_marker_arrow(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ShapeParams(mi).polygon(3.0)
		LayoutParams(mi).scale(0.15).offset().to(y=0.3125)
		MarkerParams(mi).shape_h_half()

		with mi.for_bg():
			ShapeParams(mi).clock(0.2, -0.125)
			MarkerParams(mi).shape_clock_45()
			LayoutParams(mi).scale(0.5)

		return AssetNames.UIMaster.value, mi


class MarkerParams(ParamsBase):
	def shape_h_half(self) -> None:
		self.mi.decl(exports_00.cell_ZZ_aspect, 0.5)

	def shape_clock_45(self) -> None:
		self.mi.decl(exports_00.move_ZZ_alpha, 0.25)
