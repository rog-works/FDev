from typing import cast

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed


@Embed.alias('CoreError')
class CompatibleError(Exception):
	"""互換用の基底クラス"""

	@Embed.alias('message')
	def __str__(self) -> str:
		"""Returns: エラーメッセージ"""
		return super().__str__()


class Errors:
	# region 基底

	class Base(CompatibleError):
		"""アプリケーション例外の基底クラス"""

		def __init__(self, *args: object) -> None:
			"""インスタンスを生成

			Args:
				*args: コンテキスト
			Note:
				XXX CVar.__str__によりアドレスになってしまうため、CVarをアンパック
			"""
			super().__init__(*[cast(CP, arg).raw if isinstance(arg, CP) else arg for arg in iter(args)])

	class Never(Base): """未到達。設計ミス"""
	class Fatal(Base): """致命的。原因不明のエラー"""
	class Logic(Base): """実装不備。ランタイムエラー"""

	# endregion
	# region 未到達

	class Unsupported(Never): """未到達 - 非サポート"""
	class MustBeImplemented(Never): """未到達 - 未実装"""
	class IllegalSchema(Never): """未到達 - 不正なスキーマ・書式"""

	# endregion
	# region 致命的

	class AccessViolation(Fatal): """致命的 - アクセス違反"""

	# endregion
	# region 実装不備

	class NotFound(Logic): """実装不備 - 外部リソース(アセット/ファイル)が存在しない"""
	class Conflict(Logic): """実装不備 - 競合・重複処理"""
	class InvalidArguments(Logic): """実装不備 - 引数の指定ミス。外因によるエラー"""
	class IncompatibleConvertion(Logic): """実装不備 - 互換性のない変換・代入"""
	class NotAllowed(Logic): """実装不備 - 許可されない操作。内因によるエラー"""
	class UnexpectedResult(Logic): """実装不備 - 想定外の結果"""
	class OutOfBounds(Logic): """実装不備 - 範囲外や存在しないインデックス・キーを指定"""

	# endregion
