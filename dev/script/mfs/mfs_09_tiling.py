from typing import Annotated

from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.annotation import deprecated

from script.mfs.me import ME
from script.mfs.me_types import float2
from script.mfs.mfs_00_preview import preview_alpha
from script.mfs.mfs_01_op import op_switch_2d
from script.mfs.mfs_02_math import math_aspect2d, math_atan2_clock
from script.mfs.mfs_04_matrix import matrix_rotation2d
from script.mfs.mfs_06_uv import uv_radial


def tiling_3(value: Annotated[float, preview_alpha(1.0)], length: Annotated[float, 3.0], unit: Annotated[float, 1.0]) -> tuple[float, float, float]:
	"""全長を1として3分割し、中央値が先端と終端に繋がる様にループしてタイリング

	Args:
		value: 値
		length: 全長
		unit: 分割単位 (default = 1.0)
	Returns:
		(全体の進捗, セル単位の進捗, インデックス)
	Note:
		```
		先端: 0.0 ~ 1/3
		中央: 1/3 ~ 2/3
		終端: 2/3 ~ 1.0
		```
	"""
	in_a = float(value < unit)
	in_b = float(not in_a) * float(value < (length - unit))
	in_c = float(not ME.sign(in_a + in_b))

	b_length = length - unit * 2.0
	b_loops = ME.floor(b_length / unit + 0.999)
	b_unit = ME.min(b_length / b_loops, unit)
	# 中央値を等分割して余剰が出ないように補正
	b_value_0 = (value - unit) % b_unit
	b_value = b_value_0 / b_unit * unit

	wa = value * in_a
	wb = (unit + b_value) * in_b
	wc = (value - (length - unit * 3.0)) * in_c
	whole = wa + wb + wc

	ca = value / unit * in_a
	cb = (b_value_0 / b_unit) * in_b
	cc = (value - (length - unit)) / unit * in_c
	cell = ca + cb + cc

	ib = (1.0 + ME.floor((value - unit) / b_unit)) * in_b
	ic = (1.0 + b_loops) * in_c
	index = ib + ic
	return whole, cell, index


def tiling_3x3_wrap_index(uv_index: Annotated[float2, float2(0.0, 0.0)], cells: Annotated[float2, float2(3.0, 3.0)]) -> float:
	"""3x3タイリング時の外周インデックスを算出

	Args:
		uv_index: UV座標 (インデックス)
		cells: 軸毎のセルの数
	Returns:
		外周インデックス
	"""
	x_left = float(uv_index.x < 1.0)
	x_right = float(uv_index.x >= (cells.x - 1.0))
	y_top = float(uv_index.y < 1.0)
	y_bottom = float(uv_index.y >= (cells.y - 1.0))
	y_center = float(not y_top) * float(not y_bottom)

	x_top = uv_index.x * y_top
	x_top_v = cells.x
	y_right = (ME.min(uv_index.y - 1.0, cells.y - 2.0) + x_top_v) * (x_right * y_center)
	y_right_v = x_top_v + cells.y - 2.0
	x_bottom = ((cells.x - 1.0 - uv_index.x) + y_right_v) * y_bottom
	x_bottom_v = y_right_v + cells.x
	y_left = (ME.min(cells.y - 2.0 - uv_index.y, cells.y - 2.0) + x_bottom_v) * x_left * y_center
	return x_top + x_bottom + y_right + y_left


def tiling_uv(uv: Annotated[float2, ME.tex_coord(0)], tiles: Annotated[float, 2.0]) -> float2:
	"""UV座標のタイリング

	Args:
		uv: UV座標
		tiles: タイル数 (default = 2.0)
	Returns:
		UV座標
	"""
	return uv * tiles % 1.0


@Embed.python
@deprecated
def tiling_uv_3x3(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0]) -> float2:
	"""UV座標のタイリング(3x3)

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
	Returns:
		UV座標
	Note:
		```
		* 中央値をループし、先端と終端に繋げる。単純なため軽量
		* 単純で扱い易い反面、アスペクト比が偏るとセルが極端に縮小されてしまう問題あり
		@deprecated 未使用
		```
	"""
	fix_aspect2d = math_aspect2d(aspect)
	max_aspect2d = 1.0 / fix_aspect2d
	deform = uv / fix_aspect2d
	wx = tiling_3(deform.x * 3.0, max_aspect2d.x * 3.0, 1.0)[0]
	wy = tiling_3(deform.y * 3.0, max_aspect2d.y * 3.0, 1.0)[0]
	return float2(wx, wy) / 3.0


