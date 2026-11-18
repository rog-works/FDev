# @see Engine/Source/Runtime/Core/Public/Serialization/Archive.h

from abc import abstractmethod
from typing import Any

from tranp.app.compatible.python.embed import Embed


@Embed.alias('F', prefix=True)
class Archive:
	"""ストリーム(基底)"""

	def Num(self) -> int:
		"""バイト配列のサイズを取得

		Returns:
			バイト配列のサイズ
		"""
		return len(self.GetData())

	@abstractmethod
	def GetData(self) -> list[Any]:
		"""Returns: 内部ポインター ※C++ではCP[uint8]"""
		...

	@abstractmethod
	@Embed.python
	def set_data(self, buff: list[Any]) -> None:
		"""Args: buff: バイト配列 @python"""
		...
