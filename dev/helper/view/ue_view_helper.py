from collections.abc import Callable
from itertools import chain
from re import compile as re_compile
from re import search as re_search
from typing import ClassVar

from tranp.app.implements.cpp.view.cpp_view_helper import factories_for_cpp
from tranp.app.lang.string import is_quoted_literal
from tranp.app.view.helper.block import BlockParser
from tranp.app.view.helper.helper import factories
from tranp.app.view.render import RendererHelperProvider, RendererSetting
from UE5.CoreUObject.UObject.ObjectMacros import UPROPERTY

from App.Main.Core.Logs import Logs

flatten = chain.from_iterable


class UEMetaArgHelper:
	"""UEメタデータ引数ヘルパー"""

	@classmethod
	def parse(cls, meta_arg: str) -> 'UEMetaArgHelper':
		"""メタデータ引数を解析してインスタンスを生成

		Args:
			meta_arg: 引数
		Returns:
			インスタンス
		"""
		args_begin = meta_arg.find('(')
		label = meta_arg[:args_begin]
		args_str = meta_arg[args_begin + 1:-1]
		return cls(label, args_str)

	def __init__(self, label: str, args_str: str) -> None:
		"""インスタンスを生成

		Args:
			label: ラベル
			args_str: 引数リスト ※文字列
		"""
		self.label = label
		self.args_str = args_str

	def format(self) -> str:
		"""Returns: 書式化"""
		return f'{self.label}={self.args_str}' if self.args_str else self.label


class UEMetaHelper:
	"""UEメタデータヘルパー

	Note:
		```
		### 期待値
		1. `{A()}`
		2. `{A("a")}`
		2. `{A("a, b")}`
		3. `{A("a"), B("b, c")}`
		```
	"""

	@classmethod
	def parse(cls, meta: str) -> 'UEMetaHelper':
		"""メタデータを解析してインスタンスを生成

		Args:
			meta: メタデータ
		Returns:
			インスタンス
		"""
		args = BlockParser.break_separator(meta[1:-1], ',')
		return cls([UEMetaArgHelper.parse(arg) for arg in args])

	def __init__(self, args: list[UEMetaArgHelper]) -> None:
		"""インスタンスを生成

		Args:
			args: 引数リスト
		"""
		self.args = args

	def format(self) -> str:
		"""Returns: 書式化"""
		join_args = ', '.join([arg.format() for arg in self.args])
		return f'({join_args})'


class UEViewHelper:
	"""ビューヘルパー(UE用)"""

	_DeclVarPattern: ClassVar = re_compile(r'^(public|protected|private):[^{=]+[\w\d]+;$')

	@classmethod
	def filter_decl_var(cls, statements: list[str], subject) -> list[str]:
		"""メンバー変数定義の行を抜き出す

		Args:
			statements: ステートメントリスト
			subject: 追加の検索条件
		Returns:
			ステートメントリスト
		"""
		return [statement for statement in statements if (len(subject) == 0 or subject in statement) and re_search(cls._DeclVarPattern, statement)]

	@classmethod
	def parse_decl_var(cls, decl_var: str) -> tuple[str, str, str, str]:
		"""メンバー変数定義をパース

		Args:
			decl_var: 変数定義
		Returns:
			(アクセス修飾子, アノテーション, 型名, 変数名)
		"""
		remain = decl_var

		end = remain.find(':')
		accessor = remain[:end]
		remain = remain[end + 2:]

		annotation = ''
		if remain.startswith(UPROPERTY.__name__):
			elems = BlockParser.break_last_block(remain, '()')
			annotation = f'{elems[0]}({elems[1]})'
			remain = remain[len(annotation) + 1:]

		var_type = ''
		if remain.find('<') != -1:
			elems = BlockParser.break_last_block(remain, '<>')
			var_type = f'{elems[0]}<{elems[1]}>'
			remain = remain[len(var_type) + 1:]
		else:
			end = remain.find(' ')
			var_type = remain[:end]
			remain = remain[end + 1:]

		var_name = remain[:-1]
		return accessor, annotation, var_type, var_name

	@classmethod
	def build_log_call(cls, calls: str, args: list[str]) -> str:
		"""ログ関数コールを構築

		Args:
			calls: ログ関数のレシーバー
			args: 引数リスト(0: 呼び出し元, 1: 出力テキスト)
		Returns:
			ログ関数コール
		"""
		problems = [Logs.error.__name__, Logs.warning.__name__]

		logs_name = calls[:calls.find('::')]
		tag = calls[len(logs_name) + 2:]
		level = tag if tag in problems else 'info'
		format_text = f'[#{tag}] [{args[0]}]'

		args_ = []
		if tag not in problems:
			args_.append('::'.join([logs_name, Logs.Flags.__name__, tag]))

		if len(args) == 1:
			args_.append(f'"{format_text}:"')
		elif len(args) > 1:
			args_.append(f'"{format_text}: %s"')
			args_.append(f'*FString({args[1]})' if is_quoted_literal(args[1], '"') else f'*{args[1]}')

		return f'log_{level}({", ".join(args_)})'


def ue_meta_parse(setting: RendererSetting) -> Callable[[str], UEMetaHelper]:
	"""@see UEMetaHelper"""
	return lambda meta: UEMetaHelper.parse(meta)


def parse_decl_var(setting: RendererSetting) -> Callable[[str], tuple[str, str, str, str]]:
	"""@see UEViewHelper.parse_decl_var"""
	return lambda decl_var: UEViewHelper.parse_decl_var(decl_var)


def build_log_call(setting: RendererSetting) -> Callable[[str, list[str]], str]:
	"""@see UEViewHelper.build_log_call"""
	return lambda calls, args: UEViewHelper.build_log_call(calls, args)


def filter_decl_var(setting: RendererSetting) -> Callable[[list[str], str], list[str]]:
	"""@see UEViewHelper.filter_decl_var"""
	return lambda strings, subject: UEViewHelper.filter_decl_var(strings, subject)


def renderer_helper_provider() -> RendererHelperProvider:
	"""ヘルパープロバイダー

	Returns:
		ヘルパープロバイダー
	"""
	funcs, filters = factories()
	funcs_cpp, filters_cpp = factories_for_cpp()
	app_funcs = [ue_meta_parse, parse_decl_var, build_log_call]
	app_filters = [filter_decl_var]
	return lambda: ([*funcs, *funcs_cpp, *app_funcs], [*filters, *filters_cpp, *app_filters])
