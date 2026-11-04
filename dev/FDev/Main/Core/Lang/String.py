from typing import ClassVar

from tranp.app.compatible.cpp.classes import char, wchar_t
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.StringBuilder import StringBuilder

from FDev.Main.Const.ProjectConst import Aliases


@Embed.alias(Aliases.General.value, prefix=True)
class String:
	"""文字列操作ユーティリティー"""

	_Zero: ClassVar = char('0')
	_Nine: ClassVar = char('9')
	_a: ClassVar = char('a')
	_z: ClassVar = char('z')
	_A: ClassVar = char('A')
	_Z: ClassVar = char('Z')
	_Underscore: ClassVar = char('_')
	_Minus: ClassVar = char('-')
	_Dot: ClassVar = char('.')
	_Backslash: ClassVar = char('\\')

	@classmethod
	def count(cls, string: str, subject: str) -> int:
		"""指定の文字列が含まれる数を計測

		Args:
			string: 文字列
			subject: カウント対象の文字列 ※UEの仕様上char型にするメリットが低いためstr型とする
		Returns:
			含まれる数
		Note:
			@see str.count
		"""
		index = 0
		count = 0
		string_size = len(string)
		subject_size = len(subject)
		while index <= (string_size - subject_size):
			found = string.find(subject, index)
			if found == -1:
				break

			index = found + subject_size
			count += 1

		return count

	@classmethod
	def ltrim(cls, string: str, chara: char) -> str:
		"""トリム(左)

		Args:
			string: 文字列
			chara: 対象の文字
		Returns:
			トリム後の文字列
		"""
		found = -1
		for i in range(len(string)):
			if string[i] != chara:
				break

			found = i + 1

		if found == len(string):
			return ''

		return string[found:] if found != -1 else string

	@classmethod
	def rtrim(cls, string: str, chara: char) -> str:
		"""トリム(右)

		Args:
			string: 文字列
			chara: 対象の文字
		Returns:
			トリム後の文字列
		"""
		found = -1
		for i in range(len(string)):
			index = len(string) - 1 - i
			if string[index] != chara:
				break

			found = index

		if found == 0:
			return ''

		return string[:found] if found != -1 else string

	@classmethod
	def trim(cls, string: str, chara: char) -> str:
		"""トリム

		Args:
			string: 文字列
			chara: 対象の文字
		Returns:
			トリム後の文字列
		"""
		return cls.rtrim(cls.ltrim(string, chara), chara)

	@classmethod
	def is_number(cls, string: str, begin: int = -1, end: int = -1) -> bool:
		"""文字列が数字か判定

		Args:
			string: 文字列
			begin: 開始インデックス (default = -1)
			end: 終了インデックス (default = -1)
		Returns:
			True = 数字
		"""
		length = len(string)
		_begin = min(length, max(0, begin))
		_end = min(length, max(_begin, end if end != -1 else length))
		for index in range(_begin, _end):
			if index == _begin and string[index] == cls._Minus:
				continue
			elif string[index] >= cls._Zero and string[index] <= cls._Nine:
				continue
			elif string[index] == cls._Dot:
				continue
			else:
				return False

		return True

	@classmethod
	def is_name(cls, string: str, begin: int = -1, end: int = -1) -> bool:
		"""文字列が名前か判定

		Args:
			string: 文字列
			begin: 開始インデックス (default = -1)
			end: 終了インデックス (default = -1)
		Returns:
			True = 名前
		"""
		length = len(string)
		_begin = min(length, max(0, begin))
		_end = min(length, max(_begin, end if end != -1 else length))
		for index in range(_begin, _end):
			if (index > _begin and string[index] >= cls._Zero and string[index] <= cls._Nine):
				continue
			elif (string[index] >= cls._a and string[index] <= cls._z):
				continue
			elif (string[index] >= cls._A and string[index] <= cls._Z):
				continue
			elif (string[index] == cls._Underscore):
				continue
			else:
				return False

		return True

	@classmethod
	def join(cls, strings: list[str], delimiter: str) -> str:
		"""区切り文字で文字列のリストを結合

		Args:
			strings: 文字列リスト
			delimiter: 区切り文字
		Returns:
			結合後の文字列
		Note:
			@see str.join
		"""
		if len(strings) == 0:
			return ''

		builder = StringBuilder()
		for i in range(len(strings)):
			if i > 0:
				builder.Append(delimiter)
				builder.Append(strings[i])
			else:
				builder.Append(strings[i])

		return builder.ToString()

	@classmethod
	def split(cls, string: str, delimiter: str) -> list[str]:
		"""区切り文字で文字列を分割する

		Args:
			string: 文字列
			delimiter: 区切り文字
		Returns:
			分割した文字列
		Note:
			@see str.split
		"""
		parts: list[str] = []
		pos0 = 0
		while pos0 < len(string):
			pos1 = string.find(delimiter, pos0)
			if pos1 == -1:
				pos1 = len(string)

			parts.append(string[pos0:pos1])
			pos0 = pos1 + len(delimiter)

		# 対象の文字列が空文字、または末尾が区切り文字の場合は空文字を要素に追加する
		if len(string) == 0 or string.endswith(delimiter):
			parts.append('')

		return parts

	@classmethod
	def escape(cls, string: str, chara: char) -> str:
		"""文字列内の任意の文字に対してエスケープを施す

		Args:
			string: 対象
			chara: エスケープ対象の文字
		Returns:
			エスケープ後の文字列
		"""
		target = str('') + chara
		if string.count(target) == 0 and string.count('\\') == 0:
			return string

		builder = StringBuilder()
		begin = 0
		end = begin
		while end < len(string):
			if string[end] == chara or string[end] == cls._Backslash:
				builder.Append(string[begin:end])
				builder.AppendChar(cls._Backslash)
				builder.AppendChar(string[end])
				begin = end + 1

			end += 1

		if begin < end:
			builder.Append(string[begin:end])

		return builder.ToString()

	@classmethod
	def unescape(cls, string: str) -> str:
		"""文字列内のエスケープを解除する

		Args:
			string: 対象
		Returns:
			エスケープ解除後の文字列
		"""
		if string.count('\\') == 0:
			return string

		builder = StringBuilder()
		begin = 0
		escape = '\\'
		while begin < len(string):
			end = string.find(escape, begin)
			if end == -1:
				builder.Append(string[begin:])
				break

			builder.Append(string[begin:end])
			builder.AppendChar(string[end + 1])
			begin = end + 2

		return builder.ToString()

	@classmethod
	def from_code(cls, code: int) -> str:
		"""文字コードから文字に変換

		Args:
			code: 文字コード(Unicode)
		Returns:
			文字
		Note:
			FStringにUnicodeの私用領域(0xFxxx)を直接渡すと文字化けするためTCHARを中継して変換
		"""
		return str('') + wchar_t(code)

	@classmethod
	@Embed.python
	def find_strict(cls, string: str, subject: str, begin: int = 0, end: int = 0) -> int:
		"""指定の文字列を検索し、開始インデックスを返却

		Args:
			string: 文字列
			subject: 検索対象
			begin: 開始インデックス (default = 0)
			end: 終了インデックス (default = 0)
		Returns:
			開始インデックス
		Note:
			```
			* CaseSensitive版。通常の用途ではstr.findの使用を推奨
			* 開始/終了インデックスの負の値には対応しない
			* 引数のstring/subjectは、どちらもstr型が必須。リテラルの指定は禁止
			* 翻訳によって置き換え
			@see data/template/func_call/default.j2
			```
		"""
		if begin < end and end > 0:
			return string.find(subject, begin, end)
		else:
			return string.find(subject, begin)

	@classmethod
	def startswith_strict(cls, string: str, prefix: str, begin: int = 0, end: int = 0) -> bool:
		"""指定の文字列との前方一致

		Args:
			string: 文字列
			suffix: 接尾辞
			begin: 開始インデックス (default = 0)
			end: 終了インデックス (default = 0)
		Returns:
			True = 一致
		Note:
			```
			* CaseSensitive版。通常の用途ではstr.startswithの使用を推奨
			* 開始/終了インデックスの負の値には対応しない
			@see str.endswith
			```
		"""
		if begin < end and end > 0:
			return cls.find_strict(string, prefix, begin, end) == begin
		elif begin > 0 and end == 0:
			return cls.find_strict(string, prefix, begin) == begin
		else:
			return cls.find_strict(string, prefix, 0) == 0

	@classmethod
	def endswith_strict(cls, string: str, suffix: str, begin: int = 0, end: int = 0) -> bool:
		"""指定の文字列との後方一致

		Args:
			string: 文字列
			suffix: 接尾辞
			begin: 開始インデックス (default = 0)
			end: 終了インデックス (default = 0)
		Returns:
			True = 一致
		Note:
			```
			* CaseSensitive版。通常の用途ではstr.endswithの使用を推奨
			* 開始/終了インデックスの負の値には対応しない
			@see str.endswith
			```
		"""
		if begin < end and end > 0:
			expect_at = max(begin, end - len(suffix))
			return cls.find_strict(string, suffix, expect_at, end) == expect_at
		elif begin > 0 and end == 0:
			expect_at = max(begin, len(string) - len(suffix))
			return cls.find_strict(string, suffix, expect_at) == expect_at
		else:
			expect_at = max(0, len(string) - len(suffix))
			return cls.find_strict(string, suffix, expect_at) == expect_at

	@classmethod
	def count_strict(cls, string: str, subject: str, begin: int = 0, end: int = 0) -> int:
		"""指定の文字列が含まれる数を計測

		Args:
			string: 文字列
			subject: カウント対象の文字列
			begin: 開始インデックス (default = 0)
			end: 終了インデックス (default = 0)
		Returns:
			含まれる数
		Note:
			```
			* CaseSensitive版。通常の用途ではstr.countの使用を推奨
			* 開始/終了インデックスの負の値には対応しない
			@see count
			```
		"""
		index = begin
		count = 0
		string_size = len(string) if end == 0 else end
		subject_size = len(subject)
		while index <= (string_size - subject_size):
			found = cls.find_strict(string, subject, index, string_size)
			if found == -1:
				break

			index = found + subject_size
			count += 1

		return count

	@classmethod
	@Embed.python
	def replace_strict(cls, string: str, subject: str, replaced: str) -> str:
		"""文字列を置換

		Args:
			string: 文字列
			subject: 検索対象
			replaced: 置換内容
		Returns:
			置換後の文字列
		Note:
			```
			* CaseSensitive版。通常の用途ではstr.replaceの使用を推奨
			* 引数のstring/subjectは、どちらもstr型が必須。リテラルの指定は禁止
			* 翻訳によって置き換え
			@see data/template/func_call/default.j2
			```
		"""
		return string.replace(subject, replaced)

	@classmethod
	def split_strict(cls, string: str, delimiter: str) -> list[str]:
		"""文字列を置換

		Args:
			string: 文字列
			delimiter: 区切り文字
		Returns:
			文字列リスト
		Note:
			```
			* CaseSensitive版。通常の用途ではstr.splitの使用を推奨
			@see split
			```
		"""
		parts: list[str] = []
		pos0 = 0
		while pos0 < len(string):
			pos1 = cls.find_strict(string, delimiter, pos0)
			if pos1 == -1:
				pos1 = len(string)

			parts.append(string[pos0:pos1])
			pos0 = pos1 + len(delimiter)

		# 対象の文字列が空文字、または末尾が区切り文字の場合は空文字を要素に追加する
		if len(string) == 0 or cls.endswith_strict(string, delimiter):
			parts.append('')

		return parts