def tiling_uv_3x3_components(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0]) -> tuple[float2, float2, float2, float2]:
	"""UV座標のタイリング(3x3)の演算結果を生成

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
	Returns:
		(全体, セル毎, インデックス, 軸毎のセルの数)
	Note:
		```
		* セル毎に情報を細分化。組み合わせることで全体の進捗を1次元化することが出来る
		* 実質的にtiling_uv_3x3_wrap専用
		```
	"""
	fix_aspect2d = math_aspect2d(aspect)
	max_aspect2d = 1.0 / fix_aspect2d
	deform = uv / fix_aspect2d
	# XXX 分割代入は前方省略出来ないため、wx/wyは変数宣言のみ
	wx, cx, ix = tiling_3(deform.x * 3.0, max_aspect2d.x * 3.0, 1.0)
	wy, cy, iy = tiling_3(deform.y * 3.0, max_aspect2d.y * 3.0, 1.0)
	uv_whole = float2(wx, wy) / 3.0
	uv_cell = float2(cx, cy)
	uv_index = float2(ix, iy)
	cells = ME.floor(3.0 / fix_aspect2d + 0.999)
	return uv_whole, uv_cell, uv_index, cells


def tiling_uv_3x3_wrap_internal(uv_cell: Annotated[float2, float2(0.0, 0.0)], uv_index: Annotated[float2, float2(0.0, 0.0)], cells: Annotated[float2, float2(3.0, 3.0)]) -> float2:
	"""UV座標をタイリング(3x3/帯状)

	Args:
		uv_cell: UV座標 (セル毎)
		uv_index: UV座標 (インデックス)
		cells: 軸毎のセルの数
	Returns:
		UV座標
	"""
	# マスク
	mask_center_x = float(uv_index.x > 0.0) * float(uv_index.x < (cells.x - 1.0))
	mask_center_y = float(uv_index.y > 0.0) * float(uv_index.y < (cells.y - 1.0))
	mask_core = mask_center_x * mask_center_y
	mask_cross = (mask_center_x + mask_center_y) * float(not mask_core)
	mask_edge = float(not mask_cross) * float(not mask_core)

	# ベクトル
	mask_left = uv_index.x < 1.0
	mask_right = uv_index.x >= (cells.x - 1.0)
	mask_top = uv_index.y < 1.0
	mask_bottom = uv_index.y >= (cells.y - 1.0)
	vx = mask_left * -1.0 + mask_right * 1.0
	vy = mask_top * -1.0 + mask_bottom * 1.0

	# 回転角度
	u_theta_org = math_atan2_clock(vy, vx)
	u_edge = (1.0 - (u_theta_org - 0.125)) * mask_edge
	u_cross = (1.0 - u_theta_org) * mask_cross
	u_theta = u_edge + u_cross

	# 3x3
	uv_3x3 = matrix_rotation2d(uv_cell - 0.5, u_theta) + 0.5

	# X軸の進捗
	index = tiling_3x3_wrap_index(uv_index, cells)
	divides = (ME.max(cells.x, cells.y) * 2.0) + 2.0
	x_scale_radial = 4.0 / divides
	x_scale_whole = 1.0 / divides
	x_offset = index * x_scale_whole % 1.0
	x_whole = ME.min(x_offset + uv_3x3.x * x_scale_whole, 1.0)

	# UV
	uv_whole = float2(x_whole, uv_3x3.y)
	uv_edge_radial_0 = uv_radial(uv_3x3, float2(0.5, -0.5), 2.0)
	uv_edge_radial = float2(uv_edge_radial_0.x, 1.0 - uv_edge_radial_0.y)
	uv_edge = (uv_edge_radial * float2(x_scale_radial, 1.0) + float2(x_offset, 0.0)) * mask_edge
	uv_cross = uv_whole * mask_cross
	return uv_edge + uv_cross


@Embed.python
@deprecated
def tiling_uv_3x3_wrap(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0]) -> float2:
	"""UV座標をタイリング(3x3/帯状)

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
	Returns:
		UV座標
	Note:
		@deprecated 未使用
	"""
	# XXX 分割代入は前方省略出来ないため、uv_wholeは変数宣言のみ
	uv_whole, uv_cell, uv_index, cells = tiling_uv_3x3_components(uv, aspect)
	return tiling_uv_3x3_wrap_internal(uv_cell, uv_index, cells)


def tiling_uv_min_scroll(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0]) -> float2:
	"""UV座標のタイリング(比率小)

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
	Returns:
		UV座標
	"""
	aspect2d = math_aspect2d(aspect)
	return uv / aspect2d


def tiling_uv_even_for_ui(uv: Annotated[float2, ME.tex_coord(0)], tiles: Annotated[float, 1.0]) -> tuple[float2, float2, float2]:
	"""UV座標をタイリング(UI用/等分)

	Args:
		uv: UV座標
		tiles: タイリング数 (default = 1.0)
	Returns:
		(セル毎の進捗, インデックス, 軸毎のセルの数)
	"""
	uv_cell = tiling_uv(uv, tiles)
	uv_index = ME.floor(uv * tiles)
	cells = float2(tiles, tiles)
	return uv_cell, uv_index, cells


