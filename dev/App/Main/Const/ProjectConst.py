from enum import Enum
from typing import ClassVar

from tranp.app.compatible.python.embed import Embed


@Embed.python
class ClassPrefixs(Enum):
	"""クラス名の接頭辞

	Attributes:
		General: 全クラス共通の接頭辞
		UObject: UObject系クラスの接頭辞
		Struct: UE公開用の構造体の接頭辞
		Enum: UE公開用のEnumの接頭辞
		Actor: Actor系クラスの接頭辞
		Slate: Slate系クラスの接頭辞
		Template: ジェネリック系クラスの接頭辞
	"""
	General = 'FDev'
	UObject = 'U' + General
	Struct = 'F' + General
	Enum = 'E' + General
	Actor = 'A' + General
	Slate = 'S' + General
	Template = 'T' + General


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class ProjectConst:
	"""アプリケーション定数

	Attributes:
		Name: プロジェクト名
	"""
	Name: ClassVar = 'FDev'


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class PackagePrefixs:
	"""パッケージ接頭辞

	Attributes:
		Script: C++パッケージの接頭辞
		Game: アセットパッケージの接頭辞
	"""
	Script: ClassVar = '/Script'
	Game: ClassVar = '/Game'
