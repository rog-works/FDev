from typing import Self

from compatible.error import Errors
from const.const_color import ColorCodes
from const.const_layout import Opacities, OutlineCenters, OutlineSizes, Paddings
from const.const_material import EasingIndexs, MFImages, SquareEdges, SquareSides
from script.mfs.me_types import float3, texture
from script.mfs.mfs_10_exports import exports_00, exports_ui_main
from script.mis.core.mi_definition import MIDefinition


def to_min_max(min_01: float, max_01: float) -> tuple[float, float]:
	minimum = max_01 - (1.0 / (max_01 - min_01))
	return minimum, max_01


class ParamsBase:
	def __init__(self, mi: MIDefinition) -> None:
		self.mi = mi


class LayoutOffsetOptions(ParamsBase):
	def to(self, x: float = 0.0, y: float = 0.0) -> Self:
		self.mi.decl(exports_00.cell_ZZ_offset_x, self.mi.ok(x, x != 0.0))
		self.mi.decl(exports_00.cell_ZZ_offset_y, self.mi.ok(y, y != 0.0))
		return self

	def rt(self, size: float) -> Self:
		self.mi.decl(exports_00.cell_ZZ_offset_x, -size)
		self.mi.decl(exports_00.cell_ZZ_offset_y, size)
		return self

	def lb(self, size: float) -> Self:
		self.mi.decl(exports_00.cell_ZZ_offset_x, size)
		self.mi.decl(exports_00.cell_ZZ_offset_y, -size)
		return self

	def to_pixel(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_cell_offset_to_pixel, True)
		return self


class LayoutParams(ParamsBase):
	def safe_zone(self) -> None:
		"""Note: paddingとの使い分け (safe_zone: マスク生成の健全化, padding: レイアウト上のパディング)"""
		self.mi.decl(exports_00.a_flag_ZZ_cell_scale_padding_pixel, True)
		self.mi.decl(exports_00.a_flag_ZZ_cell_scale_padding_pixel_ignore_dpi_scale, True)
		self.mi.decl(exports_00.cell_ZZ_scale_padding_pixel, -Paddings.SafeZone.value)

	def padding(self, pixel: float) -> None:
		self.mi.decl(exports_00.a_flag_ZZ_cell_scale_padding_pixel, True)
		self.mi.decl(exports_00.cell_ZZ_scale_padding_pixel, -pixel)

	def scale(self, size: float) -> Self:
		# Note: XXX paddingとscaleは実質的に同じ用途
		self.mi.decl(exports_00.cell_ZZ_scale, size)
		return self

	def offset(self) -> LayoutOffsetOptions:
		return LayoutOffsetOptions(self.mi)

	def invert(self, border: float) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_uv_invert, True)
		self.mi.decl(exports_00.uv_ZZ_invert_border_x, border)
		return self

	def mirror(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_uv_mirror, True)
		return self


class ShapeOptions(ParamsBase):
	def keep(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_cell_aspect_keep, True)
		return self

	def tiles(self, tiles: float) -> Self:
		self.mi.decl(exports_00.uv_ZZ_tiles, tiles)
		return self

	def tiling(self, x3: bool = False, wrap: bool = False, scroll: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_uv_tiling_3x3, self.mi.ok(True, x3 and not wrap and not scroll))
		self.mi.decl(exports_00.a_flag_ZZ_uv_tiling_3x3_wrap, self.mi.ok(True, wrap and not x3 and not scroll))
		self.mi.decl(exports_00.a_flag_ZZ_uv_tiling_min_scroll, self.mi.ok(True, scroll and not x3 and not wrap))
		return self
	
	def rotation(self, degree: float) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_cell_rotation, True)
		self.mi.decl(exports_00.cell_ZZ_degree, degree)
		return self


class ShapeOptionsRound(ShapeOptions):
	def cornar_min(self, cornar_min: float) -> Self:
		self.mi.decl(exports_00.polygon_ZZ_round_radius_min, cornar_min)
		return self

	def edges(self, edges: SquareEdges) -> Self:
		self.mi.decl(exports_00.polygon_ZZ_allows_edges, edges.value)
		return self

	def clip(self, sides: SquareSides) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_clip_square_sides, True)
		self.mi.decl(exports_00.polygon_ZZ_allows_sides, sides.value)
		return self

	def to_pixel(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_size_to_pixel_for_mask, True)
		return self


