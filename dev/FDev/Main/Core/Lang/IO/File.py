from typing import Annotated, cast

from tranp.app.compatible.cpp.classes import uint8
from tranp.app.compatible.cpp.cvar import CRef
from tranp.app.compatible.python.embed import Embed
from tranp.app.lang.convertion import as_a
from UE5.Core.Containers.StringConv import UTF8_TO_TCHAR
from UE5.Core.Misc.FileHelper import FileHelper
from UE5.Core.Misc.Paths import Paths

from compatible.error import Errors
from FDev.Main.Const.ProjectConst import ClassPrefixs


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class Files:
	"""ファイル操作ヘルパー"""

	@classmethod
	def exiets(cls, filepath: str) -> bool:
		"""ファイルが存在するか判定

		Args:
			filepath: ファイルパス (プロジェクトルートからの相対パス)
		Returns:
			True = 存在
		"""
		abs_filepath = Paths.Combine(Paths.ProjectDir(), filepath)
		return Paths.FileExists(abs_filepath)

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
		buffer = cls.__make_buffer()
		output = CRef(buffer)
		ok = FileHelper.LoadFileToArray(output, abs_filepath.encode())
		if not ok:
			raise Errors.NotFound(cls.load, abs_filepath)

		return cls.__to_str(output)

	@classmethod
	@Embed.python
	def __make_buffer(cls) -> list[uint8]:
		"""Returns: バイト配列 @python str"""
		# XXX Pythonで型ヒントが成り立たないのは一旦許容する
		return cast(list[uint8], '')

	@classmethod
	@Embed.alias(__make_buffer.__name__)
	def __make_buffer_cpp(cls) -> list[uint8]:
		"""Returns: バイト配列"""
		return []

	@classmethod
	@Embed.python
	def __to_str(cls, output: Annotated[CRef[list[uint8]], Embed.mutable]) -> str:
		"""Args: output: 出力 @python CRef[str] Returns: 変換後の文字列"""
		# XXX Pythonで型ヒントが成り立たないのは一旦許容する
		return as_a(str, output.raw)

	@classmethod
	@Embed.alias(__to_str.__name__)
	def __to_str_cpp(cls, output: Annotated[CRef[list[uint8]], Embed.mutable]) -> str:
		"""Args: output: 出力 Returns: 変換後の文字列"""
		output.raw.append(cast(uint8, 0))
		return UTF8_TO_TCHAR(output)
