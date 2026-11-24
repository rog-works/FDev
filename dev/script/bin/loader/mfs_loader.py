import glob
import hashlib
import os
from typing import Any, ClassVar, Self, TypeAlias, TypedDict, override

from tranp.app.lang.convertion import as_a

from helper.schema.json_serialize import to_json
from helper.schema.yaml_extension import yaml_load
from script.bin.loader.master_loader import MasterLoader

ComDict: TypeAlias = dict[str, list[Any]]
FuncDict = TypedDict('FuncDict', {'desc': str, 'hash': str, 'params': list[ComDict], 'statements': list[ComDict]})


class MFSLoader(MasterLoader):
	"""マスターローダー(マテリアル関数/マテリアル)"""

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
		filepaths = [filepath for filepath in glob.glob(os.path.join(root_dir, 'func/**/*.yml'), recursive=True) if filepath.find(MFSMaster.ExportsFileName) == -1]
		filepaths.extend(glob.glob(os.path.join(root_dir, 'material/**/*.yml'), recursive=True))
		return filepaths

	@classmethod
	@override
	def _support_hash(cls) -> bool:
		"""Returns: True = ハッシュ保存に対応"""
		return True

	@classmethod
	@override
	def _save_impl(cls, output_dir: str, filepaths: list[str], force: bool) -> None:
		"""マスターデータを出力

		Args:
			output_dir: 出力ディレクトリー
			filepaths: 入力データのファイルパスリスト
			force: True = 強制出力
		"""
		masters: dict[str, list[MFSMaster]] = {}
		depends: dict[str, list[str]] = {}
		for filepath in filepaths:
			relative_filepath = os.path.relpath(filepath, cls.master_root())
			module_path = os.path.splitext(relative_filepath)[0].replace(os.path.sep, '.')
			in_masters, in_depends = MFSMaster.load(filepath)
			masters[module_path] = in_masters
			depends[module_path] = in_depends

		sorted_masters: list[MFSMaster] = []
		for module_path in cls._lookup(depends):
			# XXX exportsの除外
			if module_path in masters:
				sorted_masters.extend(masters[module_path])

		with cls._open_app(output_dir, cls.domain()) as f:
			cls._write_json({master.src: master.func for master in sorted_masters}, f)

	@classmethod
	def _lookup(cls, depends: dict[str, list[str]]) -> list[str]:
		"""モジュールパスを参照順にルックアップ

		Args:
			depends: 依存モジュール一覧
		Returns:
			モジュールパスリスト
		"""
		results: list[str] = []
		entries = list(depends.keys())
		while len(entries) > 0:
			entry = entries.pop(0)
			for module_path in cls._lookup_bubbling(depends, entry, results):
				if module_path not in results:
					results.append(module_path)

				if module_path in entries:
					entries.remove(module_path)

		return results

	@classmethod
	def _lookup_bubbling(cls, depends: dict[str, list[str]], entry: str, all_results: list[str]) -> list[str]:
		"""モジュールパスを参照順にルックアップ

		Args:
			depends: 依存モジュール一覧
			entry: モジュールパス(エントリーポイント)
			all_results: モジュールパスリスト(全体)
		Returns:
			モジュールパスリスト(今回)
		"""
		in_results: list[str] = []
		for depended_module_path in depends.get(entry, []):
			for module_path in cls._lookup_bubbling(depends, depended_module_path, all_results):
				if module_path not in all_results:
					all_results.append(module_path)
					in_results.append(module_path)

		if entry not in all_results:
			all_results.append(entry)
			in_results.append(entry)

		return in_results


class MFSMaster:
	"""マスターデータ(マテリアル関数/マテリアル)"""

	ExportsFileName: ClassVar = 'mfs_exports'
	__ExportFuncs: ClassVar[dict[str, FuncDict]] = {}

	@classmethod
	def load(cls, filepath: str) -> tuple[list[Self], list[str]]:
		"""インスタンスを生成

		Args:
			filepath: ファイルパス
		Returns:
			(インスタンスリスト, 依存モジュールリスト)
		"""
		funcs, depends = cls.__load_yml(filepath)
		return [cls.__build(src, func) for src, func in funcs.items()], depends

	@classmethod
	def __load_yml(cls, filepath: str) -> tuple[dict[str, FuncDict], list[str]]:
		"""関数データをロード

		Args:
			filepath: ファイルパス
		Returns:
			(関数データ一覧, 依存モジュールリスト)
		"""
		entries = as_a(dict, yaml_load(filepath))
		depends = as_a(list, entries.pop('depends'))
		return entries, depends

	@classmethod
	def __build(cls, src: str, func: FuncDict) -> Self:
		"""インスタンスを構築

		Args:
			src: アセットソースパス(ドメイン相対/マテリアル)
			func: 関数データ
		Returns:
			インスタンス
		"""
		func['hash'] = hashlib.md5(to_json((src, func)).encode('utf-8')).hexdigest()

		# 公開パラメーターを追加
		first_key = list(func['statements'][0].keys())[0]
		if first_key.startswith('exports_'):
			func['statements'].pop(0)
			exports = cls.__exports_by(first_key)
			for statement in reversed(exports['statements']):
				func['statements'].insert(0, statement)

		return cls(src, func)

	@classmethod
	def __exports_by(cls, name: str) -> FuncDict:
		"""公開パラメーターの関数データを取得

		Args:
			name: 公開パラメーター名
		Returns:
			関数データ
		"""
		if not cls.__ExportFuncs:
			filepath = os.path.join(MFSLoader.master_root(), 'func', 'exports', f'{cls.ExportsFileName}.yml')
			cls.__ExportFuncs, _ = cls.__load_yml(filepath)

		return cls.__ExportFuncs[f'func/exports/{name}']

	def __init__(self, src: str, func: FuncDict) -> None:
		"""インスタンスを生成

		Args:
			src: アセットソースパス(ドメイン相対/マテリアル)
			func: 関数データ
		Note:
			XXX 関数名の接頭辞をフォルダー名とする
		"""
		self.src = src
		self.func = func

	def to_json(self) -> str:
		"""Returns: JSON"""
		return to_json(self.func)

	def pretty(self) -> str:
		"""Returns: フォーマット文字列"""
		return to_json(self.func, pretty=True)