class ShapeOptionsSquare(ShapeOptions):
	def clip(self, sides: SquareSides) -> Self:
		ShapeOptionsRound(self.mi).clip(sides)
		return self


class ShapeOptionsRing(ParamsBase):
	def center(self, center: OutlineCenters) -> Self:
		self.mi.decl(exports_00.hollow_ZZ_center, center.value)
		return self

	def to_pixel(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_size_to_pixel_for_line, True)
		return self


class ShapeParams(ParamsBase):
	def balloon(self, keep: bool = False, anti: bool = True) -> ShapeOptions:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_square_round, self.mi.ok(True, not keep))
		self.mi.decl(exports_00.a_flag_ZZ_mask_square_round_fix, self.mi.ok(True, keep))
		self.mi.decl(exports_00.polygon_ZZ_allows_edges, SquareEdges.LTRTRB.value)
		self.mi.decl(exports_00.polygon_ZZ_round_radius, 1.0)
		return ShapeOptions(self.mi)

	def circle(self, anti: bool = True) -> ShapeOptions:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_circle, True)
		return ShapeOptions(self.mi)

	def clock(self, radius: float, center: float = 0.0, anti: bool = True) -> ShapeOptions:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_clock, True)
		self.mi.decl(exports_00.cupsule_ZZ_radius, radius)
		self.mi.decl(exports_00.cupsule_ZZ_center, center)
		return ShapeOptions(self.mi)

	def cupsule(self, radius: float, begin: float, end: float, anti: bool = True) -> ShapeOptions:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_cupsule, True)
		self.mi.decl(exports_00.cupsule_ZZ_radius, radius)
		self.mi.decl(exports_00.cupsule_ZZ_begin, begin)
		self.mi.decl(exports_00.cupsule_ZZ_end, end)
		return ShapeOptions(self.mi)

	def round(self, cornar: float, anti: bool = True) -> ShapeOptionsRound:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_square_round_fix, True)
		self.mi.decl(exports_00.polygon_ZZ_round_radius, cornar)
		return ShapeOptionsRound(self.mi)

	def square_round(self, cornar: float, anti: bool = True) -> ShapeOptionsRound:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_square_round, True)
		self.mi.decl(exports_00.polygon_ZZ_round_radius, cornar)
		return ShapeOptionsRound(self.mi)

	def square(self, anti: bool = True) -> ShapeOptionsSquare:
		self.mi.decl(exports_00.a_flag_ZZ_mask_square, True)
		return ShapeOptionsSquare(self.mi)
	
	def polygon(self, sides: float, anti: bool = True) -> ShapeOptions:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_polygon, True)
		self.mi.decl(exports_00.polygon_ZZ_sides, sides)
		return ShapeOptions(self.mi)

	def polygon_round(self, sides: float, cornar, anti: bool = True) -> ShapeOptions:
		self.mi.decl(exports_ui_main.a_flag_00_anti, self.mi.ok(True, anti))
		self.mi.decl(exports_00.a_flag_ZZ_mask_polygon_round, True)
		self.mi.decl(exports_00.polygon_ZZ_sides, sides)
		self.mi.decl(exports_00.polygon_ZZ_round_radius, cornar)
		return ShapeOptions(self.mi)

	def ring(self, size: float) -> ShapeOptionsRing:
		self.mi.decl(exports_00.a_flag_ZZ_mask_hollow, True)
		self.mi.decl(exports_00.hollow_ZZ_line_size, size)
		return ShapeOptionsRing(self.mi)

	def outline(self, size: OutlineSizes) -> None:
		self.mi.decl(exports_00.a_flag_ZZ_size_to_pixel_for_line, True)
		self.mi.decl(exports_00.hollow_ZZ_center, OutlineCenters.Line.value)
		self.mi.decl(exports_00.hollow_ZZ_line_size, size.value)


class ColorOptions(ParamsBase):
	def opacity(self, opacity: Opacities) -> Self:
		self.mi.decl(exports_00.opacity_ZZ, opacity.value)
		return self

	def opacity_with(self, intensity: bool = False, texture: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_color_trans, True if intensity else None)
		self.mi.decl(exports_00.a_flag_ZZ_color_trans_with_texture, True if texture else None)
		return self

	def rotation(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_color_rotaion, True)
		return self


