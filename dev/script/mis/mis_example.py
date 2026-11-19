import math

from const.const_asset import AssetNames
from const.const_color import ColorCodes
from const.const_layout import Opacities
from const.const_material import EasingIndexs, MFImages
from script.mfs.me_types import float3
from script.mfs.mfs_10_exports import exports_00, exports_b1, exports_ui_main
from script.mis.core.mi_definition import DataDict, MIDefinition
from script.mis.core.mi_params import ColorOptions, ColorParams, IntensityParams, LayoutParams, ParamsBase, ShapeParams


def export() -> dict[str, DataDict]:
	return MIDefinition.export([getattr(Definitions, key) for key in sorted(Definitions.__dict__.keys()) if key.startswith('example')])


class Definitions:
	@classmethod
	def example_bg(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ExampleParams(mi).color_base(float3(0.005, 0.005, 0.005), float3(0.01, 0.02, 0.05)).opacity(Opacities.Shadow)
		IntensityParams(mi).circle().min_max(0.4, 1.0)
		IntensityParams(mi).texture(MFImages.Noise, invert=True)
		IntensityParams(mi).anime(0.02)

		with mi.for_bg():
			ExampleParams(mi).color_base(float3(0.005, 0.005, 0.005), float3(0.01, 0.02, 0.05))
			IntensityParams(mi).uv(x=True).curve(EasingIndexs.Sin180)

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_bg3(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# blend
		mi.decl(exports_ui_main.a_flag_blend_00_and_b1_on_b1, True)

		# scale
		LayoutParams(mi).scale(1.15)
		# scale/intensity
		mi.decl(exports_00.a_flag_ZZ_cell_scale_with_intensity_01, True)
		mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_length_01, True)
		mi.decl(exports_00.intensity_ZZ_min, 0.65)
		# circle
		ShapeParams(mi).circle().tiling(x3=True).tiles(18.0)
		ExampleParams(mi).color_base(float3(0.0, 0.4, 1.0), float3(0.0, 0.2, 1.0))

		with mi.for_bg():
			ShapeParams(mi).square_round(0.1).tiling(x3=True)
			ExampleParams(mi).color_base(float3(0.0, 0.4, 1.0))

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_bg4(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ShapeParams(mi).square_round(0.05).tiling(x3=True)
		ExampleParams(mi).color_base(float3(0.0, 0.0, 0.1), float3(0.14, 0.01, 0.1))
		IntensityParams(mi).uv(x=True, y=True).curve(EasingIndexs.Sin180)
		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_blend_trans(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).scale(0.8)
		ShapeParams(mi).circle()
		ColorParams(mi).base(ColorCodes.M1).opacity(Opacities.Shadow)

		with mi.for_bg():
			LayoutParams(mi).scale(0.8)
			LayoutParams(mi).offset().to(0.1, -0.1)
			ShapeParams(mi).circle()
			ColorParams(mi).base(ColorCodes.M1p4).opacity(Opacities.Shadow)

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_cell3(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# deform
		mi.decl(exports_00.cell_ZZ_aspect, 0.15)
		mi.decl(exports_00.cell_ZZ_offset_x, 0.3)
		ShapeParams(mi).square().tiling(x3=True)
		ExampleParams(mi).color_base(float3(1.0, 0.0, 0.0), float3(1.0, 1.0, 1.0))
		IntensityParams(mi).uv(y=True).curve(EasingIndexs.Linear180)

		with mi.for_bg():
			# scale
			LayoutParams(mi).scale(1.5)
			mi.decl(exports_b1.cell_ZZ_scale_max, 1.2)
			mi.decl(exports_b1.cell_ZZ_scale_min, 0.25)
			# scale/intensity
			mi.decl(exports_b1.a_flag_ZZ_cell_scale_with_intensity_01, True)
			# circle
			ShapeParams(mi).circle().tiling(scroll=True).tiles(5.0)
			# tiling/clip
			mi.decl(exports_b1.a_flag_ZZ_clip_rect, True)
			mi.decl(exports_b1.clip_ZZ_rect_center_x, -0.5)
			mi.decl(exports_b1.clip_ZZ_rect_y, 1.0)
			# color
			ExampleParams(mi).color_base(float3(0.15, 0.15, 0.15), float3(0.05, 0.05, 0.05))
			IntensityParams(mi).uv(x=True, invert=True)
		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_cell_flash(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ShapeParams(mi).polygon(6.0, anti=False).rotation(0.0)
		ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0), float3(1.0, 0.97, 0.65)).opacity_with(intensity=True)
		IntensityParams(mi).shape(invert=True).anime(0.25)

		with mi.for_bg():
			ShapeParams(mi).square_round(0.25, anti=False).tiling(x3=True)
			ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0)).opacity_with(intensity=True)
			IntensityParams(mi).shape(invert=True)

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_cell_round(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		LayoutParams(mi).scale(0.93)
		ShapeParams(mi).square_round(0.1).tiling(x3=True)
		ShapeParams(mi).ring(0.12)
		ExampleParams(mi).color_base(float3(1.0, 0.3, 0.5), float3(1.0, 0.5, 0.0))
		IntensityParams(mi).uv(x=True, y=True)

		with mi.for_bg():
			ShapeParams(mi).square_round(0.1).tiling(x3=True)
			ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0), float3(1.0, 0.95, 0.9))
			IntensityParams(mi).uv(y=True)

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_circle_ripple(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# scale/intensity
		mi.decl(exports_00.a_flag_ZZ_cell_scale_with_intensity_01, True)
		mi.decl(exports_00.a_flag_ZZ_hollow_size_with_intensity_10, True)
		IntensityParams(mi).rotation().alpha().anime(0.5)
		# circle
		ShapeParams(mi).circle(anti=False)
		ShapeParams(mi).ring(1.0)
		# color
		ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0))
		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_font_rising(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0), float3(0.0, 1.0, 1.0))
		IntensityParams(mi).uv(y=True).rotation().alpha(add=True).anime(1.0)
		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_font_text5(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0), float3(0.3, 0.25, 0.06))
		IntensityParams(mi).uv(y=True).min_max(0.0, 0.65)
		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_font_text6(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# flash
		mi.decl(exports_00.a_flag_ZZ_mask_flash, True)
		mi.decl(exports_00.flash_ZZ_interval, 3.0)
		mi.decl(exports_00.flash_ZZ_speed, 5.0)
		# anime
		IntensityParams(mi).anime(1.0)

		with mi.for_bg():
			ExampleParams(mi).color_base(float3(0.0, 0.0, 0.0))

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_outline_flash(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# deform
		mi.decl(exports_00.cell_ZZ_aspect, 0.25)
		# aurora
		mi.decl(exports_00.a_flag_ZZ_mask_aurora, True)
		# tiling
		mi.decl(exports_00.a_flag_ZZ_uv_tiling_3x3_wrap, True)
		# color
		ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0), float3(1.0, 0.7, 0.7)).rotation().opacity_with(intensity=True)
		IntensityParams(mi).shape().anime(0.1)
		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_polygon_dissolve(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# blend
		mi.decl(exports_ui_main.a_flag_blend_b1_and_00, True)

		# dissolve
		mi.decl(exports_00.a_flag_ZZ_dissolve_unit, True)
		mi.decl(exports_00.a_flag_ZZ_mask_dissolve, True)
		mi.decl(exports_00.move_ZZ_alpha, 0.2)
		# dissolve/color
		ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0)).opacity_with(intensity=True)
		# dissolve/intensity
		mi.decl(exports_00.a_flag_ZZ_intensity_via_dissolve_10_alt, True)
		# color
		ColorParams(mi).texture(MFImages.Noise)

		with mi.for_bg():
			ShapeParams(mi).polygon(3.0, anti=False)
			ExampleParams(mi).color_base(float3(1.0, 0.1, 0.0))

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_tab4_selected(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# aurora
		mi.decl(exports_00.a_flag_ZZ_mask_aurora, True)
		ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0)).opacity_with(intensity=True)
		IntensityParams(mi).shape().anime(0.1)

		with mi.for_bg():
			ExampleParams(mi).color_base(float3(1.0, 1.0, 1.0), float3(0.333, 0.3, 0.17)).opacity_with(intensity=True)
			IntensityParams(mi).uv(y=True)

		return AssetNames.UIMaster.value, mi

	@classmethod
	def example_tiling_diamond(cls, mi: MIDefinition) -> tuple[str, MIDefinition]:
		# scale
		LayoutParams(mi).scale(1.0 / math.sqrt(2.0))
		# scale/intensity
		mi.decl(exports_00.a_flag_ZZ_cell_scale_with_intensity_01, True)
		mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_length_01, True)
		mi.decl(exports_00.intensity_ZZ_length_scale, math.sqrt(2.0))
		# scale/intensity/alpha?
		mi.decl(exports_00.move_ZZ_alpha, 1.0)
		# scale/intensity/random
		mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_random, True)
		# square
		ShapeParams(mi).square().rotation(45.0).tiling(x3=True).tiles(3.0)
		# square/rotation/random
		mi.decl(exports_00.a_flag_ZZ_cell_rotation_random, True)
		# tiling/clip
		mi.decl(exports_00.a_flag_ZZ_clip_length, True)
		mi.decl(exports_00.clip_ZZ_length_max, 1.2)
		mi.decl(exports_00.clip_ZZ_length_min, 0.1)
		# color
		ExampleParams(mi).color_base(float3(1.0, 1.0, 0.0), float3(0.0, 1.0, 1.0))
		return AssetNames.UIMaster.value, mi


class ExampleParams(ParamsBase):
	def color_base(self, *colors: float3) -> ColorOptions:
		if len(colors) == 2:
			self.mi.decl(exports_00.a_flag_ZZ_color_gradation, True)
			self.mi.decl(exports_00.color_ZZ, colors[0])
			self.mi.decl(exports_00.color_ZZ_b, colors[1])
		else:
			self.mi.decl(exports_00.color_ZZ, colors[0])

		return ColorOptions(self.mi)
