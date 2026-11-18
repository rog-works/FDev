# @see Engine/Source/Runtime/Core/Public/Containers/StringConv.h

from tranp.app.compatible.cpp.classes import uint8
from tranp.app.compatible.python.embed import Embed

from compatible.error import Errors


@Embed.alias('F', prefix=True)
class TCHARToUTF8_Convert:
	"""エンコードコンバーター(UTF-16 -> UTF-8)"""

	@classmethod
	def Convert(cls, output_8: list[uint8], size_8: int, bytes_16: bytes, size_16: int) -> None:
		"""エンコードを変換

		Args:
			output_8: バイト配列(UTF-8) ※C++ではCP[char]
			size_8: サイズ(UTF-8)
			bytes_16: バイト配列(UTF-16) ※C++ではCP[TCHAR]
			size_16: サイズ(UTF-16)
		Note:
			XXX Pythonでは使用禁止 @see data/template/func_call/default.j2
		"""
		raise Errors.Never

	@classmethod
	def ConvertedLength(cls, bytes_16: bytes, size_16: int) -> int:
		"""変換後のサイズを算出

		Args:
			bytes_16: バイト配列(UTF-16) ※C++ではCP[TCHAR]
			size_16: サイズ(UTF-16)
		Returns:
			サイズ
		"""
		return size_16


def UTF8_TO_TCHAR(buff: list[uint8]) -> str:
	"""エンコードを変換(UTF-8 -> UTF-16)

	Args:
		buff: バイト配列(UTF-8) ※C++ではCP[char]
	Returns:
		バイト配列(UTF-16) ※C++ではCP[TCHAR]
	Note:
		XXX Pythonでは使用禁止 @see data/template/func_call/default.j2
	"""
	raise Errors.Never
