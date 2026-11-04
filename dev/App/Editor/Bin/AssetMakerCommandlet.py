from enum import Enum
from typing import override

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Commandlets.Commandlet import Commandlet

from App.Editor.Asset.AssetMakerFactory import AssetMakerFactory


@Embed.python
class ArgKeys(Enum):
	"""引数のキー

	Attributes:
		Run: Commandletの起動引数
		Maker: アセットメーカー用
	"""
	Run = 'run'
	Maker = 'Maker'


@Embed.alias('U', prefix=True)
@UCLASS()
class AssetMakerCommandlet(Commandlet):
	"""コマンドランナー(アセット生成)"""

	def parse_args(self, argv: str) -> tuple[bool, list[tuple[str, str]]]:
		"""コマンドライン引数をパース

		Args:
			argv: コマンドライン引数
		Returns:
			(True = 強制実行, 引数一覧)
		Note:
			```
			### 書式
			* 全文: '{実行ファイルパス}\\UnrealEditor-Cmd.exe {プロジェクトパス}.uproject -run=AssetMakerCommandlet -Maker="{メーカータグ}: {ソースパス or all}, ..."'
			* サンプル(Maker): -Maker="mfs, force"
			```
		"""
		blocks = argv.split('-')
		del blocks[0]
		args: list[tuple[str, str]] = []
		force = False
		for block in blocks:
			arg_pair = block.strip(' ').split('=')
			if not (len(arg_pair) == 2 and arg_pair[0] == ArgKeys.Maker.value):
				continue

			arg_value = arg_pair[1][1:len(arg_pair[1]) - 1]
			pairs = arg_value.split(', ')
			for pair in pairs:
				elems = pair.split(': ')
				if len(elems) == 2:
					args.append((elems[0], elems[1]))
				elif elems[0] != 'force':
					args.append((elems[0], 'all'))
				else:
					force = True

		return force, args

	@override
	def Main(self, argv: str) -> int:
		"""エントリーポイント

		Args:
			argv: コマンドライン引数
		"""
		force, args = self.parse_args(argv)
		for tag, target in args:
			self.make_asset(tag, target, force)

		return 0

	def make_asset(self, tag: str, target: str, force: bool) -> None:
		"""アセット生成

		Args:
			tag: モジュールタグ
			target: 処理対象(アセット名 or all)
			force: True = 強制実行
		"""
		maker = AssetMakerFactory.create(tag, CP(self))
		if target == 'all':
			maker.on.create_all(force)
		else:
			maker.on.create(target, force)
