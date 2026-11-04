# @see Engine/Source/Runtime/Core/Public/Misc/Guid.h

from typing import Annotated
from uuid import uuid4

from tranp.app.compatible.python.embed import Embed


@Embed.alias('F', prefix=True)
class Guid:
	"""UUID
	
	Note:
		```
		* 初期値は全て0であり、無効な値として扱われる
		* UUIDの仕様とは一切関係なく、あくまで32文字の16進数文字列として一意性を表現
		```
	"""

	uuid: str

	def __init__(self) -> None:
		"""インスタンスを生成"""
		# @python
		self.uuid = '0' * 32

	@classmethod
	def NewGuid(cls) -> 'Guid':
		"""インスタンスを生成

		Returns:
			インスタンス
		"""
		instance = cls()
		instance.uuid = uuid4().hex
		return instance

	def ToString(self) -> str:
		"""Returns: 文字列表現"""
		return self.uuid


def LexFromString(guid: Annotated['Guid', Embed.immutable], hex_str: bytes) -> None:
	"""16進数文字列からインスタンスを復元

	Args:
		guid: インスタンス
		hex_str: 16進数文字列
	"""
	guid.uuid = hex_str.decode()
