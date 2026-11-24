from typing import Annotated

from tranp.app.compatible.python.embed import Embed

from const.const_material import MFImageSizes, ParametersValues
from script.mfs.core.me import ME, SamplerTypes
from script.mfs.core.me_types import float2, float3
from script.mfs.func.color.mfs_color import color_gradation, color_gradation3, color_gradation_ab_to_c, color_gradation_c_to_ab, color_gradation_line_ab_to_c, color_rotation, color_spectrum
from script.mfs.func.exports.mfs_exports import exports_ZZ
from script.mfs.func.mask.mfs_mask import mask_aurora, mask_clock_cupsule, mask_cupsule, mask_dissolve, mask_flash, mask_linear_range, mask_polygon, mask_polygon_round, mask_rect, mask_rect_edge, mask_square, mask_square_round, mask_square_round_fix, mask_square_side, mask_stripe
from script.mfs.func.math.mfs_math import math_aspect2d, math_resolution_to_aspect, math_resolution_to_pixel_size
from script.mfs.func.matrix.mfs_matrix import matrix_rotation2d
from script.mfs.func.op.mfs_op import op_in
from script.mfs.func.op.mfs_op_logic import op_or, op_switch_2d, op_switch_ab, op_switch_dir_multiply
from script.mfs.func.tiling.mfs_tiling import tiling_uv_for_ui
from script.mfs.func.uv.mfs_uv import uv_deformation, uv_fisheye, uv_invert_x, uv_to_vector


