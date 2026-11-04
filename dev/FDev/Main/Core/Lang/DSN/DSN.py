from typing import ClassVar

from tranp.app.compatible.python.embed import Embed

from FDev.Main.Const.ProjectConst import ClassPrefixs


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class DSN:
	"""DSN(Dot Separator Name)"""

	Delimiter: ClassVar[str] = '.'

	@classmethod
	def is_association(cls, base: str, path: str, delimiter: str = Delimiter) -> bool:
		"""関連があるか判定(要素単位で前方一致、または同じ)

		Args:
			base: パス(基準)
			path: パス(比較対象)
			delimiter: 区切り文字 (default = '.')
		Returns:
			True = 適合
		"""
		if len(base) > len(path):
			return False
		elif len(base) == 0:
			return True
		elif base == path:
			return True

		base_count = cls.count(base, delimiter)
		if base_count > cls.count(path, delimiter):
			return False
		elif not path.startswith(base):
			return False

		base_tail = cls.pick(base, base_count - 1, delimiter)
		path_head = cls.pick(path, base_count - 1, delimiter)
		return base_tail == path_head

	@classmethod
	def is_under(cls, base: str, path: str, delimiter: str = Delimiter) -> bool:
		"""配下要素か判定

		Args:
			base: パス(基準)
			path: パス(比較対象)
			delimiter: 区切り文字 (default = '.')
		Returns:
			True = 適合
		"""
		return cls.count(base, delimiter) + 1 == cls.count(path, delimiter) and cls.is_association(base, path)

	@classmethod
	def count(cls, path: str, delimiter: str = Delimiter) -> int:
		"""要素数を取得

		Args:
			path: パス
			delimiter: 区切り文字 (default = '.')
		Returns:
			要素数
		"""
		return 0 if len(path) == 0 else path.count(delimiter) + 1

	@classmethod
	def elements(cls, path: str, delimiter: str = Delimiter) -> list[str]:
		"""パスから要素リストに分解

		Args:
			path: パス
			delimiter: 区切り文字 (default = '.')
		Returns:
			要素リスト
		"""
		if len(path) == 0:
			return []
		else:
			return path.split(delimiter)

	@classmethod
	def join(cls, elems: list[str], delimiter: str = Delimiter) -> str:
		"""パス/要素を連結してパスを生成

		Args:
			elems: パス/要素リスト
			delimiter: 区切り文字 (default = '.')
		Returns:
			連結したパス
		"""
		return delimiter.join(elems)

	@classmethod
	def joined(cls, a: str, b: str, delimiter: str = Delimiter) -> str:
		"""パスを連結

		Args:
			a: パスA
			b: パスB
			delimiter: 区切り文字 (default = '.')
		Returns:
			連結したパス
		"""
		if len(a) == 0:
			return b
		elif len(b) == 0:
			return a
		else:
			return a + delimiter + b

	@classmethod
	def pick(cls, path: str, index: int, delimiter: str = Delimiter) -> str:
		"""指定位置の要素を取得

		Args:
			path: パス
			index: インデックス
			delimiter: 区切り文字 (default = '.')
		Returns:
			要素
		"""
		if len(path) == 0:
			return ''

		begin = 0
		for i in range(index + 1):
			end = path.find(delimiter, begin)
			if i == index and end == -1:
				return path[begin:]
			elif end == -1:
				return ''
			elif i == index:
				return path[begin:end]

			begin = end + 1

		return ''

	@classmethod
	def first(cls, path: str, delimiter: str = Delimiter) -> str:
		"""先頭の要素を取得

		Args:
			path: パス
			delimiter: 区切り文字 (default = '.')
		Returns:
			要素
		"""
		return cls.pick(path, 0, delimiter)

	@classmethod
	def last(cls, path: str, delimiter: str = Delimiter) -> str:
		"""末尾の要素を取得

		Args:
			path: パス
			delimiter: 区切り文字 (default = '.')
		Returns:
			要素
		"""
		if len(path) == 0 or path.count(delimiter) == 0:
			return path

		begin = path.rfind(delimiter) + 1
		return path[begin:]

	@classmethod
	def pad_left(cls, path: str, count: int, delimiter: str = Delimiter) -> str:
		"""パスを左から詰める(先頭 -> 末尾)

		Args:
			path: パス
			count: 要素数
			delimiter: 区切り文字 (default = '.')
		Returns:
			パス
		"""
		if path.count(delimiter) < count:
			return ''

		begin = 0
		for _ in range(count):
			begin = path.find(delimiter, begin) + 1

		return path[begin:]

	@classmethod
	def pad_right(cls, path: str, count: int, delimiter: str = Delimiter) -> str:
		"""パスを右から詰める(末尾 -> 先頭)

		Args:
			path: パス
			count: 要素数
			delimiter: 区切り文字 (default = '.')
		Returns:
			パス
		"""
		if path.count(delimiter) < count:
			return ''

		end = len(path) - 1
		for _ in range(count):
			end = path.rfind(delimiter, 0, end) - 1

		return path[:end + 1]

	@classmethod
	def padding(cls, path: str, shift: int, delimiter: str = Delimiter) -> str:
		"""パスを指定方向から詰める(+: 左, -: 右)

		Args:
			path: パス
			shift: シフト数
			delimiter: 区切り文字 (default = '.')
		Returns:
			パス
		"""
		if shift > 0:
			return cls.pad_left(path, shift, delimiter)
		elif shift < 0:
			return cls.pad_right(path, -shift, delimiter)
		else:
			return path
