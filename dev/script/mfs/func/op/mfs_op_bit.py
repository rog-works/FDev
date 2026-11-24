from typing import Annotated


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

