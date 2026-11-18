import glob
import json
import os
from collections.abc import Callable
from typing import Self, override

from tranp.app.lang.module import load_module

from helper.env.directories import master_dir
from helper.schema.json_serialize import to_json
from script.bin.loader.master_helper import MasterHelper
from script.bin.loader.master_loader import MasterLoader
from script.mis.core.mi_definition import DataDict


class MISLoader(MasterLoader):
	"""マスターローダー(マテリアルインスタンス)"""

	@classmethod
	@override
	def domain(cls) -> str:
		"""Returns: ドメイン名"""
		return 'mis'

	@classmethod
	@override
	def find_files(cls, root_dir: str, find_ext: str = '') -> list[str]:
		"""ルートディレクトリー配下のマスターデータを抽出

		Args:
			root_dir: ルートディレクトリー
			find_ext: 検索対象の拡張子 (default = '')
		Returns:
			パスリスト
		"""
		ext = find_ext if find_ext else 'json'
		return glob.glob(os.path.join(root_dir, '**', f'{cls.domain()}_*.{ext}'), recursive=True)

	@classmethod
	@override
	def dryrun(cls, filepath: str, pretty: bool = False) -> None:
		"""空実行

		Args:
			filepath: 入力データのファイルパス
			pretry: True = 整形 (default = False)
		"""
		for master in MISMaster.load(filepath):
			print(master.pretty() if pretty else master.to_json())

	@classmethod
	@override
	def _support_hash(cls) -> bool:
		"""Returns: True = ハッシュ保存に対応"""
		return True

	@classmethod
	@override
	def _save_impl(cls, filepaths: list[str], force: bool) -> None:
		"""マスターデータを出力

		Args:
			filepaths: 入力データのファイルパスリスト
			force: True = 強制出力
		"""
		masters: list[MISMaster] = []
		for filepath in filepaths:
			masters.extend(MISMaster.load(filepath))

		with cls._open_app(cls.domain()) as f:
			cls._write_json({master.src: master.data for master in masters}, f)


class MISMaster:
	"""マスターデータ(マテリアルインスタンス)"""

	@classmethod
	def load(cls, filepath: str) -> list[Self]:
		"""インスタンスを生成

		Args:
			filepath: ファイルパス
		Returns:
			インスタンスリスト
		"""
		rel_path = os.path.relpath(filepath, os.path.join(master_dir(), MISLoader.domain()))
		base_dir = os.path.splitext(rel_path)[0].replace(f'{MISLoader.domain()}_', '').replace(os.path.sep, '/')
		return [cls(f'{base_dir}/{name}', func) for name, func in cls.__load(filepath).items()]

	@classmethod
	def __load(cls, filepath: str) -> dict[str, DataDict]:
		"""インスタンスデータをロード

		Args:
			filepath: ファイルパス
		Returns:
			インスタンスデータ一覧
		"""
		with open(filepath, mode='r', encoding='utf-8') as f:
			return json.load(f)

	def __init__(self, src: str, data: DataDict) -> None:
		"""インスタンスを生成

		Args
			src: ソースパス
			data: インスタンスデータ
		"""
		self.src = src
		self.data = data

	def to_json(self) -> str:
		"""Returns: JSON"""
		return to_json(self.data)

	def pretty(self) -> str:
		"""Returns: フォーマット文字列"""
		return to_json(self.data, pretty=True)


class MISDefinition:
	"""定義データ(マテリアルインスタンス)"""

	@classmethod
	def load(cls, filepath: str) -> dict[str, DataDict]:
		"""定義ファイルをロード

		Args:
			filepath: ファイルパス(定義データ)
		Returns:
			定義データ
		"""
		module_path = MasterHelper.to_module_path(filepath)
		func: Callable[[], dict[str, DataDict]] = load_module(module_path, 'export')
		return func()
