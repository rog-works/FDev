# @see Engine/Source/Runtime/Core/Public/Serialization/BufferArchive.h

from typing import Any, override

from tranp.app.compatible.cpp.classes import uint8
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Serialization.Archive import Archive

from compatible.error import Errors


@Embed.alias('F', prefix=True)
class BufferArchive(Archive):
	"""バイト配列 + ストリームライター

	Note:
		```
		### 注意事項
		* C++ではlist[uint8] + MemoryWriterの派生型
		* PythonではC++のインターフェイスを模擬するのみ
		* 内部ポインターをアプリケーション側で評価してはならない
		```
	"""

	buff: list[Any]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.buff = []

	# region ストリーム

	@override
	def GetData(self) -> list[Any]:
		"""Returns: 内部ポインター ※C++ではCP[uint8]"""
		return self.buff

	@override
	def set_data(self, buff: list[Any]) -> None:
		"""Args: buff: バイト配列 @python"""
		self.buff = buff

	# region リスト

	def SetNumZeroed(self, size: int) -> None:
		"""指定のサイズでゼロ初期化
		
		Args:
			size: サイズ
		"""
		...

	def Add(self, value: uint8) -> None:
		"""値を追加

		Args:
			value: 値
		Raises:
			XXX Pythonでは使用禁止
		"""
		raise Errors.Never

	# endregion
	# region ストリーム/ライター

	@Embed.python
	@classmethod
	def write[T_Scalar: (bool, int, float, str)](cls, buff: 'BufferArchive', value: T_Scalar) -> None:
		"""バッファに書き込み

		Args:
			buff: ストリームライター
			value: 値
		Note:
			```
			* このメソッドはC++のストリーム入力演算子(`<<`)を模擬。C++には実在しない @see func_call/default.j2
			* 第2引数は右辺値参照できないため、一旦左辺値を経由する必要がある @see #Examples
			```
		Examples:
			```python
			writer = BufferArchive()
			# NG
			BufferArchive.write(writer, self.string())
			# OK
			string = self.string()
			BufferArchive.write(writer, string)
			```
		"""
		buff.buff.append(value)

	# endregion
