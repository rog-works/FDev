from typing import Any, cast

from tranp.app.compatible.cpp.cvar import CP


def reserve_array(arr: list[Any], size: int) -> None:
	"""配列の領域確保ヘルパー

	Args:
		arr: 配列
		size: 領域サイズ
	Note:
		```
		* 領域確保のみを行う。目的はメモリーの再配置の回避
		* 要素のインスタンス化は行わないため、appendしない限り要素は増えない点に注意
		```
	"""
	...


def zerofill_array[T](value_type: type[T], arr: list[T], size: int) -> None:
	"""配列の初期化ヘルパー

	Args:
		value_type: 値の型
		arr: 配列
		size: 領域サイズ
	Note:
		* 領域確保とインスタンスを生成を行い、メモリーのゼロ初期化を行う
		* 値の型は引数無しで生成できることが必須要件
	"""
	for _ in range(size):
		arr.append(value_type())


def array_to_raw[T](arr: list[T]) -> CP[T]:
	"""配列の実体の先頭アドレスに変換

	Returns:
		実体の先頭アドレス
	"""
	return cast(CP[Any], arr)
