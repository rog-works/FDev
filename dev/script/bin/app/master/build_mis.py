import os
import sys

from helper.schema.json_serialize import to_json
from script.bin.loader.master_helper import MasterHelper
from script.bin.loader.mis_loader import MISDefinition, MISLoader


class App:
	"""アプリケーション"""

	def run(self, force: bool) -> None:
		"""実行処理

		Args:
			force: True = 強制実行
		"""
		root_dir = MISLoader.script_root()
		for filepath in MISLoader.find_files(root_dir, find_ext='py'):
			master_path = MasterHelper.to_master_path(filepath, master_ext='json')
			hash_path = MasterHelper.to_cache_hash_path(filepath)
			old_hash = MasterHelper.load_file(hash_path) if os.path.exists(hash_path) else ''
			new_hash = MasterHelper.calc_hash(MasterHelper.load_file(filepath))
			if force or (old_hash != new_hash):
				definition = MISDefinition.load(filepath)
				MasterHelper.save_file(master_path, to_json(definition, pretty=True))
				MasterHelper.save_file(hash_path, new_hash)
	

if __name__ == '__main__':
	App().run('-f' in sys.argv)
