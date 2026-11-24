from typing import Annotated

from const.const_material import ParametersValues
from script.mfs.core.me import ME
from script.mfs.core.me_types import float2, float3
from script.mfs.func.color.mfs_color import color_blend_a, color_gradation_ab_to_c
from script.mfs.func.exports.mfs_exports import exports_ui_main
from script.mfs.func.op.mfs_op_logic import op_and, op_or, op_switch_ab
from script.mfs.func.pixel.mfs_pixel import pixel_antialias
from script.mfs.func.ui.mfs_ui_layer import ui_layer_00, ui_layer_b1
from script.mfs.func.uv.mfs_uv import uv_to_resolution


def ui_blend_layer(
	color_fg: Annotated[float3, float3(0.0, 0.0, 0.0)],
	color_bg: Annotated[float3, float3(0.0, 0.0, 0.0)],
	mask_fg: Annotated[float, 0.0],
	mask_bg: Annotated[float, 0.0],
	opacity_fg: Annotated[float, 0.0],
	opacity_bg: Annotated[float, 0.0],
	anti_fg: Annotated[float, 0.0],
	anti_bg: Annotated[float, 0.0]
) -> tuple[float3, float]:
	"""UI用レイヤー合成

	Args:
		color_fg: ベースカラー(前景)
		color_bg: ベースカラー(背景)
		mask_fg: マスク(前景)
		mask_bg: マスク(背景)
		opacity_fg: 透過率(前景)
		opacity_bg: 透過率(背景)
		anti_fg: アンチエイリアス(前景)
		anti_bg: アンチエイリアス(背景)
	Returns:
		ベースカラー, アンチエイリアス
	Note:
		```
		### カラー合成の留意事項
		* 色が無い=黒ではないため、黒とベースカラーを合成してはならない
		* 必ずベースカラー同士を合成する必要があるため、全ての合成パターンを列挙し、有効な1パターンの結果だけを使う
		### 透過合成(前提)
		* 背景が透過の場合、投影先の色がマテリアル内で未確定なため、本質的には合成が成り立たない
		* また、アンチエイリアスを付ける場合、背景且つ不透過であったとしても輪郭線上は透過なため、実質的に前景/背景どちらの場合でも結果的に透過合成になり、これも成り立たない
		### 透過合成
		* 前提を踏まえた上で、完璧な合成結果をあえて捨て、それっぽく見える透過合成を実現
		* 不完全性: α値の低い前景を透過合成すると理想からより大きく離れる ※そもそも不正確である前提であり、許容できる程度の誤差
		```
	Example:
		```python
		# XXX 否決案の備忘録 (理由: 背景が透過、且つ前景のα値が0から0より大きくなる際に色飛びが発生する)
		color_blend = color_gradation(color_gradation(color_fg, color_bg, alpha_bg), color_fg, alpha_fg) * on_blend
		```
	"""
	not_fg = float(not mask_fg)
	not_bg = float(not mask_bg)

	on_fg = mask_fg * not_bg
	on_bg = mask_bg * not_fg
	on_blend = mask_fg * mask_bg
	on_outside = not_fg * not_bg

	alpha_fg = opacity_fg * anti_fg
	alpha_bg = opacity_bg * anti_bg
	# XXX `alpha_bg / alpha_fg`に必然性はないが、色飛びを防止をできる。半面、前景が低α値の際に背景の色見が強く出てしまう欠点有り
	alpha_target = ME.saturate(alpha_bg / ME.clamp(alpha_fg, 0.001, 1.0))
	color_fg_only = color_fg * on_fg
	color_bg_only = color_bg * on_bg
	# 前景と背景を背景のα値で合成し、その結果と前景を前景のα値で合成
	color_blend = color_gradation_ab_to_c(color_fg, color_bg, color_fg, alpha_target, alpha_fg) * on_blend
	color = color_fg_only + color_bg_only + color_blend

	opacity = color_blend_a(opacity_bg, opacity_fg)
	opacity_anti = color_blend_a(alpha_bg, alpha_fg)
	anti_fg_only = anti_fg * on_fg
	anti_bg_only = anti_bg * on_bg
	# 透過率からアンチエイリアス適用後の透過率にするための減衰倍率を算出 (opacity: 透過率, opacity_anti: アンチエイリアス適用後の透過率)
	anti_blend = ME.saturate(opacity_anti / ME.clamp(opacity, 0.001, 1.0)) * on_blend
	anti_outside = 1.0 * on_outside
	anti = anti_fg_only + anti_bg_only + anti_blend + anti_outside
	return color, anti


