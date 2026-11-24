from typing import Annotated

from script.mfs.core.me_types import float2
from script.mfs.func.preview.mfs_preview import preview_distance


def op_and(value: Annotated[float, preview_distance()], defaults: Annotated[float, 0.0], is_a: Annotated[bool, False], is_b: Annotated[bool, False]) -> float:
	"""AND条件

	Args:
		value: 値
		defaults: デフォルト値
		is_a: 条件A
		is_b: 条件B
	Returns:
		真の値
	"""
	return (value if is_b else defaults) if is_a else defaults


def op_or(value: Annotated[float, preview_distance()], defaults: Annotated[float, 0.0], is_a: Annotated[bool, False], is_b: Annotated[bool, False]) -> float:
	"""OR条件

	Args:
		value: 値
		defaults: デフォルト値
		is_a: 条件A
		is_b: 条件B
	Returns:
		真の値
	"""
	return value if is_a else (value if is_b else defaults)


def op_switch_ab(a: Annotated[float, 0.0], b: Annotated[float, 0.5], defaults: Annotated[float, 1.0], is_a: Annotated[bool, False], is_b: Annotated[bool, False]) -> float:
	"""入力値ABの切り替え。どちらも無効な場合はデフォルト値を返す

	Args:
		a: 値A
		b: 値B
		defaults: デフォルト値
		is_a: True = Aが有効
		is_b: True = Bが有効
	Returns:
		真の値
	"""
	return a if is_a else (b if is_b else defaults)


def op_switch_2d(a: Annotated[float2, float2(0.0, 0.0)], b: Annotated[float2, float2(0.5, 0.5)], defaults: Annotated[float2, float2(1.0, 1.0)], is_a: Annotated[bool, False], is_b: Annotated[bool, False]) -> float2:
	"""入力値ABの切り替え。どちらも無効な場合はデフォルト値を返す

	Args:
		a: 値A
		b: 値B
		defaults: デフォルト値
		is_a: True = Aが有効
		is_b: True = Bが有効
	Returns:
		真の値
	"""
	return a if is_a else (b if is_b else defaults)


def op_switch_dir(then: Annotated[float, 0.0], defaults: Annotated[float, 1.0], is_01: Annotated[bool, False], is_10: Annotated[bool, False]) -> float:
	"""進行方向に沿って入力値を取得。どちらも無効な場合はデフォルト値を返す

	Args:
		then: 値
		defaults: デフォルト値
		is_01: True = 0 -> 1
		is_10: True = 1 -> 0
	Returns:
		真の値
	"""
	return then if is_01 else (1.0 - then if is_10 else defaults)


def op_switch_dir_multiply(then: Annotated[float, 0.0], defaults: Annotated[float, 1.0], is_01: Annotated[bool, False], is_10: Annotated[bool, False]) -> float:
	"""進行方向に沿って入力値を取得し、デフォルト値と乗算。どちらも無効な場合はデフォルト値を返す

	Args:
		then: 値
		defaults: デフォルト値
		is_01: True = 0 -> 1
		is_10: True = 1 -> 0
	Returns:
		真の値
	"""
	return defaults * then if is_01 else (defaults * (1.0 - then) if is_10 else defaults)
