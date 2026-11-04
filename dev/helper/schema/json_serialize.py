from collections.abc import Callable
from enum import Enum
from json import dump as json_dump
from json import dumps as json_dumps
from typing import IO, Any


def to_json(data: Any, encoder: Callable[[Any], Any] | None = None, pretty: bool = False) -> str:
	"""JSONシリアライズ

	Args:
		data: 入力データ
		encoder: JSONエンコーダー (default = None)
		pretty: True = 整形 (default = False)
	Returns:
		JSON文字列
	"""
	if pretty:
		return json_dumps(data, indent=2, ensure_ascii=False, default=encoder)
	else:
		return json_dumps(data, separators=(',', ':'), ensure_ascii=False, default=encoder)


def save_json(data: Any, f: IO, pretty: bool = False, encoder: Callable[[Any], Any] | None = None) -> None:
	"""JSONシリアライズ

	Args:
		data: 入力データ
		f: ファイルストリーム
		pretty: True = 整形 (default = False)
		encoder: JSONエンコーダー (default = None)
	"""
	if pretty:
		json_dump(data, f, indent=2, ensure_ascii=False, default=encoder)
	else:
		json_dump(data, f, separators=(',', ':'), ensure_ascii=False, default=encoder)


def json_encoder(data: Any) -> Any:
	"""JSONエンコーダー

	Args:
		data: 入力データ
	Returns:
		エンコード後のデータ
	"""
	if isinstance(data, (bool, int, float, str)):
		return data
	elif isinstance(data, list):
		return [json_encoder(value) for value in data]
	elif isinstance(data, dict):
		return {key: json_encoder(value) for key, value in data.items()}
	elif isinstance(data, Enum):
		return json_encoder(data.value)
	else:
		return {key: json_encoder(value) for key, value in data.__dict__.items() if not key.startswith('_')}