def tiling_uv_3x3_for_ui(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0], tiles: Annotated[float, 1.0]) -> tuple[float2, float2, float2]:
	"""UV座標をタイリング(UI用/3x3)

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
		tiles: タイリング数 (default = 1.0)
	Returns:
		(セル毎の進捗, インデックス, 軸毎のセルの数)
	"""
	uv_whole_3x3, uv_cell_3x3, uv_index_3x3, cells_3x3 = tiling_uv_3x3_components(uv, aspect)
	uv_cell = tiling_uv(uv_whole_3x3, tiles)
	in_tiles = ME.max(ME.floor(tiles / 3.0), 1.0)
	uv_index_offset = ME.floor(uv_cell_3x3 * in_tiles)
	uv_index = uv_index_3x3 * in_tiles + uv_index_offset
	cells = cells_3x3 * in_tiles
	return uv_cell, uv_index, cells


def tiling_uv_3x3_wrap_for_ui(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0], tiles: Annotated[float, 1.0]) -> tuple[float2, float2, float2]:
	"""UV座標をタイリング(UI用/3x3/帯状)

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
		tiles: タイリング数 (default = 1.0)
	Returns:
		(セル毎の進捗, インデックス, 軸毎のセルの数)
	"""
	# XXX 分割代入は前方省略出来ないため、uv_whole_3x3は変数宣言のみ
	uv_whole_3x3, uv_cell_3x3, uv_index_3x3, cells_3x3 = tiling_uv_3x3_components(uv, aspect)
	uv_cell = tiling_uv(tiling_uv_3x3_wrap_internal(uv_cell_3x3, uv_index_3x3, cells_3x3), tiles)
	uv_index_offset = ME.floor(uv_whole_3x3 * tiles) % tiles
	uv_index = uv_index_3x3 * tiles + uv_index_offset
	cells = cells_3x3 * tiles
	return uv_cell, uv_index, cells


def tiling_uv_min_scroll_for_ui(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0], tiles: Annotated[float, 1.0]) -> tuple[float2, float2, float2]:
	"""UV座標をタイリング(UI用/比率小)

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
		tiles: タイリング数 (default = 1.0)
	Returns:
		(セル毎の進捗, インデックス, 軸毎のセルの数)
	"""
	uv_whole = tiling_uv_min_scroll(uv, aspect)
	uv_cell = tiling_uv(uv_whole, tiles)
	uv_index_offset = ME.floor(uv_whole * tiles) % tiles
	uv_index = ME.floor(uv_whole) * tiles + uv_index_offset
	cells = ME.floor(1.0 / math_aspect2d(aspect) + 0.999) * tiles
	return uv_cell, uv_index, cells


def tiling_uv_for_ui(uv: Annotated[float2, ME.tex_coord(0)], aspect: Annotated[float, 1.0], tiles: Annotated[float, 1.0], on_3x3: Annotated[bool, False], on_3x3_wrap: Annotated[bool, False], on_scroll: Annotated[bool, False]) -> tuple[float2, float2, float2]:
	"""UV座標をタイリング(UI用)

	Args:
		uv: UV座標
		aspect: アスペクト比 (default = 1.0)
		tiles: タイリング数 (default = 1.0)
		on_3x3: フラグ(3x3) (default = False)
		on_3x3_wrap: フラグ(3x3/帯状) (default = False)
		on_scroll: フラグ(比率小) (default = False)
	Returns:
		(進捗, インデックス, 軸毎のセルの数)
	"""
	uv_cell_0, uv_index_0, cells_0 = tiling_uv_even_for_ui(uv, tiles)
	uv_cell_1, uv_index_1, cells_1 = tiling_uv_3x3_for_ui(uv, aspect, tiles)
	uv_cell_2, uv_index_2, cells_2 = tiling_uv_3x3_wrap_for_ui(uv, aspect, tiles)
	uv_cell_3, uv_index_3, cells_3 = tiling_uv_min_scroll_for_ui(uv, aspect, tiles)
	uv_cell = uv_cell_3 if on_scroll else op_switch_2d(uv_cell_1, uv_cell_2, uv_cell_0, on_3x3, on_3x3_wrap)
	uv_index = uv_index_3 if on_scroll else op_switch_2d(uv_index_1, uv_index_2, uv_index_0, on_3x3, on_3x3_wrap)
	cells = cells_3 if on_scroll else op_switch_2d(cells_1, cells_2, cells_0, on_3x3, on_3x3_wrap)
	return uv_cell, uv_index, cells