class ColorParams(ParamsBase):
	def base(self, *colors: ColorCodes | tuple[ColorCodes, ColorCodes]) -> ColorOptions:
		if len(colors) == 1 and isinstance(colors[0], ColorCodes):
			self.mi.decl(exports_00.color_ZZ, float3(colors[0].value))
		elif len(colors) == 2 and isinstance(colors[0], ColorCodes) and isinstance(colors[1], ColorCodes):
			self.mi.decl(exports_00.a_flag_ZZ_color_gradation, True)
			self.mi.decl(exports_00.color_ZZ, float3(colors[0].value))
			self.mi.decl(exports_00.color_ZZ_b, float3(colors[1].value))
		elif len(colors) == 3 and isinstance(colors[0], ColorCodes) and isinstance(colors[1], ColorCodes) and isinstance(colors[2], ColorCodes):
			self.mi.decl(exports_00.a_flag_ZZ_color_gradation3, True)
			self.mi.decl(exports_00.color_ZZ, float3(colors[0].value))
			self.mi.decl(exports_00.color_ZZ_b, float3(colors[1].value))
			self.mi.decl(exports_00.color_ZZ_c, float3(colors[2].value))
		elif len(colors) == 2 and isinstance(colors[0], tuple) and isinstance(colors[1], ColorCodes):
			self.mi.decl(exports_00.a_flag_ZZ_color_gradation_ab_to_c, True)
			self.mi.decl(exports_00.color_ZZ, float3(colors[0][0].value))
			self.mi.decl(exports_00.color_ZZ_b, float3(colors[0][1].value))
			self.mi.decl(exports_00.color_ZZ_c, float3(colors[1].value))
		elif len(colors) == 2 and isinstance(colors[0], ColorCodes) and isinstance(colors[1], tuple):
			self.mi.decl(exports_00.a_flag_ZZ_color_gradation_c_to_ab, True)
			self.mi.decl(exports_00.color_ZZ, float3(colors[1][0].value))
			self.mi.decl(exports_00.color_ZZ_b, float3(colors[1][1].value))
			self.mi.decl(exports_00.color_ZZ_c, float3(colors[0].value))

		return ColorOptions(self.mi)

	def outline(self, *colors: ColorCodes | tuple[ColorCodes, ColorCodes]) -> ColorOptions:
		if len(colors) == 1 and isinstance(colors[0], ColorCodes):
			self.mi.decl(exports_00.a_flag_ZZ_color_line, True)
			self.mi.decl(exports_00.color_ZZ_line, float3(colors[0].value))
		elif len(colors) == 2 and isinstance(colors[0], ColorCodes) and isinstance(colors[1], ColorCodes):
			self.mi.decl(exports_00.a_flag_ZZ_color_line_gradation, True)
			self.mi.decl(exports_00.color_ZZ_line, float3(colors[0].value))
			self.mi.decl(exports_00.color_ZZ_line_b, float3(colors[1].value))
		elif len(colors) == 3 and isinstance(colors[0], ColorCodes) and isinstance(colors[1], ColorCodes) and isinstance(colors[2], ColorCodes):
			raise Errors.Unsupported(colors)
		elif len(colors) == 2 and isinstance(colors[0], tuple) and isinstance(colors[1], ColorCodes):
			self.mi.decl(exports_00.a_flag_ZZ_color_line_gradation_ab_to_c, True)
			self.mi.decl(exports_00.color_ZZ_line, float3(colors[0][0].value))
			self.mi.decl(exports_00.color_ZZ_line_b, float3(colors[0][1].value))
			self.mi.decl(exports_00.color_ZZ_line_c, float3(colors[1].value))
		elif len(colors) == 2 and isinstance(colors[0], ColorCodes) and isinstance(colors[1], tuple):
			raise Errors.Unsupported(colors)

		return ColorOptions(self.mi)

	def inactive(self) -> ColorOptions:
		self.mi.decl(exports_00.color_ZZ, float3(ColorCodes.M1p3.value))
		return ColorOptions(self.mi)

	def shadow(self) -> ColorOptions:
		self.mi.decl(exports_00.color_ZZ, float3(ColorCodes.M1p4.value))
		self.mi.decl(exports_00.opacity_ZZ, Opacities.Shadow.value)
		return ColorOptions(self.mi)
	
	def texture(self, image: MFImages) -> ColorOptions:
		self.mi.decl(exports_00.a_flag_ZZ_color_texture, True)
		self.mi.decl(exports_00.texture_ZZ_image, texture(image.value))
		return ColorOptions(self.mi)


