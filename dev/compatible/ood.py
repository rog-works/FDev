from typing import Any, Protocol


class OOD(Protocol):
	"""メソッドの規約・命名規則をまとめるクラス。オブジェクト指向と関係は無く、プロトコルとしての強制力はない"""

	# region ライフサイクル

	def initialize(self, *args: Any) -> None:
		"""インスタンスを初期化

		Args:
			*args: 任意
		"""
		...

	def release(self) -> None:
		"""インスタンスを解放

		Note:
			無効化や解放を目的とする。リトライ性に関しては特に明言しない
		"""
		...

	# endregion
	# region スキーマ

	def ToString(self) -> str:
		"""Returns: 文字列表現

		Note:
			クラスのデバッグ情報を出力。シリアライズ・データ変換にはserializeを使用
		"""
		...

	def length(self) -> int:
		"""Returns: 要素数"""
		...

	# endregion
	# region シリアライズ

	def serialize(self) -> str:
		"""シリアライズ

		Returns:
			JSON文字列
		Note:
			ロジック用途
		"""
		...

	# endregion