def ui_layer_ZZ(uv: Annotated[float2, ME.tex_coord(0)], resolution: Annotated[float2, float2(250.0, 250.0)], dpi_scale: Annotated[float, ParametersValues.DPIScale.value]) -> tuple[float3, float, float]:
	"""UI用レイヤー

	Args:
		uv: UV座標
		resolution: 解像度 (default = 250:250)
		dpi_scale: DPIスケール (default = 0.666)
	Returns:
		(ベースカラー, 透過率, 強度)
	"""
	exports = exports_ZZ()

	# 解像度
	aspect = math_resolution_to_aspect(resolution)
	pixel_size = math_resolution_to_pixel_size(resolution)

	# UV座標
	uv_base_0 = float2(1.0 - uv.x, uv.y) if exports.a_flag_ZZ_uv_mirror else uv
	uv_base = uv_invert_x(uv, exports.uv_ZZ_invert_border_x) if exports.a_flag_ZZ_uv_invert else uv_base_0
	uv_vector = uv_to_vector(uv_base)
	uv_length = uv_vector.length()
	uv_length_max = float2(1.0, 1.0).length()
	uv_offset = float2(exports.uv_ZZ_offset_x, exports.uv_ZZ_offset_y)

	# タイル情報 XXX セルとタイルは同義。命名規則を分けているだけ
	# 変形より先にタイリングを適用しないと3x3タイリングが成立しない点に注意
	tile_uv_0, tile_index, cells = tiling_uv_for_ui(uv_base + uv_offset, aspect, exports.uv_ZZ_tiles, exports.a_flag_ZZ_uv_tiling_3x3, exports.a_flag_ZZ_uv_tiling_3x3_wrap, exports.a_flag_ZZ_uv_tiling_min_scroll)
	tile_uv = uv_fisheye(tile_uv_0, 1.0) if exports.a_flag_ZZ_uv_remap_fisheye else tile_uv_0

	# セル
	cell_unit_random = ME.rand_fast(tile_index, exports.random_ZZ_seed)
	cell_unit_uv = (tile_index + 0.5) / cells
	cell_unit_vector = uv_to_vector(cell_unit_uv)
	cell_unit_length = cell_unit_vector.length()
	cell_aspect = aspect if exports.a_flag_ZZ_cell_aspect_keep else 1.0
	cell_aspect2d = math_aspect2d(aspect)
	cell_offset = cell_aspect2d * float2(exports.cell_ZZ_offset_x, exports.cell_ZZ_offset_y) * pixel_size if exports.a_flag_ZZ_cell_offset_to_pixel else float2(exports.cell_ZZ_offset_x, exports.cell_ZZ_offset_y)
	# 1.0は半径なのでピクセル指定時は2倍にする
	cell_scale_padding_pixel_0 = exports.cell_ZZ_scale_padding_pixel * 2.0 * pixel_size
	# XXX 微小な補正(1ピクセル)の場合、DPIスケールによって1ピクセル前後に揺らぐとマスクの生成に大きく影響を与えるためDPIスケールの影響を除外できるようにする
	cell_scale_padding_pixel = cell_scale_padding_pixel_0 / dpi_scale if exports.a_flag_ZZ_cell_scale_padding_pixel_ignore_dpi_scale else cell_scale_padding_pixel_0
	cell_scale = (cell_aspect2d * cell_scale_padding_pixel) + exports.cell_ZZ_scale if exports.a_flag_ZZ_cell_scale_padding_pixel else float2(exports.cell_ZZ_scale, exports.cell_ZZ_scale)
	cell_uv = uv_deformation(tile_uv, cell_offset, cell_aspect, cell_scale)

	# アニメ
	move = ME.time() * exports.move_ZZ_speed + exports.move_ZZ_alpha if exports.a_flag_ZZ_anime else exports.move_ZZ_alpha
	move_pos = float2(exports.move_ZZ_speed_x, exports.move_ZZ_speed_y) * move

	# テクスチャー
	texture_uv_offset = float2(exports.texture_ZZ_offset_x, exports.texture_ZZ_offset_y) + move_pos
	texture_aspect = aspect if exports.a_flag_ZZ_cell_aspect_keep else 1.0
	# テクスチャーのUV座標は単位変換が不要なため、uv_deformationのオフセット座標は使わず、単純に加算する
	texture_uv = uv_deformation(uv_base, float2(0.0, 0.0), texture_aspect, float2(exports.texture_ZZ_scale, exports.texture_ZZ_scale)) + texture_uv_offset
	texture_color = ME.sample(exports.texture_ZZ_image, texture_uv)

	# 強度(通常)
	intensity_uv = uv_base + float2(exports.intensity_ZZ_offset_x, exports.intensity_ZZ_offset_y)
	intensity_vector = uv_to_vector(intensity_uv)
	intensity_0 = op_switch_dir_multiply(intensity_uv.x, 1.0, exports.a_flag_ZZ_intensity_via_uv_x_01, exports.a_flag_ZZ_intensity_via_uv_x_10)
	intensity_1 = op_switch_dir_multiply(intensity_uv.y, intensity_0, exports.a_flag_ZZ_intensity_via_uv_y_01, exports.a_flag_ZZ_intensity_via_uv_y_10)
	intensity_2 = op_switch_dir_multiply((intensity_uv.x + intensity_uv.y) * 0.5, intensity_1, exports.a_flag_ZZ_intensity_via_uv_xy_01, exports.a_flag_ZZ_intensity_via_uv_xy_10)
	intensity_3 = op_switch_dir_multiply(intensity_vector.length() / exports.intensity_ZZ_length_scale, intensity_2, exports.a_flag_ZZ_intensity_via_length_01, exports.a_flag_ZZ_intensity_via_length_10)
	intensity_4 = op_switch_dir_multiply(cell_unit_uv.x, intensity_3, exports.a_flag_ZZ_intensity_via_cell_unit_uv_x_01, exports.a_flag_ZZ_intensity_via_cell_unit_uv_x_10)
	intensity_5 = op_switch_dir_multiply(cell_unit_uv.y, intensity_4, exports.a_flag_ZZ_intensity_via_cell_unit_uv_y_01, exports.a_flag_ZZ_intensity_via_cell_unit_uv_y_10)
	intensity_6 = op_switch_dir_multiply(cell_unit_length / exports.intensity_ZZ_length_scale, intensity_5, exports.a_flag_ZZ_intensity_via_cell_unit_length_01, exports.a_flag_ZZ_intensity_via_cell_unit_length_10)
	intensity_7 = op_switch_dir_multiply(cell_uv.x, intensity_6, exports.a_flag_ZZ_intensity_via_cell_uv_x_01, exports.a_flag_ZZ_intensity_via_cell_uv_x_10)
	intensity_8 = op_switch_dir_multiply(cell_uv.y, intensity_7, exports.a_flag_ZZ_intensity_via_cell_uv_y_01, exports.a_flag_ZZ_intensity_via_cell_uv_y_10)
	intensity_9 = op_switch_dir_multiply(uv_to_vector(cell_uv).length() / exports.intensity_ZZ_length_scale, intensity_8, exports.a_flag_ZZ_intensity_via_cell_length_01, exports.a_flag_ZZ_intensity_via_cell_length_10)
	intensity_10 = op_switch_dir_multiply(ME.abs(ME.atan2_fast(intensity_vector.y, intensity_vector.x) / ME.pi()), intensity_9, exports.a_flag_ZZ_intensity_via_uv_theta_01, exports.a_flag_ZZ_intensity_via_uv_theta_10)
	intensity_11 = op_switch_dir_multiply(mask_square(intensity_vector, 1.0), intensity_10, exports.a_flag_ZZ_intensity_via_uv_square_01, exports.a_flag_ZZ_intensity_via_uv_square_10)
	intensity_12 = op_switch_ab(move, intensity_11 + move, intensity_11, exports.a_flag_ZZ_intensity_via_alpha, exports.a_flag_ZZ_intensity_via_alpha_add)
	intensity_13 = ME.sample(exports.intensity_ZZ_curve, float2(intensity_12, (exports.intensity_ZZ_easing + 0.5) / MFImageSizes.EasingCurve.value), SamplerTypes.Linear.value).x if exports.a_flag_ZZ_intensity_curve else intensity_12
	intensity_14 = op_switch_dir_multiply(texture_color.x, intensity_13, exports.a_flag_ZZ_intensity_via_texture_01, exports.a_flag_ZZ_intensity_via_texture_10)
	intensity_15 = (intensity_14 + cell_unit_random) % 1.0 if exports.a_flag_ZZ_intensity_via_cell_unit_random else intensity_14
	intensity_16 = intensity_15 % 1.0 if exports.a_flag_ZZ_intensity_rotation else intensity_15
	intensity_17 = intensity_16 if exports.a_flag_ZZ_intensity_stretch_alt else (intensity_16 - exports.intensity_ZZ_min) / (exports.intensity_ZZ_max - exports.intensity_ZZ_min)
	intensity_18 = ME.saturate(intensity_17) if exports.a_flag_ZZ_intensity_clamp else intensity_17
	intensity = 1.0 - intensity_18 if exports.a_flag_ZZ_intensity_invert else intensity_18

	# 強度(簡易)
	intensity_minimal_0 = intensity_uv.x if exports.a_flag_ZZ_intensity_minimal_via_uv_x else 1.0
	intensity_minimal_1 = intensity_minimal_0 * intensity_uv.y if exports.a_flag_ZZ_intensity_minimal_via_uv_y else intensity_minimal_0
	intensity_minimal_2 = intensity_minimal_1 * (intensity_uv.x + intensity_uv.y) * 0.5 if exports.a_flag_ZZ_intensity_minimal_via_uv_xy else intensity_minimal_1
	intensity_minimal_3 = intensity_minimal_2 * ME.abs(ME.atan2_fast(intensity_vector.y, intensity_vector.x) / ME.pi()) if exports.a_flag_ZZ_intensity_minimal_via_uv_theta else intensity_minimal_2
	intensity_minimal_4 = move if exports.a_flag_ZZ_intensity_minimal_via_alpha else intensity_minimal_3
	intensity_minimal_5 = ME.saturate(intensity_minimal_4) if exports.a_flag_ZZ_intensity_minimal_clamp else intensity_minimal_4
	intensity_minimal = 1.0 - intensity_minimal_5 if exports.a_flag_ZZ_intensity_minimal_invert else intensity_minimal_5

	# XXX サイズを0にするとアーティファクトが発生するため下限値を設ける
	cell_scale_alt = cell_scale * ME.max(op_switch_dir_multiply(intensity, 1.0, exports.a_flag_ZZ_cell_scale_with_intensity_01, exports.a_flag_ZZ_cell_scale_with_intensity_10), 0.001)
	# XXX マスク用のcell_uvにはintensityを適用するため別途算出
	cell_uv_alt_0 = uv_deformation(tile_uv, cell_offset, cell_aspect, cell_scale_alt)
	cell_uv_alt = op_switch_2d(cell_uv_alt_0, cell_uv_alt_0, cell_uv, exports.a_flag_ZZ_cell_scale_with_intensity_01, exports.a_flag_ZZ_cell_scale_with_intensity_10)

	# ベクトル
	vector_u_theta = exports.cell_ZZ_degree / 360.0 + move + (cell_unit_random if exports.a_flag_ZZ_cell_rotation_random else 0.0)
	vector_aspect2d = math_aspect2d(exports.cell_ZZ_aspect)
	vector = matrix_rotation2d(uv_to_vector(cell_uv_alt), vector_u_theta) / vector_aspect2d if exports.a_flag_ZZ_cell_rotation else uv_to_vector(cell_uv_alt) / vector_aspect2d

	# サイズ
	mask_pixel_size = pixel_size / ME.min(cell_scale_alt.x, cell_scale_alt.y)
	# 角丸/中抜きの半径は(1.0=半径)。ピクセル指定時は2倍で直径に変換。タイリング時は半径がタイル数で分割されるため、更にタイル数を掛けて直径に変換
	mask_radius_bias_for_line = mask_pixel_size * (2.0 * exports.uv_ZZ_tiles) if exports.a_flag_ZZ_size_to_pixel_for_line else 1.0
	mask_radius_bias_for_mask = mask_pixel_size * (2.0 * exports.uv_ZZ_tiles) if exports.a_flag_ZZ_size_to_pixel_for_mask else 1.0
	# カプセルは半径によって1の長さが決定するため、ピクセル指定時は線のサイズに逆数を掛ける
	mask_hollow_line_size_0 = exports.hollow_ZZ_line_size * op_or(1.0 / exports.cupsule_ZZ_radius, 1.0, exports.a_flag_ZZ_mask_clock, exports.a_flag_ZZ_mask_cupsule)
	mask_hollow_line_size = op_switch_dir_multiply(intensity, mask_hollow_line_size_0, exports.a_flag_ZZ_hollow_size_with_intensity_01, exports.a_flag_ZZ_hollow_size_with_intensity_10)

	# 消失エフェクト
	dissolve_alpha = (move * uv_length_max / uv_length) if exports.a_flag_ZZ_dissolve_unit else move
	dissolve_mask, dissolve_min_mask, dissolve_min_alpha = mask_dissolve(1.0 - dissolve_alpha, exports.dissolve_ZZ_smooth, float2(exports.dissolve_ZZ_scroll_x, exports.dissolve_ZZ_scroll_y))

	# マスク
	mask_0 = cell_uv_alt.x if exports.a_flag_ZZ_mask_cell_x else 1.0
	mask_1 = vector.length() if exports.a_flag_ZZ_mask_circle else mask_0
	mask_2 = mask_polygon(vector, exports.polygon_ZZ_sides) if exports.a_flag_ZZ_mask_polygon else mask_1
	mask_3 = mask_polygon_round(vector, exports.polygon_ZZ_sides, exports.polygon_ZZ_round_radius * mask_radius_bias_for_mask) if exports.a_flag_ZZ_mask_polygon_round else mask_2
	mask_4 = mask_square(vector, 1.0) if exports.a_flag_ZZ_mask_square else mask_3
	mask_5 = mask_square_round(vector, 1.0, exports.polygon_ZZ_round_radius * mask_radius_bias_for_mask, exports.polygon_ZZ_round_radius_min * mask_radius_bias_for_mask, exports.polygon_ZZ_allows_edges) if exports.a_flag_ZZ_mask_square_round else mask_4
	mask_6 = mask_square_round_fix(cell_uv_alt, aspect, exports.polygon_ZZ_round_radius * mask_radius_bias_for_mask, exports.polygon_ZZ_round_radius_min * mask_radius_bias_for_mask, exports.polygon_ZZ_allows_edges) if exports.a_flag_ZZ_mask_square_round_fix else mask_5
	mask_7 = mask_cupsule(vector, exports.cupsule_ZZ_radius, exports.cupsule_ZZ_begin, exports.cupsule_ZZ_end) if exports.a_flag_ZZ_mask_cupsule else mask_6
	mask_8 = mask_clock_cupsule(vector, exports.cupsule_ZZ_radius, move, exports.cupsule_ZZ_center) if exports.a_flag_ZZ_mask_clock else mask_7
	mask_9 = mask_stripe(intensity, exports.stripe_ZZ_size * mask_radius_bias_for_mask) if exports.a_flag_ZZ_mask_stripe else mask_8
	mask_10 = mask_flash(cell_uv_alt.x + cell_uv_alt.y, exports.flash_ZZ_speed, exports.flash_ZZ_interval, exports.flash_ZZ_size, move) if exports.a_flag_ZZ_mask_flash else mask_9
	mask_11 = mask_aurora(cell_uv_alt, move, 2.0, 8.0, True) if exports.a_flag_ZZ_mask_aurora else mask_10
	mask_12 = dissolve_mask if exports.a_flag_ZZ_mask_dissolve else mask_11
	mask = mask_linear_range(mask_12, 1.0, mask_hollow_line_size * mask_radius_bias_for_line, exports.hollow_ZZ_center) if exports.a_flag_ZZ_mask_hollow else mask_12

	# 強度(通常2)
	intensity_alt_0 = op_switch_dir_multiply(ME.saturate(mask), intensity, exports.a_flag_ZZ_intensity_via_shape_01_alt, exports.a_flag_ZZ_intensity_via_shape_10_alt)
	intensity_alt_1 = op_switch_dir_multiply(dissolve_min_alpha, intensity_alt_0, exports.a_flag_ZZ_intensity_via_dissolve_01_alt, exports.a_flag_ZZ_intensity_via_dissolve_10_alt)
	intensity_alt_2 = ME.sample(exports.intensity_ZZ_curve, float2(intensity_alt_1, (exports.intensity_ZZ_easing + 0.5) / MFImageSizes.EasingCurve.value), SamplerTypes.Linear.value).x if exports.a_flag_ZZ_intensity_curve_alt else intensity_alt_1
	intensity_alt = ME.saturate((intensity_alt_2 - exports.intensity_ZZ_min) / (exports.intensity_ZZ_max - exports.intensity_ZZ_min)) if exports.a_flag_ZZ_intensity_stretch_alt else intensity_alt_2

	# 強度(ベースカラー/輪郭線)
	intensity_color = intensity_minimal if exports.a_flag_ZZ_color_intensity_via_minimal else intensity_alt
	intensity_line = intensity_minimal if exports.a_flag_ZZ_color_intensity_via_minimal_for_line else intensity_alt

	# 輪郭線
	# レイヤー単体で形状と輪郭線を合成するため別途マスクを生成 XXX powerは2.0 ~ 4.0程度が適当。小さいほど均し範囲が広くなるため太く見え、大きいと細く見えるがジャギが出る
	line_mask = mask_linear_range(mask, 1.0, mask_hollow_line_size * mask_radius_bias_for_line, exports.hollow_ZZ_center)
	line_alpha = 1.0 - ME.power(ME.saturate(line_mask), 2.5)

	# ベースカラー
	color_0 = color_gradation(exports.color_ZZ, exports.color_ZZ_b, intensity_color) if exports.a_flag_ZZ_color_gradation else exports.color_ZZ
	color_1 = color_gradation3(exports.color_ZZ, exports.color_ZZ_b, exports.color_ZZ_c, intensity_color) if exports.a_flag_ZZ_color_gradation3 else color_0
	color_2 = color_gradation_ab_to_c(exports.color_ZZ, exports.color_ZZ_b, exports.color_ZZ_c, intensity_color, ME.saturate(move)) if exports.a_flag_ZZ_color_gradation_ab_to_c else color_1
	color_3 = color_gradation_c_to_ab(exports.color_ZZ, exports.color_ZZ_b, exports.color_ZZ_c, intensity_color, ME.saturate(move)) if exports.a_flag_ZZ_color_gradation_c_to_ab else color_2
	color_4 = color_spectrum(intensity_color) if exports.a_flag_ZZ_color_spectrum else color_3
	color_5 = color_gradation(color_4, texture_color.xyz, exports.texture_ZZ_alpha * intensity_color) if exports.a_flag_ZZ_color_texture else color_4
	color_6 = color_gradation(color_5, exports.color_ZZ_line, line_alpha) if exports.a_flag_ZZ_color_line else color_5
	color_7 = color_gradation_c_to_ab(exports.color_ZZ_line, exports.color_ZZ_line_b, color_6, intensity_line, line_alpha) if exports.a_flag_ZZ_color_line_gradation else color_6
	color_8 = color_gradation_line_ab_to_c(exports.color_ZZ_line, exports.color_ZZ_line_b, exports.color_ZZ_line_c, color_7, intensity_line, ME.saturate(move), line_alpha) if exports.a_flag_ZZ_color_line_gradation_ab_to_c else color_7
	color = color_rotation(color_8, move) if exports.a_flag_ZZ_color_rotaion else color_8

	# 透過率
	opacity_0 = exports.opacity_ZZ * op_in(cell_unit_length, exports.clip_ZZ_length_min, exports.clip_ZZ_length_max) if exports.a_flag_ZZ_clip_length else exports.opacity_ZZ
	opacity_1 = opacity_0 * float(cell_unit_random <= exports.clip_ZZ_random) if exports.a_flag_ZZ_clip_random else opacity_0
	opacity_2 = opacity_1 * mask_rect(cell_unit_vector, float2(exports.clip_ZZ_rect_x, exports.clip_ZZ_rect_y), float2(exports.clip_ZZ_rect_center_x, exports.clip_ZZ_rect_center_y)) if exports.a_flag_ZZ_clip_rect else opacity_1
	opacity_3 = opacity_2 * mask_rect_edge(cell_unit_vector, float2(exports.clip_ZZ_rect_x, exports.clip_ZZ_rect_y), float2(exports.clip_ZZ_rect_center_x, exports.clip_ZZ_rect_center_y)) if exports.a_flag_ZZ_clip_rect_edge else opacity_2
	opacity_4 = opacity_3 * mask_square_side(vector, mask_hollow_line_size * mask_radius_bias_for_line, exports.polygon_ZZ_allows_sides) if exports.a_flag_ZZ_clip_square_sides else opacity_3
	opacity_5 = opacity_4 * texture_color.w if exports.a_flag_ZZ_color_trans_with_texture else opacity_4
	opacity = opacity_5 * intensity_alt if exports.a_flag_ZZ_color_trans else opacity_5
	return color, opacity, mask


@Embed.python
def ui_layer_00(uv: Annotated[float2, ME.tex_coord(0)], resolution: Annotated[float2, float2(250.0, 250.0)], dpi_scale: Annotated[float, ParametersValues.DPIScale.value]) -> tuple[float3, float, float]:
	"""UI用レイヤー(ダミー) @see ui_layer_ZZ"""
	return ui_layer_ZZ(uv, resolution, dpi_scale)


@Embed.python
def ui_layer_b1(uv: Annotated[float2, ME.tex_coord(0)], resolution: Annotated[float2, float2(250.0, 250.0)], dpi_scale: Annotated[float, ParametersValues.DPIScale.value]) -> tuple[float3, float, float]:
	"""UI用レイヤー(ダミー) @see ui_layer_ZZ"""
	return ui_layer_ZZ(uv, resolution, dpi_scale)
