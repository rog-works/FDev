from os import environ
from typing import ClassVar


class PyEnviron:
	"""Python環境変数ラッパー

	Note:
		```
		XXX os.environは純粋なdictではないため参照が異常に遅い
		```
	"""

	environ: ClassVar[dict[str, str]] = environ.copy()

	@classmethod
	def verbose_on(cls) -> bool:
		"""ログ出力の切り替え

		Returns:
			True = 標準出力にログを出力
		Note:
			```
			@see App.Main.Core.Core
			```
		"""
		return 'PYVERBOSE' in cls.environ
