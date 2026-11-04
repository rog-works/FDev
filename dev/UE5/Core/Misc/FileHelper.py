from typing import cast

from tranp.app.compatible.cpp.classes import uint8
from tranp.app.compatible.cpp.cvar import CRef
from tranp.app.compatible.python.embed import Embed

from compatible.error import Errors


@Embed.alias('F', prefix=True)
class FileHelper:
	"""ファイル操作ヘルパー"""

	@classmethod
	def LoadFileToArray(cls, output: CRef[list[uint8]], filepath: bytes) -> bool:
		"""指定のファイルをロード

		Args:
			output: 出力 @python CRef[str]
			filepath: ファイルパス
		Returns:
			True = 成功
		Note:
			```
			XXX Pythonでoutputの型ヒントが成り立たないのは一旦許容する
			@see UE5.Core.Containers.StringConv
			```
		"""
		if not isinstance(output.raw, str):
			raise Errors.InvalidArguments(output, filepath)

		with open(filepath.decode(), mode='r', encoding='utf-8') as f:
			output.copy_proxy(cast(CRef[list[uint8]], CRef(f.read())))
			return True
