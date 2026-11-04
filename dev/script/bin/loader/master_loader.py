import hashlib
import os
from abc import ABCMeta, abstractmethod
from io import TextIOWrapper
from typing import IO, Any

from const.const_asset import AssetDomains, AssetFormats
from helper.env.directories import cache_dir, master_dir, project_dir, script_dir
from helper.schema.json_serialize import save_json


class MasterLoader(metaclass=ABCMeta):
	"""マスターローダー(基底)"""

	@classmethod
	@abstractmethod
	def domain(cls) -> str:
		"""Returns: ドメイン名"""
		...

	@classmethod
	def script_root(cls) -> str:
		"""Returns: ルートディレクトリー(定義データ)"""
		return os.path.join(script_dir(), cls.domain())

	@classmethod
	def master_root(cls) -> str:
		"""Returns: ルートディレクトリー(マスターデータ)"""
		return os.path.join(master_dir(), cls.domain())

	@classmethod
	@abstractmethod
	def find_files(cls, root_dir: str, find_ext: str = '') -> list[str]:
		"""ルートディレクトリー配下のマスターデータを抽出

		Args:
			root_dir: ルートディレクトリー
			find_ext: 検索対象の拡張子 (default = '')
		Returns:
			パスリスト
		"""
		...

	@classmethod
	@abstractmethod
	def dryrun(cls, filepath: str, pretty: bool = False) -> None:
		"""空実行

		Args:
			filepath: 入力データのファイルパス
			pretry: True = 整形 (default = False) (default = False)
		"""
		...

	@classmethod
	def _support_hash(cls) -> bool:
		"""Returns: True = ハッシュ保存に対応"""
		return False

	@classmethod
	def save(cls, filepaths: list[str], force: bool = False) -> None:
		"""マスターデータを出力

		Args:
			filepaths: 入力データのファイルパスリスト
			force: True = 強制出力 (default = False)
		"""
		if cls._support_hash():
			cls._save_with_hash(filepaths, force)
		else:
			cls._save_without_hash(filepaths, force)

	@classmethod
	def _save_with_hash(cls, filepaths: list[str], force: bool) -> None:
		"""マスターデータを出力(ハッシュ対応)

		Args:
			filepaths: 入力データのファイルパスリスト
			force: True = 強制出力
		"""
		hash_filepath = cls._hash_filepath()
		new_hash = cls._calc_hash(filepaths)
		old_hash = cls._load_hash(hash_filepath)
		if force or new_hash != old_hash:
			cls._save_impl(filepaths, force)
			cls._save_hash(hash_filepath, new_hash)

	@classmethod
	def _save_without_hash(cls, filepaths: list[str], force: bool) -> None:
		"""マスターデータを出力(ハッシュ非対応)

		Args:
			filepaths: 入力データのファイルパスリスト
			force: True = 強制出力
		"""
		cls._save_impl(filepaths, force)

	@classmethod
	@abstractmethod
	def _save_impl(cls, filepaths: list[str], force: bool) -> None:
		"""マスターデータを出力

		Args:
			filepaths: 入力データのファイルパスリスト
			force: True = 強制出力
		"""
		...

	@classmethod
	def _open_app(cls, src: str) -> TextIOWrapper:
		"""出力データのファイルを開く(アプリケーション用) @see _open"""
		return cls._open(AssetDomains.MasterApp.value, src)

	@classmethod
	def _open(cls, domain: str, src: str) -> TextIOWrapper:
		"""出力データのファイルを開く

		Args:
			domain: アセットドメイン
			src: 出力データのソースパス
		Returns:
			IO
		"""
		filepath = os.path.join(project_dir(), AssetFormats.MasterFilepath.value.format(path=os.path.join(domain, src)))
		return open(filepath, mode='w', encoding='utf-8', newline='')

	@classmethod
	def _write_json(cls, data: Any, f: IO) -> None:
		"""データの書き込み

		Args:
			data: 書き込みデータ
			f: IO
		"""
		save_json(data, f)

	@classmethod
	def _hash_filepath(cls) -> str:
		"""Returns: ハッシュファイルパス"""
		return os.path.join(cache_dir(), 'master', f'{cls.domain()}-hashs.txt')

	@classmethod
	def _calc_hash(cls, filepaths: list[str]) -> str:
		"""マスターデータのハッシュを算出

		Args:
			filepaths: 入力データのファイルパスリスト
		Returns:
			ハッシュ値
		"""
		join_hashs = ''
		for filepath in filepaths:
			with open(filepath, mode='r', encoding='utf-8') as f:
				body = f'{filepath}{f.read()}'
				join_hashs += hashlib.md5(body.encode('utf-8')).hexdigest()

		return hashlib.md5(join_hashs.encode('utf-8')).hexdigest()

	@classmethod
	def _load_hash(cls, hash_filepath: str) -> str:
		"""マスターデータのハッシュを読み込み

		Args:
			hash_filepath: ハッシュのファイルパス
		Returns:
			ハッシュ値
		"""
		if not os.path.exists(hash_filepath):
			return ''

		with open(hash_filepath, mode='r', encoding='utf-8') as f:
			return f.read()

	@classmethod
	def _save_hash(cls, hash_filepath: str, hash: str) -> None:
		"""マスターデータのハッシュを保存

		Args:
			hash_filepath: ハッシュのファイルパス
			hash: ハッシュ値
		"""
		dir_path = os.path.dirname(hash_filepath)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

		with open(hash_filepath, mode='w', encoding='utf-8', newline='') as f:
			f.write(hash)
