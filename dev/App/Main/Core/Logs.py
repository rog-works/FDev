from collections.abc import Callable
from enum import Enum
from typing import ClassVar

from tranp.app.compatible.python.embed import Embed

from compatible.enum import EnumAsInt
from helper.env.py_environ import PyEnviron


class Logs:
	"""ロガー"""

	class Flags(EnumAsInt, Enum):
		"""ログ出力フラグ Note: XXX 最上位バイトを使うとC++でコンパイルエラーになるため使用禁止"""
		asset = 0x00000002
		editor = 0x00000800
		all = 0x0fffffff

	class Destinations(EnumAsInt, Enum):
		"""ログの入出力先"""
		defaults = 0x0001
		all = 0xffff

	enabled: ClassVar = True
	__dest_in: ClassVar = int(Destinations.defaults)
	__dest_out: ClassVar = int(Destinations.defaults)
	__flags: ClassVar = int(Flags.all)

	# region 出力フラグ管理

	@classmethod
	@Embed.python
	def ok(cls, flag: Flags) -> bool:
		"""Args: flag: ログ出力フラグ Returns: True = 出力有効 Note: @python"""
		return PyEnviron.verbose_on()

	@classmethod
	@Embed.alias(ok.__name__)
	def ok_cpp(cls, flag: Flags) -> bool:
		"""Args: flag: ログ出力フラグ Returns: True = 出力有効 Note: @cpp"""
		return cls.enabled and (cls.__dest_in & cls.__dest_out) != 0 and (cls.__flags & int(flag)) != 0

	@classmethod
	def dest_in_ok(cls, destination: Destinations) -> bool:
		"""Args: destination: 入力元 Returns: True = 出力有効"""
		return (cls.__dest_in & int(destination)) != 0

	@classmethod
	def dest_in_on(cls, destination: Destinations) -> None:
		"""入力元追加 Args: destination: 入力元"""
		cls.__dest_in |= int(destination)

	@classmethod
	def dest_in_off(cls, destination: Destinations) -> None:
		"""入力元削除 Args: destination: 入力元"""
		cls.__dest_in &= ~int(destination)

	@classmethod
	def dest_out(cls, destination: Destinations = Destinations.defaults) -> None:
		"""出力先変更 Args: destination: 出力先 (default = defaults)"""
		cls.__dest_out = int(destination)

	@classmethod
	def flag_ok(cls, flag: Flags) -> bool:
		"""Args: flag: ログ出力フラグ Returns: True = 出力有効(個別)"""
		return (cls.__flags & int(flag)) != 0

	@classmethod
	def on(cls, flag: Flags) -> None:
		"""出力追加 Args: flag: ログ出力フラグ"""
		cls.__flags |= int(flag)

	@classmethod
	def off(cls, flag: Flags) -> None:
		"""出力削除 Args: flag: ログ出力フラグ"""
		cls.__flags &= ~int(flag)

	# endregion
	# region ログ出力

	@classmethod
	@Embed.python
	def warning(cls, calls: Callable, text: str = '') -> None:
		"""ログ出力(warning) @python"""
		cls.__put(cls.warning.__name__, calls, text)

	@classmethod
	@Embed.python
	def error(cls, calls: Callable, text: str = '') -> None:
		"""ログ出力(error) @python"""
		cls.__put(cls.error.__name__, calls, text)

	@classmethod
	@Embed.python
	def asset(cls, calls: Callable, text: str = '') -> None:
		"""ログ出力(asset) @python"""
		cls.__put(cls.asset.__name__, calls, text)

	@classmethod
	@Embed.python
	def editor(cls, calls: Callable, text: str = '') -> None:
		"""ログ出力(editor) @python"""
		cls.__put(cls.editor.__name__, calls, text)

	@classmethod
	@Embed.python
	def __put(cls, tag: str, calls: Callable, text: str) -> None:
		"""ログ出力 Args: tag: タグ名 calls: 呼び出し元, text: 本文 @python"""
		if cls.ok(cls.Flags.all):
			print(f'[#{tag}] [{calls.__qualname__}]: {text}')

	# endregion