def ui_main(uv: Annotated[float2, ME.tex_coord(0)]) -> tuple[float3, float]:
	"""UI用マテリアルエントリーポイント

	Args:
		uv: UV座標
	Returns:
		(ベースカラー, α値)
	"""
	exports = exports_ui_main()

	# 解像度
	dpi_scale = ME.const_by(ParametersValues.DPIScale.name)
	resolution = float2(exports.resolution_width, exports.resolution_height) if exports.a_flag_resolution_manualy else uv_to_resolution(uv, dpi_scale)

	# レイヤー
	color_00_0, opacity_00_0, intensity_00 = ui_layer_00(uv, resolution, dpi_scale)
	color_b1_0, opacity_b1_0, intensity_b1 = ui_layer_b1(uv, resolution, dpi_scale)

	# マスク
	mask_00_1 = float(intensity_00 <= 1.0) * float(opacity_00_0 > 0.0) if exports.a_flag_00 else 0.0
	mask_b1_1 = float(intensity_b1 <= 1.0) * float(opacity_b1_0 > 0.0) if exports.a_flag_b1 else 0.0
	mask_00 = 0.0 if exports.a_flag_blend_b1_not_00 else op_or(mask_00_1 * mask_b1_1, mask_00_1, exports.a_flag_blend_00_and_b1_on_b1, exports.a_flag_blend_b1_and_00)
	mask_b1 = op_switch_ab(mask_b1_1 * mask_00_1, mask_b1_1 * (not mask_00_1), mask_b1_1, exports.a_flag_blend_b1_and_00, exports.a_flag_blend_b1_not_00)

	# アンチエイリアス
	anti_00_0 = op_and(pixel_antialias(intensity_00), mask_00, exports.a_flag_00, exports.a_flag_00_anti)
	anti_b1_0 = op_and(pixel_antialias(intensity_b1), mask_b1, exports.a_flag_b1, exports.a_flag_b1_anti)
	anti_00 = op_or(anti_00_0 * anti_b1_0, anti_00_0, exports.a_flag_blend_00_and_b1_on_b1, exports.a_flag_blend_b1_and_00)
	anti_b1 = anti_00_0 * anti_b1_0 if exports.a_flag_blend_b1_and_00 else anti_b1_0

	# α値
	opacity_00 = opacity_00_0 * mask_00 if exports.a_flag_00 else 0.0
	opacity_b1 = opacity_b1_0 * mask_b1 if exports.a_flag_b1 else 0.0

	# ベースカラー
	color_00 = color_00_0 if exports.a_flag_00 else float3(0.0, 0.0, 0.0)
	color_b1 = color_b1_0 if exports.a_flag_b1 else float3(0.0, 0.0, 0.0)
	color_blend, anti_blend = ui_blend_layer(color_00, color_b1, mask_00, mask_b1, opacity_00, opacity_b1, anti_00, anti_b1)
	color = (color_blend if exports.a_flag_b1 else color_00) if exports.a_flag_00 else color_b1
	anti = (anti_blend if exports.a_flag_b1 else anti_00) if exports.a_flag_00 else anti_b1

	# 透過率
	opacity_0 = opacity_00 if exports.a_flag_00 else 0.0
	opacity_1 = color_blend_a(opacity_b1, opacity_0) if exports.a_flag_b1 else opacity_0
	opacity = opacity_1 * anti
	return color, opacity
