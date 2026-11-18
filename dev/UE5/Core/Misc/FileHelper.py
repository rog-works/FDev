# @see Engine/Source/Runtime/Core/Public/Misc/FileHelper.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Serialization.BufferArchive import BufferArchive


@Embed.alias('F', prefix=True)
class FileHelper:
	"""ファイル操作ヘルパー"""

	@classmethod
	def SaveArrayToFile(cls, buff: BufferArchive, filepath: bytes) -> bool:
		"""
		Args:
			buff: バイト配列
			filepath: ファイルパス(絶対パス)
		Returns:
			True = 成功
		"""
		...

	@classmethod
	def LoadFileToArray(cls, output: BufferArchive, filepath: bytes) -> bool:
		"""指定のファイルをロード

		Args:
			output: バイト配列(出力)
			filepath: ファイルパス(絶対パス)
		Returns:
			True = 成功
		"""
		with open(filepath.decode(), mode='r', encoding='utf-8') as f:
			BufferArchive.write(output, f.read())
			return True
