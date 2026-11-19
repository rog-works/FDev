from const.const_asset import AssetNames
from const.const_color import ColorCodes
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import ColorParams, IntensityParams, LayoutParams, ShapeParams


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('shape_slider')])


class Definitions:
	@classmethod
	def shape_slider_cursor(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).scale(0.85)
		ShapeParams(mi).circle()
		# XXX 仕様上は0.25だが、アンチエイリアスによって1ドット程度細くなるため若干太めに設定
		ShapeParams(mi).ring(0.4)
		ColorParams(mi).base(ColorCodes.M2).opacity_with(intensity=True)
		IntensityParams(mi).alpha()

		# circle
		with mi.for_bg():
			LayoutParams(mi).scale(0.85 / 2.0)
			ShapeParams(mi).circle()
			ColorParams(mi).base(ColorCodes.M2)

		return AssetNames.UIMaster.value, mi

	@classmethod
	def shape_slider_cursor_shadow(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).scale(0.85)
		LayoutParams(mi).offset().lb(0.075)
		ShapeParams(mi).circle()
		# XXX 仕様上は0.25だが、アンチエイリアスによって1ドット程度細くなるため若干太めに設定
		ShapeParams(mi).ring(0.4)
		ColorParams(mi).shadow().opacity_with(intensity=True)
		IntensityParams(mi).alpha()

		with mi.for_bg():
			LayoutParams(mi).scale(0.85 / 2.0)
			LayoutParams(mi).offset().lb(0.075)
			ShapeParams(mi).circle()
			ColorParams(mi).shadow()

		return AssetNames.UIMaster.value, mi
