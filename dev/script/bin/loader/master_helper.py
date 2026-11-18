import glob
import hashlib
import os

from helper.env.directories import cache_dir, dev_dir, master_dir, script_dir


class MasterHelper:
	"""マスターデータヘルパー"""

	@classmethod
	def load_file(cls, filepath: str) -> str:
		"""ファイルをロード

		Args:
			filepath: ファイルパス
		Returns:
			コンテンツ
		"""
		with open(filepath, mode='r', encoding='utf-8') as f:
			return f.read()

	@classmethod
	def save_file(cls, filepath: str, content: str) -> None:
		"""ファイルをセーブ

		Args:
			filepath: ファイルパス
			content: コンテンツ
		"""
		if not os.path.exists(os.path.dirname(filepath)):
			os.makedirs(os.path.dirname(filepath))

		with open(filepath, mode='w', encoding='utf-8', newline='') as f:
			f.write(content)

	@classmethod
	def to_module_path(cls, script_path: str) -> str:
		"""モジュールパスに変換

		Args:
			script_path: ファイルパス(定義データ)
		Returns:
			モジュールパス
		"""
		relpath = os.path.relpath(script_path, dev_dir())
		return os.path.splitext(relpath)[0].replace(os.path.sep, '.')

	@classmethod
	def to_master_path(cls, script_path: str, master_ext: str) -> str:
		"""マスターデータのファイルパスに変換

		Args:
			script_path: ファイルパス(定義データ)
			master_ext: 拡張子(マスターデータ)
		Returns:
			ファイルパス(マスターデータ)
		"""
		relpath = os.path.relpath(script_path, script_dir())
		elems = relpath.split(os.path.sep)
		domain = elems.pop(0)
		filename = os.path.splitext(elems.pop())[0]
		return os.path.join(master_dir(), domain, *elems, f'{filename}.{master_ext}')

	@classmethod
	def to_src(cls, master_path: str) -> str:
		"""アセット相対パスに変換

		Args:
			master_path: ファイルパス(マスターデータ)
		Returns:
			アセット相対パス
		"""
		relpath = os.path.relpath(master_path, master_dir())
		elems = relpath.split(os.path.sep)
		filename = os.path.splitext(elems.pop())[0]
		return '.'.join([*elems[1:], filename])

	@classmethod
	def to_cache_hash_path(cls, filepath: str) -> str:
		"""キャッシュ用ハッシュパスに変換

		Args:
			filepath: ファイルパス
		Returns:
			キャッシュパス
		"""
		relpath = os.path.relpath(filepath, dev_dir())
		elems = relpath.split(os.path.sep)
		dir_name = elems.pop(0)
		filename = os.path.splitext(elems.pop())[0]
		return os.path.join(cache_dir(), dir_name, *elems, f'{filename}-hash.txt')

	@classmethod
	def to_cache_path(cls, master_path: str, content_hash: str) -> str:
		"""キャッシュパスに変換

		Args:
			master_path: ファイルパス(マスターデータ)
			content_hash: コンテンツのハッシュ値
		Returns:
			キャッシュパス
		"""
		relpath = os.path.relpath(master_path, master_dir())
		elems = relpath.split(os.path.sep)
		filename = os.path.splitext(elems.pop())[0]
		cache_abs_dir = os.path.join(cache_dir(), 'master', *elems)
		cache_filename = f'{filename}-{content_hash}.cache.json'
		return os.path.join(cache_abs_dir, cache_filename)

	@classmethod
	def save_cache(cls, cache_path: str, data: str) -> None:
		"""キャッシュを保存

		Args:
			cache_path: キャッシュパス
			data: データ
		"""
		if not os.path.exists(os.path.dirname(cache_path)):
			os.makedirs(os.path.dirname(cache_path))
		else:
			cls._cleanup_cache(cache_path)

		with open(cache_path, mode='w', encoding='utf-8', newline='') as f:
			f.write(data)

	@classmethod
	def _cleanup_cache(cls, cache_path: str) -> None:
		"""旧キャッシュを全て削除

		Args:
			cache_path: キャッシュパス
		"""
		begin_path = cache_path[:cache_path.rfind('-')]
		search_path = f'{begin_path}-*.cache.json'
		for old_path in glob.glob(search_path):
			os.unlink(old_path)

	@classmethod
	def calc_hash(cls, content: str) -> str:
		"""Args: content: コンテンツ Returns: ハッシュ値"""
		return hashlib.md5(content.encode('utf-8')).hexdigest()
