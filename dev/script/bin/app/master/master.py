import os
import sys
from typing import TypedDict

from script.bin.loader.master_loader import MasterLoader
from script.bin.loader.mfs_loader import MFSLoader

ArgsDict = TypedDict('ArgsDict', {'input': str, 'domains': list[str], 'force': bool, 'pretty': bool, 'help': bool})


class Args:
	"""引数"""

	def __init__(self, argv: list[str]) -> None:
		"""インスタンスを生成

		Args:
			argv: 引数リスト
		"""
		data = self._parse(argv)
		self.input = data['input']
		self.domains = data['domains']
		self.force = data['force']
		self.pretty = data['pretty']
		self.help = data['help']

	@property
	def mode(self) -> str:
		"""Returns: 実行モード"""
		if self.input:
			return 'dryrun'
		elif self.help:
			return 'help'
		else:
			return 'output'

	def _parse(self, argv: list[str]) -> ArgsDict:
		"""引数を解析

		Args:
			argv: 引数リスト
		Returns:
			引数一覧
		"""
		args: ArgsDict = {
			'input': '',
			'domains': [],
			'force': False,
			'pretty': False,
			'help': False,
		}
		while len(argv) > 0:
			arg = argv.pop(0)
			if arg == '-i':
				args['input'] = argv.pop(0)
			elif arg == '-f':
				args['force'] = True
			elif arg == '--pretty':
				args['pretty'] = True
			elif arg == '-h':
				args['help'] = True
			elif not arg.startswith('-'):
				args['domains'].append(arg)

		return args


class App:
	"""アプリケーション"""

	def __init__(self, args: Args) -> None:
		"""インスタンスを生成

		Args:
			args: 引数
		"""
		self.args = args

	def loaders(self) -> list[type[MasterLoader]]:
		"""Returns: マスターローダーリスト"""
		return [
			MFSLoader,
		]

	def run(self) -> None:
		"""実行処理"""
		if self.args.mode == 'help':
			self._run_help()
		elif self.args.mode == 'dryrun':
			self._run_dryrun()
		else:
			self._run_output()

	def _run_help(self) -> None:
		domains = [loader.domain() for loader in self.loaders()]
		print(f"""# Usage
## Output
$ bin/master
$ bin/master -f
$ bin/master [-f] [{'] ['.join(domains)}]

## Dryrun
$ bin/master -i path/to/({'|'.join(domains)})/xxx.ext [--pretty]

## Show help
$ bin/master -h
""")

	def _run_dryrun(self) -> None:
		"""実行処理(空実行)"""
		filepath = os.path.abspath(os.path.join(os.getcwd(), self.args.input))
		for loader in self.loaders():
			if self.args.input.find(f'/{loader.domain()}/') != -1:
				loader.dryrun(filepath, self.args.pretty)

	def _run_output(self) -> None:
		"""実行処理(マスターデータ出力)"""
		for loader in self.loaders():
			runnable = len(self.args.domains) == 0 or loader.domain() in self.args.domains
			if runnable:
				root_dir = loader.master_root()
				filepaths = loader.find_files(root_dir)
				loader.save(filepaths, self.args.force)


if __name__ == '__main__':
	args = Args(sys.argv[1:])
	App(args).run()
