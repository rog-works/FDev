from typing import Annotated

from script.mfs.me import ME
from script.mfs.me_types import float2
from script.mfs.mfs_00_preview import preview_distance


def op_not(value: Annotated[float, preview_distance()]) -> float:
	"""0と1を反転

	Args:
		value: 値 (0 or 1)
	Returns:
		0 or 1
	Note:
		入力値は0 or 1に限定。それ以外は全てエラーとする
	"""
	assert value in [0.0, 1.0]
	return 1.0 - value


def op_ge(value: Annotated[float, preview_distance()], threshold: Annotated[float, 0.0]) -> float:
	"""value >= threshold = 1

	Args:
		value: 値
		threshold: 閾値 (default = 0.0)
	Returns:
		0 or 1
	"""
	return ME.step(threshold, value)


def op_le(value: Annotated[float, preview_distance()], threshold: Annotated[float, 1.0]) -> float:
	"""value <= threshold = 1

	Args:
		value: 値
		threshold: 閾値 (default = 1.0)
	Returns:
		0 or 1
	"""
	return ME.step(value, threshold)


def op_gt(value: Annotated[float, preview_distance()], threshold: Annotated[float, 0.0]) -> float:
	"""value > threshold = 1

	Args:
		value: 値
		threshold: 閾値 (default = 0.0)
	Returns:
		0 or 1
	"""
	return 1.0 - ME.step(value, threshold)


def op_lt(value: Annotated[float, preview_distance()], threshold: Annotated[float, 1.0]) -> float:
	"""value < threshold = 1

	Args:
		value: 値
		threshold: 閾値 (deafult = 1.0)
	Returns:
		0 or 1
	"""
	return 1.0 - ME.step(threshold, value)


def op_in(value: Annotated[float, preview_distance()], minimum: Annotated[float, 0.0], maximum: Annotated[float, 1.0]) -> float:
	"""min <= value <= max

	Args:
		value: 値
		minimum: 下限 (deafult = 0.0)
		maximum: 上限 (deafult = 1.0)
	Returns:
		0 or 1
	"""
	return op_ge(value, minimum) * op_le(value, maximum)


def op_bit4_on(flags: Annotated[float, 1.0], index: Annotated[float, 1.0]) -> float:
	"""指定のビットを判定

	Args:
		flags: 1.0 ~ 15.0
		index: 1.0 ~ 4.0
	Returns:
		0 or 1
	"""
	mask_4 = float(index > 3.0)
	mask_3 = float(index < 4.0) * float(index > 2.0)
	mask_2 = float(index < 3.0) * float(index > 1.0)
	mask_1 = float(index < 2.0)
	bit4 = mask_4 * float((flags * 0.125) % 2.0 >= 1.0)
	bit3 = mask_3 * float((flags * 0.25) % 2.0 >= 1.0)
	bit2 = mask_2 * float((flags * 0.5) % 2.0 >= 1.0)
	bit1 = mask_1 * float(flags % 2.0 >= 1.0)
	return bit4 + bit3 + bit2 + bit1


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
