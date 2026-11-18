from enum import Enum
from typing import cast

from compatible.error import Errors


class EnumAsInt:
	"""Enumのint変換トレイト
	
	Examples:
		```python
		# 継承はEnumより前に書くことが必須
		class Values(EnumAsInt, Enum): ...
		```
	"""

	def __int__(self) -> int:
		"""Returns: 値 or インデックス Note: int型以外はインデックスを返却"""
		for index, value in enumerate(cast(type[Enum], self.__class__)):
			if value == self:
				return value.value if isinstance(value.value, int) else index

		raise Errors.Never(self)
		return -1
