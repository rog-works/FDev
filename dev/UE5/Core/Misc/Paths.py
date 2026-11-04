from os import path as os_path

from tranp.app.compatible.python.embed import Embed

from App.Main.Const.ProjectConst import PackagePrefixs
from helper.env.directories import project_dir


@Embed.alias('F', prefix=True)
class Paths:
	"""ファイルパスマネージャー"""

	@classmethod
	def FileExists(cls, filepath: str) -> bool:
		"""ファイルが存在するか判定

		Args:
			filepath: ファイルパス
		Returns:
			True = 存在
		"""
		return os_path.exists(filepath)

	@classmethod
	def ProjectDir(cls) -> str:
		"""プロジェクトルートの絶対パスを取得

		Returns:
			プロジェクトルート
		"""
		return project_dir()

	@classmethod
	def ProjectContentDir(cls) -> str:
		"""Contentフォルダの絶対パスを取得

		Returns:
			Contentフォルダのパス
		"""
		return os_path.join(cls.ProjectDir(), 'Content')

	@classmethod
	def Combine(cls, *elem: str) -> str:
		"""パスを結合

		Args:
			*elem: 要素リスト
		Returns:
			結合後のパス
		"""
		return os_path.join(*elem)


@Embed.alias('F', prefix=True)
class PackageName:
	"""パッケージの名前関連ユーティリティー Note: @see Engine/Source/Runtime/CoreUObject/Public/Misc/PackageName.h"""

	@classmethod
	def GetAssetPackageExtension(cls) -> str:
		"""Returns: アセットの拡張子"""
		return '.uasset'

	@classmethod
	def LongPackageNameToFilename(cls, package_path: str, asset_ext: str) -> str:
		"""パッケージパスからファイルパスに変換

		Args:
			package_path: パッケージパス
			asset_ext: アセットの拡張子
		Returns:
			ファイルパス
		"""
		normalize_path = package_path.replace(f'{PackagePrefixs.Game}/', '').replace('/', os_path.sep)
		filepath = '{path}{ext}'.format(path=normalize_path, ext=asset_ext)
		return os_path.join(Paths.ProjectContentDir(), filepath)

	@classmethod
	def DoesPackageExist(cls, package_path: str) -> bool:
		"""パッケージパスに対応するアセットが存在するか判定

		Args:
			package_path: パッケージパス
		Returns:
			True = 存在
		"""
		filepath = cls.LongPackageNameToFilename(package_path, cls.GetAssetPackageExtension())
		return os_path.exists(filepath)
