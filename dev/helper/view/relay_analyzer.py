from re import Match, Pattern
from re import compile as re_compile
from re import search as re_search
from sys import _getframe as getframe  # type: ignore XXX 利用面に問題はないため警告を抑制
from typing import Any, ClassVar

from tranp.app.lang.convertion import as_a


def analyze_prop(relay: Any) -> str:
	"""リレー末尾のプロパティー名を解析

	Args:
		relay: 任意のリレー
	Returns:
		プロパティー名
	Examples:
		```python
		analyze_prop(module.path.to.prop)
		> 'prop'
		```
	"""
	return RelayAnalyzer.get().resolve(2, analyze_prop.__name__).split('.')[-1]


class RelayAnalyzer:
	"""リレーアナライザー

	Note:
		```
		### 制限事項
		* ファイル毎に1種類の関数コール
		* 解析出来るリレーは第1引数のみ
		* リレーは英数字 + ドットのみ
		```
	"""

	FramePattern: ClassVar[Pattern[str]] = re_compile(r"file '(.+\.py)', line (\d+)")
	__instance: ClassVar['RelayAnalyzer | None'] = None

	@classmethod
	def get(cls) -> 'RelayAnalyzer':
		"""Returns: シングルトンインスタンス"""
		if cls.__instance is None:
			cls.__instance = cls()

		return cls.__instance
	
	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.__caches: dict[str, dict[int, str]] = {}

	def resolve(self, backtrace_at: int, calls: str) -> str:
		"""関数コールを解析し、第1引数のリレーを解決

		Args:
			backtrace_at: 遡るコール数
			calls: 探索対象の関数名(またはリレー)
		Returns:
			リレー
		"""
		frame = getframe(backtrace_at)
		matches = as_a(Match, re_search(RelayAnalyzer.FramePattern, str(frame)))
		line_index = int(matches[2]) - 1
		filepath = matches[1]
		if filepath not in self.__caches:
			self.__caches[filepath] = self.__load_calls(filepath, calls)

		return self.__caches[filepath][line_index]

	def __load_calls(self, filepath: str, calls: str) -> dict[int, str]:
		"""ソースコード内の指定の関数コールを抽出し、マップ表を出力

		Args:
			filepath: ソースファイルのパス
			calls: 探索対象の関数名(またはリレー)
		Returns:
			{行インデックス: リレー}
		"""
		pattern = re_compile(fr'{calls}\(([\w\d.]+)')
		relayed: dict[int, str] = {}
		with open(filepath, mode='r', encoding='utf-8') as f:
			for line_at, line in enumerate(f):
				if line.find(f'{calls}(') != -1:
					relayed[line_at] = as_a(Match, re_search(pattern, line))[1]

		return relayed
