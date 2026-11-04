from typing import Annotated

from tranp.app.compatible.python.embed import Embed

from FDev.Main.Const.ProjectConst import Aliases


@Embed.alias(Aliases.General.value, prefix=True)
class CoreError(Exception):
	"""例外(アプリケーション)

	Note:
		```
		* トランスパイル後に参照されるクラスのため、Python上は原則使用禁止
		@see compatible.error.CompatibleError
		@see data/template/statement/throw.j2
		```
	"""

	__message: str

	def __init__(self, message: str) -> None:
		"""インスタンスを生成

		Args:
			message: エラーメッセージ
		"""
		super().__init__()
		self.__message = message

	@Embed.pure
	def message(self) -> Annotated[str, Embed.immutable]:
		"""Returns: エラーメッセージ @immutable"""
		return self.__message
