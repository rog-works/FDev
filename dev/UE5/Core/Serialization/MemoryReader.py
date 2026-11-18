# @see Engine/Source/Runtime/Core/Public/Serialization/MemoryReader.h

from typing import Any, override

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Serialization.Archive import Archive

from compatible.error import Errors


@Embed.alias('F', prefix=True)
class MemoryReader(Archive):
	"""ストリームリーダー"""

	buff: Archive

	def __init__(self, buff: Archive) -> None:
		"""インスタンスを生成

		Args:
			buff: バイト配列 ※C++ではlist[uint8]
		"""
		self.buff = buff

	# region ストリーム

	@override
	def GetData(self) -> list[Any]:
		"""Returns: 内部ポインター ※C++ではCP[uint8]"""
		return self.buff.GetData()

	@override
	def set_data(self, buff: list[Any]) -> None:
		"""Args: buff: バイト配列 @python"""
		raise Errors.Unsupported
