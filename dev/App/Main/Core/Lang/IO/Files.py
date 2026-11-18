from tranp.app.compatible.cpp.classes import uint8
from tranp.app.compatible.cpp.cvar import CRef
from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.convertion import as_a
from UE5.Core.Containers.StringConv import UTF8_TO_TCHAR, TCHARToUTF8_Convert
from UE5.Core.Misc.FileHelper import FileHelper
from UE5.Core.Misc.Paths import Paths
from UE5.Core.Serialization.BufferArchive import BufferArchive

from compatible.error import Errors


class Files:
	"""ファイル操作ヘルパー"""

	@classmethod
	def exists(cls, filepath: str) -> bool:
		"""ファイルが存在するか判定

		Args:
			filepath: ファイルパス (プロジェクトルートからの相対パス)
		Returns:
			True = 存在
		"""
		abs_filepath = Paths.Combine(Paths.ProjectDir(), filepath)
		return Paths.FileExists(abs_filepath)

	@classmethod
	def save(cls, filepath: str, content: str) -> bool:
		"""ファイルを保存

		Args:
			filepath: ファイルパス (プロジェクトルートからの相対パス)
			content: コンテンツ
		Returns:
			True = 保存成功
		"""
		abs_filepath = Paths.Combine(Paths.ProjectDir(), filepath)
		size_8 = TCHARToUTF8_Convert.ConvertedLength(content.encode(), len(content))
		buff_8 = BufferArchive()
		buff_8.SetNumZeroed(size_8)
		TCHARToUTF8_Convert.Convert(buff_8.GetData(), size_8, content.encode(), len(content))
		return FileHelper.SaveArrayToFile(buff_8, abs_filepath.encode())

	@classmethod
	def load(cls, filepath: str) -> str:
		"""ファイルを読み込み

		Args:
			filepath: ファイルパス (プロジェクトルートからの相対パス)
		Returns:
			コンテンツ
		Raises:
			NotFound: ファイルが存在しない
		"""
		abs_filepath = Paths.Combine(Paths.ProjectDir(), filepath)
		buff = BufferArchive()
		if not FileHelper.LoadFileToArray(buff, abs_filepath.encode()):
			raise Errors.NotFound(cls.load, abs_filepath)

		return cls.__to_str(CRef(buff))

	@classmethod
	@Embed.python
	def __to_str(cls, buff: CRef[BufferArchive]) -> str:
		"""Args: buff: バイト配列 Returns: 変換後の文字列"""
		return as_a(str, buff.on.GetData()[0])

	@classmethod
	@Embed.alias(__to_str.__name__)
	def __to_str_cpp(cls, buff: CRef[BufferArchive]) -> str:
		"""Args: buff: バイト配列 Returns: 変換後の文字列"""
		buff.on.Add(uint8(0))
		return UTF8_TO_TCHAR(buff.on.GetData())
