from typing import ClassVar


class ProjectConst:
	"""アプリケーション定数

	Attributes:
		Name: プロジェクト名
	"""
	Name: ClassVar = 'FDev'


class PackageConst:
	"""パッケージ定数

	Attributes:
		Script: C++パッケージの先頭パス
		Game: アセットパッケージの先頭パス
		App: アプリケーションのルートモジュールパス
		AppMain: アプリケーションのGameモジュールパス
	"""
	Script: ClassVar = '/Script'
	Game: ClassVar = '/Game'
	App: ClassVar = 'App'
	AppMain: ClassVar = 'App.Main'
