import os
from typing import Any, Protocol
from unittest import mock

import yaml
import yaml.constructor
from tranp.app.lang.annotation import duck_typed
from tranp.app.lang.convertion import as_a
from tranp.app.lang.dict import dict_pluck
from tranp.app.lang.module import to_fullyname


class YamlExtension(Protocol):
	"""PyYAML拡張プロトコル

	Examples:
		```python
		class MyExtension:
			def __init__(self, **kwargs: Any) -> None:
				self.var = kwargs.get('var')

			def tag(self) -> str:
				return '!{tag_name}'

			def __call__(self, loader: yaml.SafeLoader, node: yaml.Node) -> Any:
				return {output_node}
		```
	"""

	def __init__(self, **kwargs: Any) -> None:
		"""インスタンスを生成

		Args:
			**kwargs: 追加の引数
		"""

	def tag(self) -> str:
		"""Returns: タグ名"""
		...

	def __call__(self, loader: yaml.SafeLoader, node: yaml.Node) -> Any:
		"""ノードを解析して出力

		Args:
			loader: ローダー ※AppLoaderの想定
			node: ノード(オリジナル)
		Returns:
			出力ノード
		Note:
			* 出力ノードはrepresenterの実装が必要な場合のみPyYAML拡張のインスタンスにすれば良い
			* 素の値(bool/int/float/str/list/dict)で出力した方が後処理も不要で扱いも簡単なためこちらを推奨
		"""
		...


@duck_typed(YamlExtension)
class YamlImport:
	"""PyYAML拡張(外部インポート)"""

	def __init__(self, **kwargs: Any) -> None:
		"""インスタンスを生成

		Args:
			**kwargs: 追加の引数
		"""
		self.root_dir = kwargs.get('root_dir', os.getcwd())
		self.caches: dict[str, Any] = {}

	def tag(self) -> str:
		"""Returns: タグ名"""
		return '!import'

	def __call__(self, loader: yaml.SafeLoader, node: yaml.Node) -> Any:
		"""ノードを解析して出力

		Args:
			loader: ローダー
			node: ノード
		Returns:
			出力ノード
		"""
		elems = as_a(str, loader.construct_scalar(node)).split('#')
		path = elems[0]
		jsonpath = elems[1] if len(elems) == 2 else '$'
		data = self.load(path)
		return dict_pluck(data, jsonpath) if jsonpath != '$' else data

	def load(self, path: str) -> Any:
		"""YAMLをロード

		Args:
			path: ファイルパス
		Returns:
			データ
		"""
		if path not in self.caches:
			filepath = os.path.join(self.root_dir, f'{path}.yml')
			with open(filepath, mode='r', encoding='utf-8') as f:
				self.caches[path] = yaml.load(f, Loader=yaml.SafeLoader)

		return self.caches[path]


def yaml_load(filepath: str, ext_types: list[type[YamlExtension]] = [], **kwargs: Any) -> Any:
	"""YAMLをロード

	Args:
		filepath: ファイルパス
		extensions: PyYAML拡張リスト (default = [])
	Returns:
		データ
	"""
	for ext_type in ext_types:
		extension = ext_type(**kwargs)
		yaml.add_constructor(extension.tag(), extension, Loader=yaml.SafeLoader)

	if not YamlImport in ext_types:
		with open(filepath, mode='r', encoding='utf-8') as f:
			return yaml.load(f, Loader=yaml.SafeLoader)

	# XXX カスタムタグをマージ出来るようにするため、モンキーパッチで対応
	with mock.patch(to_fullyname(yaml.constructor.SafeConstructor.construct_mapping), construct_mapping_patch):
		with mock.patch(to_fullyname(yaml.constructor.SafeConstructor.flatten_mapping), flatten_mapping_patch):
			with open(filepath, mode='r', encoding='utf-8') as f:
				return yaml.load(f, Loader=yaml.SafeLoader)


def construct_mapping_patch(self: yaml.constructor.SafeConstructor, node: yaml.nodes.MappingNode, deep: bool = False) -> Any:
	"""連想配列を解析(モンキーパッチ)

	Args:
		node: ノード(連想配列)
		deep: True = 再帰的に処理
	Returns:
		値
	Note:
		XXX 元の実装ではelse条件にconstruct_mappingが存在するが、デッドコードなので削除
	"""
	return flatten_mapping_patch(self, node, deep)
	

def flatten_mapping_patch(self: yaml.constructor.SafeConstructor, node: yaml.nodes.MappingNode, deep: bool = False) -> Any:
	"""連想配列を展開(モンキーパッチ)

	Args:
		node: ノード(連想配列)
		deep: True = 再帰的に処理 (XXX 本来は存在しない引数)
	Returns:
		値
	Note:
		```
		XXX 本来は内部要素を改変するだけで何も返さないメソッド(どうせ直後にデータ変換するのだから無駄な分離)
		XXX 直接内部でデータ生成まで行うことでカスタムタグの展開処理と統合
		```
	"""
	in_nodes: list[tuple[yaml.nodes.Node, yaml.nodes.Node]] = node.value
	merge: dict[str, Any] = {}
	for in_node in in_nodes:
		key_node, value_node = in_node
		if key_node.tag == 'tag:yaml.org,2002:merge':
			if not value_node.tag.startswith('tag:yaml.org'):
				data = as_a(dict, self.construct_object(value_node))
				merge.update(data)
			elif isinstance(value_node, yaml.nodes.MappingNode):
				data = flatten_mapping_patch(self, value_node, deep)
				merge.update(data)
			elif isinstance(value_node, yaml.nodes.SequenceNode):
				for subnode in value_node.value:
					if not isinstance(subnode, yaml.nodes.MappingNode):
						raise ValueError('Unexpected value in array', key_node, value_node)

					in_data = flatten_mapping_patch(self, subnode, deep)
					merge.update(in_data)
			else:
				raise ValueError('Unexpected value', key_node, value_node)
		else:
			key_data = as_a(str, self.construct_object(key_node))
			value_data = self.construct_object(value_node, deep=deep)
			merge[key_data] = value_data

	return merge
