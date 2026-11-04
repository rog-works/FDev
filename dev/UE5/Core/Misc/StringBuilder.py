from tranp.app.compatible.python.embed import Embed


@Embed.alias('TStringBuilder<256>')
class StringBuilder:
	"""ストリングビルダー Note: XXX 初期サイズは256固定とする"""

	__elems: list[str]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.__elems = []

	def Append(self, string: str) -> 'StringBuilder':
		"""要素を追加 Args: string: 要素"""
		self.__elems.append(string)
		return self

	def AppendChar(self, string: str) -> 'StringBuilder':
		"""要素を追加 Args: string: 要素 Note: XXX char型やstrの1文字参照の場合はこちらを使用"""
		self.__elems.append(string)
		return self

	def ToString(self) -> str:
		"""Returns: 文字列 Note: XXX 実際はTCHAR*を返却。FStringではない点に注意"""
		return ''.join(self.__elems)
