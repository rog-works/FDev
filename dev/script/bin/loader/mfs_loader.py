import glob
import hashlib
import os
from typing import Any, ClassVar, Self, TypeAlias, TypedDict, override

from tranp.app.lang.convertion import as_a

from helper.env.directories import master_dir
from helper.schema.json_serialize import to_json
from helper.schema.yaml_extension import yaml_load
from script.bin.loader.master_loader import MasterLoader

ComDict: TypeAlias = dict[str, list[Any]]
FuncDict = TypedDict('FuncDict', {'desc': str, 'hash': str, 'params': list[ComDict], 'statements': list[ComDict]})


class MFSLoader(MasterLoader):
	"""マスターローダー(マテリアル関数)"""

	@classmethod
	@override
	def domain(cls) -> str:
		"""Returns: ドメイン名"""
		return 'mfs'

	@classmethod
	@override
	def find_files(cls, root_dir: str, find_ext: str = '') -> list[str]:
		"""ルートディレクトリー配下のマスターデータを抽出

		Args:
			root_dir: ルートディレクトリー
			find_ext: 検索対象の拡張子 (default = '')
		Returns:
			パスリスト
		Note:
			XXX 公開パラメーター用のファイルは除外する
		"""
		return [filepath for filepath in glob.glob(os.path.join(root_dir, f'{cls.domain()}_*.yml')) if filepath.find(MFSMaster.ExportsFileName) == -1]

	@classmethod
	@override
	def dryrun(cls, filepath: str, pretty: bool = False) -> None:
		"""空実行

		Args:
			filepath: 入力データのファイルパス
			pretry: True = 整形 (default = False)
		"""
		for master in MFSMaster.load(filepath):
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
		masters: list[MFSMaster] = []
		for filepath in filepaths:
			masters.extend(MFSMaster.load(filepath))

		with cls._open_app(cls.domain()) as f:
			cls._write_json({master.src: master.func for master in masters}, f)


class MFSMaster:
	"""マスターデータ(マテリアル関数)"""

	ExportsFileName: ClassVar[str] = 'mfs_10_exports'
	__export_funcs: ClassVar[dict[str, FuncDict]] = {}

	@classmethod
	def load(cls, filepath: str) -> list[Self]:
		"""インスタンスを生成

		Args:
			filepath: ファイルパス
		Returns:
			インスタンスリスト
		"""
		return [cls.__build(name, func) for name, func in cls.__load_yml(filepath).items()]

	@classmethod
	def __load_yml(cls, filepath: str) -> dict[str, FuncDict]:
		"""関数データをロード

		Args:
			filepath: ファイルパス
		Returns:
			関数データ一覧
		"""
		return as_a(dict, yaml_load(filepath))

	@classmethod
	def __build(cls, name: str, func: FuncDict) -> Self:
		"""マテリアル関数マスターを生成

		Args:
			name: ファイルパス
			func: 関数データ
		Returns:
			インスタンス
		"""
		func['hash'] = hashlib.md5(to_json((name, func)).encode('utf-8')).hexdigest()

		# 公開パラメーターを追加
		first_key = list(func['statements'][0].keys())[0]
		if first_key.startswith('exports_'):
			func['statements'].pop(0)
			exports = cls.__exports_by(first_key)
			for statement in reversed(exports['statements']):
				func['statements'].insert(0, statement)

		return cls(name, func)

	@classmethod
	def __exports_by(cls, name: str) -> FuncDict:
		"""公開パラメーターの関数データを取得

		Args:
			name: 公開パラメーター名
		Returns:
			関数データ
		"""
		if not cls.__export_funcs:
			cls.__export_funcs = cls.__load_yml(os.path.join(master_dir(), MFSLoader.domain(), f'{cls.ExportsFileName}.yml'))

		return cls.__export_funcs[name]

	def __init__(self, name: str, func: FuncDict) -> None:
		"""インスタンスを生成

		Args:
			name: 関数名
			func: 関数データ
		Note:
			XXX 関数名の接頭辞をフォルダー名とする
		"""
		self.src = f'{name.split('_')[0]}/{name}'
		self.func = func

	def to_json(self) -> str:
		"""Returns: JSON"""
		return to_json(self.func)

	def pretty(self) -> str:
		"""Returns: フォーマット文字列"""
		return to_json(self.func, pretty=True)
