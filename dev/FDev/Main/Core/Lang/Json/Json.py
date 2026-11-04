from typing import Annotated, ClassVar, cast

from tranp.app.compatible.cpp.classes import char, uint64, void
from tranp.app.compatible.cpp.cvar import CP, CSP
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.StringBuilder import StringBuilder
from UE5.CoreUObject.UObject.Object import GenStruct
from UE5.CoreUObject.UObject.ObjectMacros import USTRUCT

from compatible.cvar import unpack_shared
from compatible.error import Errors
from FDev.Main.Const.ProjectConst import Aliases
from FDev.Main.Core.Lang.DSN.DSN import DSN
from FDev.Main.Core.Lang.Json.JsonEntry import JsonEntry
from FDev.Main.Core.Lang.Json.JsonParser import JsonEntryTypes, JsonParseInfo, JsonParser
from FDev.Main.Core.Lang.String import String


@Embed.struct
@Embed.alias(Aliases.Struct.value, prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class Json(GenStruct):
	"""JSON

	Note:
		```
		### 留意事項
		* 文字列は2重引用符以外のエスケープを行わない (外部入力の文字列を扱うのは基本的にNG)
		* 数値は10進数のみ扱う
		* 配列の要素挿入は出来ず、追加のみ対応
		* オブジェクトのみキーリストを管理
		### メンバー変数としての公開は禁止
		* 理由: 初期状態が不確定になり、安全性を担保出来なくなるため @see UE5.CoreUObject.UObject.Object.UObject.post_init_properties
		* Jsonのコピーは非常に軽量なため、過剰な回避策を実装するより、関数を通して共有する方が遥かに安価で安全
		```
	"""

	EmptyEntry: ClassVar = JsonEntry.new_empty()

	cursor: CP[JsonEntry]

	def __init__(self, entry: CP[JsonEntry] | None = None) -> None:
		"""インスタンスを生成

		Args:
			entry: JSONエントリー | None (default = None)
		"""
		self.cursor: CP[JsonEntry] = entry if entry else Json.EmptyEntry.addr

	@Embed.python
	def __repr__(self) -> str:
		"""Returns: シリアライズ表現"""
		if self.is_scalar:
			return f'<{Json.__name__}[{self.type_name}]: {self.serialize()}{" read_only" if self.cursor.on.read_only else ""} @ {self.cursor}>'
		else:
			return f'<{Json.__name__}[{self.type_name}]: [{self.length}]{" read_only" if self.cursor.on.read_only else ""} @ {self.cursor}>'

	@Embed.pure
	def ToString(self) -> str:
		"""Returns: 文字列表現"""
		if self.is_scalar:
			return '<Json[{type_name}]: {value}{readonly} @ {addr}>'.format(type_name=self.type_name, value=self.serialize(), readonly=str(' readonly' if self.cursor.on.read_only else ''), addr=self.cursor)
		else:
			return '<Json[{type_name}]: [{num}]{readonly} @ {addr}>'.format(type_name=self.type_name, num=self.length, readonly=str(' readonly' if self.cursor.on.read_only else ''), addr=self.cursor)

	# region ファクトリー

	@classmethod
	def parse(cls, json_str: str) -> CSP[JsonEntry]:
		"""JSON文字列を基にインスタンスを生成(読み取り専用)

		Args:
			json_str: JSON文字列
		Returns:
			JSONエントリー
		"""
		info  = JsonParseInfo()
		JsonParser.parse(json_str, CP(info))
		returned = JsonEntry.new_entry(info.entries[0].entry_type, is_root=True, read_only=True)
		returned.on.build_entry(json_str, info, 0)
		return returned

	@classmethod
	def new_bool(cls, value: bool, read_only: bool = False) -> CSP[JsonEntry]:
		"""Args: value: 値, read_only: True = 読み取り専用 (default = False) Returns: JSONエントリー"""
		returned = JsonEntry.new_entry(JsonEntryTypes.Boolean, is_root=True, read_only=read_only)
		returned.on.set_bool(value)
		return returned

	@classmethod
	def new_int(cls, value: int, read_only: bool = False) -> CSP[JsonEntry]:
		"""Args: value: 値, read_only: True = 読み取り専用 (default = False) Returns: JSONエントリー"""
		returned = JsonEntry.new_entry(JsonEntryTypes.Integer, is_root=True, read_only=read_only)
		returned.on.set_int(value)
		return returned

	@classmethod
	def new_float(cls, value: float, read_only: bool = False) -> CSP[JsonEntry]:
		"""Args: value: 値, read_only: True = 読み取り専用 (default = False) Returns: JSONエントリー"""
		returned = JsonEntry.new_entry(JsonEntryTypes.Float, is_root=True, read_only=read_only)
		returned.on.set_float(value)
		return returned

	@classmethod
	def new_string(cls, value: str, read_only: bool = False) -> CSP[JsonEntry]:
		"""Args: value: 値, read_only: True = 読み取り専用 (default = False) Returns: JSONエントリー"""
		returned = JsonEntry.new_entry(JsonEntryTypes.String, is_root=True, read_only=read_only)
		# XXX unescapeした文字列を保持するのが正なのでescapeはしないこと
		returned.on.set_string(value)
		return returned

	@classmethod
	def new_array(cls) -> CSP[JsonEntry]:
		"""Args: value: 値 Returns: JSONエントリー"""
		return JsonEntry.new_entry(JsonEntryTypes.Array, is_root=True, read_only=False)

	@classmethod
	def new_object(cls) -> CSP[JsonEntry]:
		"""Args: value: 値 Returns: JSONエントリー"""
		return JsonEntry.new_entry(JsonEntryTypes.Object, is_root=True, read_only=False)

	# endregion
	# region スキーマ

	@property
	@Embed.pure
	def is_empty(self) -> bool:
		"""Returns: True = 空データ"""
		return self.cursor == Json.EmptyEntry.addr

	@property
	@Embed.pure
	def is_root(self) -> bool:
		"""Returns: True = ルートオブジェクト"""
		return self.cursor.on.is_root

	@property
	@Embed.pure
	def read_only(self) -> bool:
		"""Returns: True = 読み取り専用"""
		return self.cursor.on.read_only

	@property
	@Embed.pure
	def entry_type(self) -> JsonEntryTypes:
		"""Returns: JSONエントリー種別"""
		return self.cursor.on.entry_type

	@property
	@Embed.pure
	def iterable(self) -> bool:
		"""Returns: True = Array/Object"""
		return self.cursor.on.entry_type == JsonEntryTypes.Array or self.cursor.on.entry_type == JsonEntryTypes.Object

	@property
	@Embed.pure
	def is_scalar(self) -> bool:
		"""Returns: True = スカラー型"""
		return not self.iterable

	@property
	@Embed.pure
	def is_bool(self) -> bool:
		"""Returns: True = Boolean"""
		return self.cursor.on.entry_type == JsonEntryTypes.Boolean

	@property
	@Embed.pure
	def is_int(self) -> bool:
		"""Returns: True = Integer"""
		return self.cursor.on.entry_type == JsonEntryTypes.Integer

	@property
	@Embed.pure
	def is_float(self) -> bool:
		"""Returns: True = Float"""
		return self.cursor.on.entry_type == JsonEntryTypes.Float

	@property
	@Embed.pure
	def is_string(self) -> bool:
		"""Returns: True = String"""
		return self.cursor.on.entry_type == JsonEntryTypes.String

	@property
	@Embed.pure
	def is_array(self) -> bool:
		"""Returns: True = Array"""
		return self.cursor.on.entry_type == JsonEntryTypes.Array

	@property
	@Embed.pure
	def is_object(self) -> bool:
		"""Returns: True = Object"""
		return self.cursor.on.entry_type == JsonEntryTypes.Object

	@property
	@Embed.pure
	def type_name(self) -> Annotated[str, Embed.immutable]:
		"""Returns: 型の名前 @immutable @test"""
		to_type_names = Embed.static(Json.type_name).decl(lambda: {
			JsonEntryTypes.Boolean: bool.__name__,
			JsonEntryTypes.Integer: int.__name__,
			JsonEntryTypes.Float: float.__name__,
			JsonEntryTypes.String: str.__name__,
			JsonEntryTypes.Array: list.__name__,
			JsonEntryTypes.Object: Json.__name__,
		})
		return to_type_names[self.cursor.on.entry_type]

	# endregion
	# region 要素参照

	@Embed.pure
	def __getitem__(self, key: str) -> 'Json':
		"""配下要素を取得

		Args:
			key: 要素キー
		Returns:
			インスタンス
		Raises:
			NotAllowed: Array/Object以外で使用
			OutOfBounds: 存在しないエントリーを指定
		"""
		return self.by(key)

	@property
	@Embed.pure
	def length(self) -> int:
		"""Returns: 配下要素の数 Raises: NotAllowed: Array/Object以外で実行"""
		if not self.iterable:
			raise Errors.NotAllowed(Json.length, self)

		return self.cursor.on.length

	@property
	@Embed.pure
	def keys(self) -> Annotated[list[str], Embed.immutable]:
		"""Returns: キーリスト @immutable Raises: NotAllowed: Object以外で使用"""
		if self.cursor.on.entry_type != JsonEntryTypes.Object:
			raise Errors.NotAllowed(Json.keys, self)

		return self.cursor.on.keys

	@property
	def entries(self) -> 'list[Json]':
		"""Returns: 配下要素リスト Raises: NotAllowed: Array/Object以外で使用"""
		if not self.iterable:
			raise Errors.NotAllowed(Json.entries, self)

		return [Json(entry.addr) for entry in self.cursor.on.entries]

	@Embed.pure
	def exists(self, jsonpath: str) -> bool:
		"""指定のJSONパスを持つ要素が存在するか判定

		Args:
			jsonpath: JSONパス
		Returns:
			True = 存在
		"""
		routes = DSN.elements(jsonpath)
		cursor = self.cursor
		for i in range(len(routes)):
			curr = Json(cursor)
			if curr.has_key(routes[i]):
				return False

			cursor = curr.by(routes[i]).cursor

		return True

	@Embed.pure
	def has_key(self, key: str) -> bool:
		"""指定のキーを持つ配下要素が存在するか判定

		Args:
			key: キー
		Returns:
			True = 存在
		Raises:
			NotAllowed: Array/Object以外で使用
		"""
		if self.cursor.on.entry_type == JsonEntryTypes.Array:
			return String.is_number(key) and int(key) >= 0 and int(key) < self.length
		elif self.cursor.on.entry_type == JsonEntryTypes.Object:
			return key in self.cursor.on.keys
		else:
			raise Errors.NotAllowed(Json.has_key, self)
	
	@Embed.pure
	def key_at(self, index: int) -> str:
		"""指定位置のキーを取得

		Args:
			index: インデックス
		Returns:
			キー
		Raises:
			NotAllowed: Array/Object以外で使用
			OutOfBounds: 存在しないエントリーを指定
		"""
		if self.cursor.on.entry_type == JsonEntryTypes.Array:
			return str(index)
		elif self.cursor.on.entry_type == JsonEntryTypes.Object:
			return self.cursor.on.keys[index]
		else:
			raise Errors.NotAllowed(Json.key_at, self)

	@Embed.pure
	def at(self, index: int) -> 'Json':
		"""配下要素を取得

		Args:
			index: インデックス
		Returns:
			インスタンス
		Raises:
			NotAllowed: Array/Object以外で使用
			OutOfBounds: 存在しないエントリーを指定
		"""
		if not self.iterable:
			raise Errors.NotAllowed(Json.at, self)

		return Json(self.cursor.on.entries[index].addr)

	@Embed.pure
	def by(self, key: str) -> 'Json':
		"""配下要素を取得

		Args:
			key: シンボル名
		Returns:
			インスタンス
		Raises:
			NotAllowed: Array/Object以外で使用
			OutOfBounds: 存在しないエントリーを指定
		"""
		if self.cursor.on.entry_type == JsonEntryTypes.Array:
			return Json(self.cursor.on.entries[int(key)].addr)
		elif self.cursor.on.entry_type == JsonEntryTypes.Object:
			index = self.cursor.on.keys.index(key)
			return Json(self.cursor.on.entries[index].addr)
		else:
			raise Errors.NotAllowed(Json.by, self)

	def fetch(self, jsonpath: str) -> 'Json':
		"""JSONパスと一致するエントリーを取得

		Args:
			jsonpath: JSONパス
		Returns:
			インスタンス
		Raises:
			OutOfBounds: 存在しないエントリーを指定
		"""
		routes = DSN.elements(jsonpath)
		cursor = self.cursor
		for i in range(len(routes)):
			cursor = Json(cursor).by(routes[i]).cursor

		return Json(cursor)

	# endregion
	# region 実体参照

	@property
	def cursor_id(self) -> uint64:
		"""Returns: カーソルのアドレスID"""
		return uint64(self.cursor.to_addr_id())

	@property
	def entity_at(self) -> CP[void]:
		"""Returns: 実体のアドレス"""
		if self.cursor.on.entry_type == JsonEntryTypes.Boolean:
			return CP(self.cursor.on.as_bool)
		elif self.cursor.on.entry_type == JsonEntryTypes.Integer:
			return CP(self.cursor.on.as_int)
		elif self.cursor.on.entry_type == JsonEntryTypes.Float:
			return CP(self.cursor.on.as_float)
		elif self.cursor.on.entry_type == JsonEntryTypes.String:
			return CP(self.cursor.on.as_string)
		else:
			return CP(self)

	@property
	def as_bool(self) -> bool:
		"""Returns: 値 Raises: NotAllowed: Boolean以外で使用"""
		if self.cursor.on.entry_type != JsonEntryTypes.Boolean:
			raise Errors.NotAllowed(Json.as_bool, self)

		return self.cursor.on.as_bool

	@property
	def as_int(self) -> int:
		"""Returns: 値 Raises: NotAllowed: Integer以外で使用"""
		if self.cursor.on.entry_type != JsonEntryTypes.Integer:
			raise Errors.NotAllowed(Json.as_int, self)

		return self.cursor.on.as_int

	@property
	def as_float(self) -> float:
		"""Returns: 値 Raises: NotAllowed: Float以外で使用"""
		if self.cursor.on.entry_type != JsonEntryTypes.Float:
			raise Errors.NotAllowed(Json.as_float, self)

		return self.cursor.on.as_float

	@property
	def as_string(self) -> Annotated[str, Embed.immutable]:
		"""Returns: 値 @immutable Raises: NotAllowed: String以外で使用"""
		if self.cursor.on.entry_type != JsonEntryTypes.String:
			raise Errors.NotAllowed(Json.as_string, self)

		return self.cursor.on.as_string

	# endregion
	# region 要素更新

	def set_value[T_Value: (bool, int, float, str, 'Json', CSP[JsonEntry])](self, value: Annotated[T_Value, Embed.immutable]) -> None:
		"""値を更新 Args: value: 値 @immutable Raises: NotAllowed: 読み取り専用"""
		if self.cursor.on.read_only:
			raise Errors.NotAllowed(Json.set_value, self)

		if isinstance(value, bool):
			self.cursor.on.set_bool(value)
		elif isinstance(value, int):
			self.cursor.on.set_int(value)
		elif isinstance(value, float):
			self.cursor.on.set_float(value)
		elif isinstance(value, str):
			self.cursor.on.set_string(value)
		elif isinstance(value, Json):
			self.cursor.on.copy_value(cast(Json, value).cursor)
		elif isinstance(value, unpack_shared(CSP[JsonEntry])):
			self.cursor.on.copy_value(cast(CSP[JsonEntry], value).addr)

	def apply_at[T_Value: (bool, int, float, str, 'Json', CSP[JsonEntry])](self, index: int, value: Annotated[T_Value, Embed.immutable]) -> None:
		"""配列の要素を追加/反映 Args: index: インデックス value: 値 @immutable

		Raises:
			NotAllowed: 読み取り専用
			NotAllowed: Array以外で使用
			InvalidArguments: 対象外のインデックスを指定
		Note:
			XXX CSP[JsonEntry]を指定した場合はisolateせずそのまま登録する
		"""
		if self.cursor.on.read_only:
			raise Errors.NotAllowed(Json.apply_at, self)
		elif self.cursor.on.entry_type != JsonEntryTypes.Array:
			raise Errors.NotAllowed(Json.apply_at, self)
		elif not (index >= 0 and index <= self.length + 1):
			raise Errors.InvalidArguments(Json.apply_at, self, index)

		if index < self.length:
			self.at(index).set_value(value)
			return

		if isinstance(value, bool):
			self.cursor.on.append(Json.new_bool(value))
		elif isinstance(value, int):
			self.cursor.on.append(Json.new_int(value))
		elif isinstance(value, float):
			self.cursor.on.append(Json.new_float(value))
		elif isinstance(value, str):
			self.cursor.on.append(Json.new_string(value))
		elif isinstance(value, Json):
			self.cursor.on.append(cast(Json, value).cursor.on.isolate(self.read_only))
		elif isinstance(value, unpack_shared(CSP[JsonEntry])):
			new_entry = cast(CSP[JsonEntry], value)
			new_entry.on.freeze(self.read_only)
			self.cursor.on.append(new_entry)

	def apply_of[T_Value: (bool, int, float, str, 'Json', CSP[JsonEntry])](self, key: str, value: Annotated[T_Value, Embed.immutable]) -> None:
		"""オブジェクトの要素を追加/反映 Args: key: キー value: 値 @immutable

		Raises:
			NotAllowed: 読み取り専用
			NotAllowed: Object以外で使用
		Note:
			XXX CSP[JsonEntry]を指定した場合はisolateせずそのまま登録する
		"""
		if self.cursor.on.read_only:
			raise Errors.NotAllowed(Json.apply_of, self)
		elif self.cursor.on.entry_type != JsonEntryTypes.Object:
			raise Errors.NotAllowed(Json.apply_of, self)

		if self.has_key(key):
			self.by(key).set_value(value)
			return

		if isinstance(value, bool):
			self.cursor.on.join(key, Json.new_bool(value))
		elif isinstance(value, int):
			self.cursor.on.join(key, Json.new_int(value))
		elif isinstance(value, float):
			self.cursor.on.join(key, Json.new_float(value))
		elif isinstance(value, str):
			self.cursor.on.join(key, Json.new_string(value))
		elif isinstance(value, Json):
			self.cursor.on.join(key, cast(Json, value).cursor.on.isolate(self.read_only))
		elif isinstance(value, unpack_shared(CSP[JsonEntry])):
			new_entry = cast(CSP[JsonEntry], value)
			new_entry.on.freeze(self.read_only)
			self.cursor.on.join(key, new_entry)

	def freeze(self, on: bool = True) -> None:
		"""読み取り設定を変更 Args: on: True = 読み取り専用 (default = True) Raises: NotAllowed: ルート要素以外で使用"""
		if not self.is_root:
			raise Errors.NotAllowed(Json.freeze, self)

		self.cursor.on.freeze(on)

	# endregion
	# region 要素削除

	def remove_at(self, index: int) -> None:
		"""配列の指定インデックスを削除 Args: index: インデックス

		Raises:
			NotAllowed: 読み取り専用
			NotAllowed: Array以外で使用
			OutOfBounds: 存在しないエントリーを指定
		"""
		if self.cursor.on.read_only:
			raise Errors.NotAllowed(Json.remove_at, self)
		elif self.cursor.on.entry_type != JsonEntryTypes.Array:
			raise Errors.NotAllowed(Json.remove_at, self)

		self.cursor.on.remove_at(index)

	def remove_of(self, key: str) -> None:
		"""オブジェクトの指定キーを削除 Args: key: キー

		Raises:
			NotAllowed: 読み取り専用
			NotAllowed: Object以外で使用
			OutOfBounds: 存在しないエントリーを指定
		"""
		if self.cursor.on.read_only:
			raise Errors.NotAllowed(Json.remove_of, self)
		elif self.cursor.on.entry_type != JsonEntryTypes.Object:
			raise Errors.NotAllowed(Json.remove_of, self)

		self.cursor.on.remove_of(key)

	def clear(self) -> None:
		"""配下要素を全て削除 Raises: NotAllowed: 読み取り専用"""
		if self.cursor.on.read_only:
			raise Errors.NotAllowed(Json.clear, self)

		self.cursor.on.clear()

	# endregion
	# region 複製

	def isolate(self, owner: 'CP[Json] | None' = None) -> CSP[JsonEntry]:
		"""自身を基点に複製。読み取り属性は接続先に依存。接続先が無い場合は自身の設定を引き継ぐ

		Args:
			owner: 接続先のインスタンス | None (default = None)
		Returns:
			JSONエントリー
		"""
		return self.cursor.on.isolate(owner.on.read_only if owner else self.cursor.on.read_only)

	# endregion
	# region シリアライズ

	def to_json(self) -> CSP[JsonEntry]:
		"""JSONシリアライズ Returns: JSONエントリー"""
		return self.cursor.on.isolate(self.read_only)

	def from_json(self, json: 'Json') -> None:
		"""JSONデシリアライズ Args: json: JSON Raises: NotAllowed: 読み取り専用"""
		if self.cursor.on.read_only:
			raise Errors.NotAllowed(Json.from_json, self)

		self.cursor.on.copy_value(json.cursor)

	@Embed.pure
	def serialize(self) -> str:
		"""Returns: JSON文字列"""
		builder = StringBuilder()
		self.__build_string(self.cursor, CP(builder))
		return builder.ToString()

	@classmethod
	def __build_string(cls, entry: CP[JsonEntry], builder: CP[StringBuilder]) -> None:
		"""Args: entry: JSON, builder: ストリングビルダー"""
		if entry.on.entry_type == JsonEntryTypes.Boolean:
			builder.on.Append('true' if entry.on.as_bool else 'false')
		elif entry.on.entry_type == JsonEntryTypes.Integer:
			builder.on.Append(str(entry.on.as_int))
		elif entry.on.entry_type == JsonEntryTypes.Float:
			builder.on.Append(str(entry.on.as_float))
		elif entry.on.entry_type == JsonEntryTypes.String:
			builder.on.Append('\"')
			builder.on.Append(String.escape(entry.on.as_string, char('"')))
			builder.on.Append('\"')
		elif entry.on.entry_type == JsonEntryTypes.Array:
			builder.on.Append('[')
			for index, in_entry in enumerate(entry.on.entries):
				if index > 0:
					builder.on.Append(',')

				cls.__build_string(in_entry.addr, builder)

			builder.on.Append(']')
		else:
			builder.on.Append('{')
			for index, in_entry in enumerate(entry.on.entries):
				if index > 0:
					builder.on.Append(',')

				builder.on.Append('\"')
				builder.on.Append(entry.on.keys[index])
				builder.on.Append('\":')
				cls.__build_string(in_entry.addr, builder)

			builder.on.Append('}')

	# endregion
