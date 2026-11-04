from typing import Annotated

from tranp.app.compatible.cpp.classes import int64
from tranp.app.compatible.cpp.cvar import CP, CSP
from tranp.app.compatible.python.embed import Embed

from FDev.Main.Const.ProjectConst import Aliases
from FDev.Main.Core.Lang.Json.JsonParser import JsonEntryTypes, JsonParseInfo
from FDev.Main.Core.Lang.String import String


@Embed.alias(Aliases.General.value, prefix=True)
class JsonEntry:
	"""JSONエントリー"""

	entry_type: JsonEntryTypes
	is_root: bool
	read_only: bool
	as_bool: bool
	as_int: int
	as_float: float
	as_string: str
	keys: list[str]
	entries: 'list[CSP[JsonEntry]]'

	def __init__(self, is_root: bool = False, read_only: bool = False) -> None:
		"""インスタンスを生成

		Args:
			is_root: True = ルート要素 (default = False)
			read_only: True = 読み取り専用 (default = False)
		"""
		self.entry_type = JsonEntryTypes.Boolean
		self.is_root = is_root
		self.read_only = read_only
		self.as_bool = False
		self.as_int = 0
		self.as_float = 0.0
		self.as_string = ''
		self.keys = []
		self.entries = []

	@Embed.python
	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		if self.entry_type == JsonEntryTypes.Boolean:
			return f'<JsonEntry[bool]: {self.as_bool} @ {CP(self)}>'
		elif self.entry_type == JsonEntryTypes.Integer:
			return f'<JsonEntry[int]: {self.as_int} @ {CP(self)}>'
		elif self.entry_type == JsonEntryTypes.Float:
			return f'<JsonEntry[float]: {self.as_float} @ {CP(self)}>'
		elif self.entry_type == JsonEntryTypes.String:
			return f'<JsonEntry[str]: "{self.as_string}" @ {CP(self)}>'
		elif self.entry_type == JsonEntryTypes.Array:
			return f'<JsonEntry[list]: [{self.length}] @ {CP(self)}>'
		else:
			return f'<JsonEntry[Object]: [{self.length}] @ {CP(self)}>'

	# region ファクトリー

	@classmethod
	def new_entry(cls, entry_type: JsonEntryTypes, is_root: bool, read_only: bool) -> 'CSP[JsonEntry]':
		"""インスタンスを生成

		Args:
			entry_type: JSONエントリー種別
			is_root: True = ルート要素
			read_only: True = 読み取り専用
		Returns:
			インスタンス
		"""
		instance = CSP.new(cls(is_root, read_only))
		instance.on.entry_type = entry_type
		return instance

	@classmethod
	def new_empty(cls) -> 'CSP[JsonEntry]':
		"""Returns: インスタンス(空) Note: 外部からはJson.EmptyEntryを使用"""
		return cls.new_entry(JsonEntryTypes.Object, is_root=True, read_only=True)

	# endregion
	# region スキーマ

	@property
	@Embed.pure
	def length(self) -> int:
		"""Returns: 配下要素の数 Note: Array/Object専用"""
		return len(self.entries)

	# endregion
	# region セッター

	def set_bool(self, value: bool) -> None:
		"""Args: value: 値"""
		self.clear()
		self.entry_type = JsonEntryTypes.Boolean
		self.as_bool = value

	def set_int(self, value: int) -> None:
		"""Args: value: 値"""
		self.clear()
		self.entry_type = JsonEntryTypes.Integer
		self.as_int = value

	def set_float(self, value: float) -> None:
		"""Args: value: 値"""
		self.clear()
		self.entry_type = JsonEntryTypes.Float
		self.as_float = value

	def set_string(self, value: str) -> None:
		"""Args: value: 値"""
		self.clear()
		self.entry_type = JsonEntryTypes.String
		self.as_string = value

	# endregion
	# region 要素追加・削除

	def append(self, entry: 'CSP[JsonEntry]') -> None:
		"""エントリーを追加(Array専用)

		Args:
			entry: インスタンス
		"""
		entry.on.is_root = False
		self.entries.append(entry)

	def join(self, key: str, entry: 'CSP[JsonEntry]') -> None:
		"""エントリーを追加(Object専用)

		Args:
			key: エントリー名
			entry: インスタンス
		"""
		entry.on.is_root = False
		self.keys.append(key)
		self.entries.append(entry)

	def remove_at(self, index: int) -> None:
		"""エントリーを削除(Array専用)

		Args:
			index: インデックス
		"""
		del self.entries[index]

	def remove_of(self, key: str) -> None:
		"""エントリーを削除(Object専用)

		Args:
			key: エントリー名
		"""
		index = self.keys.index(key)
		del self.keys[index]
		del self.entries[index]

	def clear(self) -> None:
		"""エントリーを初期化"""
		self.as_bool = False
		self.as_int = 0
		self.as_float = 0.0
		self.as_string = ''
		self.keys.clear()
		self.entries.clear()

	# endregion
	# region 構築・複製

	def freeze(self, on: bool = True) -> None:
		"""読み取り設定を変更(ルート要素専用)

		Args:
			on: True = 読み取り専用 (default = True)
		"""
		self.read_only = on
		for entry in self.entries:
			entry.on.freeze(on)

	def isolate(self, read_only: bool) -> 'CSP[JsonEntry]':
		"""自身を基点に複製

		Args:
			read_only: True = 読み取り専用
		Returns:
			インスタンス
		"""
		returned = JsonEntry.new_entry(self.entry_type, is_root=True, read_only=read_only)
		returned.on.copy_value(CP(self))
		return returned

	def build_entry(self, json_str: str, info: Annotated[JsonParseInfo, Embed.immutable], index: int) -> int:
		"""解析情報を基にインスタンスを構築

		Args:
			json_str: JSON文字列
			info: JSON解析情報 @immutable
			index: 処理インデックス
		Returns:
			進行ステップ数
		"""
		entry_type = info.entries[index].entry_type
		begin = info.entries[index].begin
		end = info.entries[index].end
		if entry_type == JsonEntryTypes.Boolean:
			self.set_bool(json_str[begin:end] == 'true')
			return 1
		elif entry_type == JsonEntryTypes.Integer:
			# XXX マスターデータのカラーコード用に32bit最上位バイトの対応
			self.set_int(int(int64(json_str[begin:end])))
			return 1
		elif entry_type == JsonEntryTypes.Float:
			self.set_float(float(json_str[begin:end]))
			return 1
		elif entry_type == JsonEntryTypes.String:
			self.set_string(String.unescape(json_str[begin + 1:end - 1]))
			return 1

		step = 1
		depth = info.entries[index].depth
		while index + step < len(info.entries):
			in_index = index + step
			if depth + 1 != info.entries[in_index].depth:
				break

			in_entry = JsonEntry.new_entry(info.entries[in_index].entry_type, is_root=False, read_only=True)
			in_step = in_entry.on.build_entry(json_str, info, in_index)
			if self.entry_type == JsonEntryTypes.Array:
				self.append(in_entry)
			else:
				self.join(info.entries[in_index].key, in_entry)

			step += in_step

		return step

	def copy_value(self, from_entry: 'CP[JsonEntry]') -> None:
		"""複製元の値をディープコピー。read_onlyは自身の設定を伝搬

		Args:
			from_entry: 複製元
		"""
		if self.entry_type != from_entry.on.entry_type:
			self.clear()

		if from_entry.on.entry_type == JsonEntryTypes.Boolean:
			self.set_bool(from_entry.on.as_bool)
		elif from_entry.on.entry_type == JsonEntryTypes.Integer:
			self.set_int(from_entry.on.as_int)
		elif from_entry.on.entry_type == JsonEntryTypes.Float:
			self.set_float(from_entry.on.as_float)
		elif from_entry.on.entry_type == JsonEntryTypes.String:
			self.set_string(from_entry.on.as_string)
		elif from_entry.on.entry_type == JsonEntryTypes.Array:
			self.entry_type = JsonEntryTypes.Array
			self.__resize_array(from_entry)
			for index in range(from_entry.on.length):
				self.entries[index].on.copy_value(from_entry.on.entries[index].addr)
		else:
			self.entry_type = JsonEntryTypes.Object
			self.__resize_object(from_entry)
			for index in range(from_entry.on.length):
				self.entries[index].on.copy_value(from_entry.on.entries[index].addr)

	def __resize_array(self, from_entry: 'CP[JsonEntry]') -> None:
		"""複製元に合わせてリサイズ(Array)

		Args:
			from_entry: 複製元
		"""
		curr_size = self.length
		next_size = from_entry.on.length
		if curr_size < next_size:
			for i in range(next_size - curr_size):
				index = curr_size + i
				add_entry = JsonEntry.new_entry(from_entry.on.entries[index].on.entry_type, is_root=False, read_only=self.read_only)
				self.append(add_entry)
		elif curr_size > next_size:
			for i in range(curr_size - next_size):
				del self.entries[next_size]

	def __resize_object(self, from_entry: 'CP[JsonEntry]') -> None:
		"""複製元に合わせてリサイズ(Object)

		Args:
			from_entry: 複製元
		"""
		curr_size = self.length
		next_size = from_entry.on.length
		if curr_size < next_size:
			for i in range(next_size - curr_size):
				index = curr_size + i
				add_entry = JsonEntry.new_entry(from_entry.on.entries[index].on.entry_type, is_root=False, read_only=self.read_only)
				self.join(from_entry.on.keys[index], add_entry)
		elif curr_size > next_size:
			for i in range(curr_size - next_size):
				del self.entries[next_size]
				del self.keys[next_size]

	# endregion