class IntensityParamsMinimal(ParamsBase):
	def shape(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_color_intensity_via_minimal, True)
		return self

	def outline(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_color_intensity_via_minimal_for_line, True)
		return self

	def uv(self, x: bool = False, y: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_minimal_via_uv_x, self.mi.ok(True, x and not y))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_minimal_via_uv_y, self.mi.ok(True, y and not x))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_minimal_via_uv_xy, self.mi.ok(True, x and y))
		return self

	def clock(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_minimal_via_uv_theta, True)
		return self

	def alpha(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_minimal_via_alpha, True)
		return self

	def clamp(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_minimal_clamp, True)
		return self

	def invert(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_minimal_invert, True)
		return self


class IntensityParams(ParamsBase):
	def min_max(self, minimum: float, maximum: float) -> Self:
		self.mi.decl(exports_00.intensity_ZZ_min, minimum)
		self.mi.decl(exports_00.intensity_ZZ_max, maximum)
		return self

	def curve(self, easing: EasingIndexs) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_curve, True)
		self.mi.decl(exports_00.intensity_ZZ_easing, easing.value)
		return self

	def uv(self, x: bool = False, y: bool = False, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_x_01, self.mi.ok(True, x and not y and not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_x_10, self.mi.ok(True, x and not y and invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_y_01, self.mi.ok(True, y and not x and not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_y_10, self.mi.ok(True, y and not x and invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_xy_01, self.mi.ok(True, x and y and not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_xy_10, self.mi.ok(True, x and y and invert))
		return self

	def uv_cell(self, x: bool = False, y: bool = False, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_uv_x_01, self.mi.ok(True, x and not y and not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_uv_x_10, self.mi.ok(True, x and not y and invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_uv_y_01, self.mi.ok(True, y and not x and not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_uv_y_10, self.mi.ok(True, y and not x and invert))
		return self

	def uv_cell_unit(self, x: bool = False, y: bool = False, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_uv_x_01, self.mi.ok(True, x and not y and not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_uv_x_10, self.mi.ok(True, x and not y and invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_uv_y_01, self.mi.ok(True, y and not x and not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_uv_y_10, self.mi.ok(True, y and not x and invert))
		return self

	def circle(self, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_length_01, self.mi.ok(True, not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_length_10, self.mi.ok(True, invert))
		return self

	def circle_cell(self, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_length_01, self.mi.ok(True, not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_length_10, self.mi.ok(True, invert))
		return self

	def circle_cell_unit(self, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_length_01, self.mi.ok(True, not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_length_10, self.mi.ok(True, invert))
		return self

	def square(self, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_square_01, self.mi.ok(True, not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_square_10, self.mi.ok(True, invert))
		return self

	def clock(self, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_theta_01, self.mi.ok(True, not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_uv_theta_10, self.mi.ok(True, invert))
		return self

	def shape(self, invert: bool = False, stretch: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_shape_01_alt, self.mi.ok(True, not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_shape_10_alt, self.mi.ok(True, invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_stretch_alt, self.mi.ok(True, stretch))
		return self

	def texture(self, image: MFImages, invert: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_texture_01, self.mi.ok(True, not invert))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_texture_10, self.mi.ok(True, invert))
		self.mi.decl(exports_00.texture_ZZ_image, texture(image.value))
		return self

	def alpha(self, add: bool = False) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_alpha, self.mi.ok(True, not add))
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_alpha_add, self.mi.ok(True, add))
		return self

	def anime(self, speed: float) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_anime, True)
		self.mi.decl(exports_00.move_ZZ_speed, speed)
		return self

	def clamp(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_clamp, True)
		return self

	def rotation(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_rotation, True)
		return self

	def invert(self) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_invert, True)
		return self

	def random_cell(self, seed: float) -> Self:
		self.mi.decl(exports_00.a_flag_ZZ_intensity_via_cell_unit_random, True)
		self.mi.decl(exports_00.random_ZZ_seed, seed)
		return self

	def minimal(self) -> IntensityParamsMinimal:
		return IntensityParamsMinimal(self.mi)
