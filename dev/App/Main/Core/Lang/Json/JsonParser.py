from enum import Enum

from tranp.app.compatible.cpp.classes import char
from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed

from App.Main.Const.ProjectConst import ClassPrefixs
from App.Main.Core.Lang.String import String


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class JsonEntryTypes(Enum):
	"""JSONエントリー種別"""
	Boolean = 0
	Integer = 1
	Float = 2
	String = 3
	Array = 4
	Object = 5
	Unknown = 6


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class JsonParseInfo:
	"""Json解析情報"""

	class Entry:
		"""エントリー"""

		entry_type: JsonEntryTypes
		key: str
		depth: int
		begin: int
		end: int

		def __init__(self, entry_type: JsonEntryTypes, key: str, depth: int, begin: int, end: int) -> None:
			"""インスタンスを生成

			Args:
				entry_type: Jsonエントリー種別
				key: キー名
				depth: 深度
				begin: 読み取り開始位置
				end: 読み取り終了位置
			"""
			self.entry_type = entry_type
			self.key = key
			self.depth = depth
			self.begin = begin
			self.end = end

	entries: list[Entry]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.entries = []


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class JsonParser:
	"""JSONパーサー"""

	@classmethod
	def parse(cls, json_str: str, info: CP[JsonParseInfo]) -> None:
		"""JSON文字列を解析

		Args:
			json_str: JSON文字列
			info: JSON解析情報
		"""
		cls._parse_entry(json_str, 0, '', 0, info)

	@classmethod
	def _parse_entry(cls, json_str: str, begin: int, key: str, depth: int, info: CP[JsonParseInfo]) -> int:
		"""JSON文字列を解析(エントリー)

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
			key: キー名
			depth: 深度
			info: JSON解析情報
		Returns:
			読み取り終了位置
		"""
		end = begin
		at_type, begin_value = cls._analyze_type(json_str, begin)
		end = begin_value
		if at_type == JsonEntryTypes.Boolean:
			end = cls._parse_boolean(json_str, begin_value, key, depth, info)
		elif at_type == JsonEntryTypes.Float:
			end = cls._parse_float(json_str, begin_value, key, depth, info)
		elif at_type == JsonEntryTypes.String:
			end = cls._parse_string(json_str, begin_value, key, depth, info)
		elif at_type == JsonEntryTypes.Array:
			end = cls._parse_array(json_str, begin_value, key, depth, info)
		elif at_type == JsonEntryTypes.Object:
			end = cls._parse_object(json_str, begin_value, key, depth, info)

		return end

	@classmethod
	def _parse_boolean(cls, json_str: str, begin: int, key: str, depth: int, info: CP[JsonParseInfo]) -> int:
		"""JSON文字列を解析(エントリー/Boolean)

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
			key: キー名
			depth: 深度
			info: JSON解析情報
		Returns:
			読み取り終了位置
		"""
		if json_str[begin] == char('f'):
			info.on.entries.append(JsonParseInfo.Entry(JsonEntryTypes.Boolean, key, depth, begin, begin + 5))
			return begin + 5
		else:
			info.on.entries.append(JsonParseInfo.Entry(JsonEntryTypes.Boolean, key, depth, begin, begin + 4))
			return begin + 4

	@classmethod
	def _parse_float(cls, json_str: str, begin: int, key: str, depth: int, info: CP[JsonParseInfo]) -> int:
		"""JSON文字列を解析(エントリー/Float)

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
			key: キー名
			depth: 深度
			info: JSON解析情報
		Returns:
			読み取り終了位置
		"""
		entry_type = JsonEntryTypes.Integer
		end = begin
		while end < len(json_str):
			if entry_type == JsonEntryTypes.Integer and json_str[end] == char('.'):
				entry_type = JsonEntryTypes.Float

			end += 1
			if not String.is_number(json_str, begin, end + 1):
				break

		info.on.entries.append(JsonParseInfo.Entry(entry_type, key, depth, begin, end))
		return end

	@classmethod
	def _parse_string(cls, json_str: str, begin: int, key: str, depth: int, info: CP[JsonParseInfo]) -> int:
		"""JSON文字列を解析(エントリー/String)

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
			key: キー名
			depth: 深度
			info: JSON解析情報
		Returns:
			読み取り終了位置
		"""
		quote = '\"'
		end = json_str.find(quote, begin)
		while end < len(json_str):
			found = json_str.find(quote, end + 1)
			if found == -1:
				end = len(json_str)
				break

			end = found
			if json_str[end - 1] != char('\\'):
				break

		info.on.entries.append(JsonParseInfo.Entry(JsonEntryTypes.String, key, depth, begin, end + 1))
		return end + 1

	@classmethod
	def _parse_array(cls, json_str: str, begin: int, key: str, depth: int, info: CP[JsonParseInfo]) -> int:
		"""JSON文字列を解析(エントリー/Array)

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
			key: キー名
			depth: 深度
			info: JSON解析情報
		Returns:
			読み取り終了位置
		"""
		info_begin = len(info.on.entries)
		end = json_str.find('[', begin)
		end += 1
		element_at = 0
		while end < len(json_str):
			entry_type, block_end = cls._analyze_type(json_str, end, ']')
			if entry_type == JsonEntryTypes.Unknown or json_str[end] == char(']'):
				end = max(end, block_end)
				break

			end = cls._parse_entry(json_str, end, str(element_at), depth + 1, info)
			element_at += 1

		info.on.entries.insert(info_begin, JsonParseInfo.Entry(JsonEntryTypes.Array, key, depth, begin, end + 1))
		return end + 1

	@classmethod
	def _parse_object(cls, json_str: str, begin: int, key: str, depth: int, info: CP[JsonParseInfo]) -> int:
		"""JSON文字列を解析(エントリー/Object)

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
			key: キー名
			depth: 深度
			info: JSON解析情報
		Returns:
			読み取り終了位置
		"""
		info_begin = len(info.on.entries)
		end = json_str.find('{', begin)
		end += 1
		while end < len(json_str):
			entry_type, block_end = cls._analyze_type(json_str, end, '}')
			if entry_type != JsonEntryTypes.String or json_str[end] == char('}'):
				end = max(end, block_end)
				break

			in_key, begin_value = cls._parse_key(json_str, end)
			end = cls._parse_entry(json_str, begin_value, in_key, depth + 1, info)

		info.on.entries.insert(info_begin, JsonParseInfo.Entry(JsonEntryTypes.Object, key, depth, begin, end + 1))
		return end + 1

	@classmethod
	def _parse_key(cls, json_str: str, begin: int) -> tuple[str, int]:
		"""JSON文字列を解析(キー)

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
		Returns:
			キー, 読み取り終了位置
		"""
		key_begin = json_str.find('\"', begin)
		end = json_str.find('\"', key_begin + 1)
		key = json_str[key_begin + 1:end]
		return (key, end + 1)

	@classmethod
	def _analyze_type(cls, json_str: str, begin: int, end_token: str = '') -> tuple[JsonEntryTypes, int]:
		"""JSONエントリーの種別を解析

		Args:
			json_str: JSON文字列
			begin: 読み取り開始位置
			end_token: 終端記号 (default = '')
		Returns:
			JSONエントリーの種別, 読み取り終了位置
		"""
		end = begin
		while end < len(json_str):
			if json_str[end] == char('f') or json_str[end] == char('t'):
				return (JsonEntryTypes.Boolean, end)
			elif json_str[end] == char('"'):
				return (JsonEntryTypes.String, end)
			elif json_str[end] == char('['):
				return (JsonEntryTypes.Array, end)
			elif json_str[end] == char('{'):
				return (JsonEntryTypes.Object, end)
			elif String.is_number(json_str, end, end + 1):
				return (JsonEntryTypes.Float, end)
			elif len(end_token) > 0 and json_str[end] == end_token[0]:
				return (JsonEntryTypes.Unknown, end)

			end += 1

		return (JsonEntryTypes.Unknown, -1)
