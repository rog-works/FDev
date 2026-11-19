import hashlib
from collections.abc import Callable
from types import TracebackType
from typing import ClassVar, Self, TypeAlias, TypedDict, TypeVar

from const.const_material import Layers
from helper.schema.json_serialize import to_json
from helper.view.relay_analyzer import RelayAnalyzer
from script.mfs.me_types import float3, texture
from script.mfs.mfs_10_exports import exports_ui_main

T_Param = TypeVar('T_Param', bool, float, float3, texture)
ParamTypes: TypeAlias = bool | float | float3 | texture
DumpTypes: TypeAlias = bool | float | tuple[float, float, float] | str
DumpDict: TypeAlias = dict[str, DumpTypes]
DataDict = TypedDict('DataDict', {'via': str, 'hash': str, 'exports': DumpDict})
Factory: TypeAlias = 'Callable[[MIDefinition], tuple[str, MIDefinition]]'


class MIDefinition:
	"""マテリアルインスタンス定義"""

	Symbol: ClassVar[str] = 'mi'

	@classmethod
	def export(cls, factories: list[Factory]) -> dict[str, DataDict]:
		"""定義ファクトリーを元に出力データを生成

		Args:
			factories: 定義ファクトリーリスト
		Returns:
			{アセット名: 出力データ}
		"""
		datums: dict[str, DataDict] = {}
		for factory in factories:
			via, definition = factory(cls())
			data = definition.to_dict()
			digest = hashlib.md5(to_json(data).encode('utf-8')).hexdigest()
			datums[factory.__name__] = {'via': via, 'hash': digest, 'exports': data}

		return datums

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.swap_bg = False
		self.params: dict[str, ParamTypes] = {}

	def __enter__(self) -> Self:
		"""トランザクション(開始) Returns: 自己参照"""
		return self

	def __exit__(self, exc_type: type[Exception], exc_value: BaseException | None, exc_traceback: TracebackType) -> None:
		"""トランザクション(終了)"""
		self.swap_bg = False

	def for_bg(self) -> Self:
		"""背景レイヤーを出力対象としてトランザクションを開始 returns: 自己参照"""
		mi = self
		mi.decl(exports_ui_main.a_flag_b1, True)
		self.swap_bg = True
		return self

	def ok(self, value: T_Param, fullfill: bool) -> T_Param | None:
		"""条件を満たした場合のみ有効な値を返却

		Args:
			value: 値
			fullfill: True = 条件達成
		Returns:
			値 | None
		"""
		return value if fullfill else None

	def decl(self, param: T_Param, value: T_Param | None) -> None:
		"""パラメーター宣言

		Args:
			param: 対象パラメーター
			value: 値 | None ※Noneの時は出力をスキップ
		"""
		if value is None:
			return

		relay = RelayAnalyzer.get().resolve(2, f'{self.Symbol}.{MIDefinition.decl.__name__}')
		layer, prop = relay.split('.')
		in_tag = Layers.Tag.value in prop
		if not in_tag and self.swap_bg:
			self.params[prop.replace(Layers.Main.value, Layers.Bg.value)] = value
		elif not in_tag:
			self.params[prop] = value
		elif self.swap_bg:
			self.params[prop.replace(Layers.Tag.value, Layers.Bg.value)] = value
		else:
			layer_id = layer[-2:]
			self.params[prop.replace(Layers.Tag.value, layer_id)] = value

	def to_dict(self) -> DumpDict:
		"""Returns: ダンプデータ"""
		data: DumpDict = {}
		for key in sorted(self.params.keys()):
			value = self.params[key]
			if isinstance(value, bool):
				data[key] = value
			elif isinstance(value, float):
				data[key] = value
			elif isinstance(value, float3):
				data[key] = (value.x, value.y, value.z)
			elif isinstance(value, texture):
				data[key] = value.src

		return data
