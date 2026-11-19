from typing import Annotated

from script.mfs.me import ME


def time_alpha(speed: Annotated[float, 1.0]) -> float:
	"""経過時間からα値を生成

	Args:
		speed: 速度 (default = 1.0)
	Returns:
		α値 (0 ~ 1)
	"""
	return (ME.time() * speed) % 1.0
