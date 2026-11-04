# @see Engine/Source/Runtime/Core/Public/UObject/NameTypes.h

from tranp.app.compatible.python.embed import Embed


@Embed.alias('F', prefix=True)
class Name:
	"""名前

	Note:
		```
		### C++
		* FStringとの違いは高速比較と省メモリである点
		* 文字列の実体はNameテーブルが管理し、各インスタンスは参照インデックスのみを保持
		### Python
		* 文字列リテラルからの暗黙変換は可能だが、FStringからは出来ない点に注意
		* C++の暗黙変換を利用して、UE側のモジュールでは仮引数のUnion型(`Name | str`)は許容する
		```
	"""

	_name: str

	def __init__(self, name: str = '') -> None:
		"""インスタンスを生成

		Args:
			name: 名前
		"""
		self._name = name

	def __eq__(self, other: 'Name | str') -> bool:
		"""Args: other: 対象 Returns: True = 同じ"""
		if isinstance(other, Name):
			return self._name == other._name
		else:
			return self._name == other

	def __str__(self) -> str:
		"""Returns: 文字列表現"""
		return self._name

	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		return f'<{self.__class__.__name__}: "{self._name}">'

	def __hash__(self) -> int:
		"""Returns: ハッシュ値"""
		return hash(self._name)

	def GetStringLength(self) -> int:
		"""Returns: 文字数"""
		return len(self._name)

	def ToString(self) -> str:
		"""Returns: 文字列表現"""
		return self._name


@Embed.alias('F', prefix=True)
class Text:
	"""テキスト Note: @see Engine/Source/Runtime/Core/Public/Internationalization/Text.h"""

	_text: str

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self._text = ''

	@classmethod
	def FromString(cls, text: str) -> 'Text':
		"""インスタンスを生成

		Args:
			text: テキスト
		Returns:
			インスタンス
		"""
		instance = cls()
		instance._text = text
		return instance

	def IsEmpty(self) -> bool:
		"""Returns: True = 空文字"""
		return len(self._text) == 0

	def ToString(self) -> str:
		"""Returns: 文字列表現"""
		return self._text
