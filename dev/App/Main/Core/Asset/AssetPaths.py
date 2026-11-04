from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.Paths import PackageName

from App.Main.Const.ProjectConst import ClassPrefixs, PackagePrefixs
from App.Main.Core.Lang.DSN.DSN import DSN
from compatible.error import Errors
from const.const_asset import AssetFormats


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class AssetPaths:
	"""ユーティリティー(アセットパス)"""

	# region 一般

	@classmethod
	def to_path(cls, domain: str, src: str) -> str:
		"""アセットソースパスをアセットパスに変換

		Args:
			domain: アセットドメイン
			src: アセットソースパス(ドメイン相対)
		Returns:
			アセットパス
		"""
		return AssetFormats.AssetPath.value.format(domain=domain, src=src)

	# endregion
	# region UEアセット

	@classmethod
	def pick_name(cls, path: str) -> str:
		"""アセットパスからアセット名を取得

		Args:
			path: アセットパス
		Returns:
			アセット名
		Raises:
			InvalidArguments: ドット/シャープを含むパスを指定
		"""
		if path.count('.') != 0 or path.count('#') != 0:
			raise Errors.InvalidArguments(cls.pick_name, path)

		return path[path.rfind('/') + 1:]

	@classmethod
	def to_ue_package_path(cls, path: str) -> str:
		"""アセットパスからパッケージパスに変換

		Args:
			path: アセットパス
		Returns:
			UEアセットパス(パッケージ)
		Note:
			相対パスの場合はプロジェクト用のパスと見做して接頭辞('/Game/')を補完
		"""
		if not path.startswith('/'):
			return DSN.joined(PackagePrefixs.Game, path, '/')
		else:
			return path

	@classmethod
	def to_ue_path(cls, path: str) -> str:
		"""アセットパスからUEアセットパスに変換

		Args:
			path: アセットパス
		Returns:
			UEアセットパス
		Note:
			相対パスの場合はプロジェクト用のパスと見做して接頭辞('/Game/')を補完
		"""
		begin_name = path.rfind('/')
		asset_name = path[begin_name + 1:] if begin_name > 0 else path
		ue_path = DSN.joined(path, asset_name)
		if not path.startswith('/'):
			return DSN.joined(PackagePrefixs.Game, ue_path, '/')
		else:
			return ue_path

	# endregion
	# region UEアセット/アセット生成

	@classmethod
	def to_ue_save_dir(cls, path: str) -> str:
		"""アセットパスから保存先のディレクトリーパスに変換 ※誤変換を避けるため、アセット生成以外で利用しないこと

		Args:
			path: アセットパス
		Returns:
			UEアセットパス(ディレクトリー)
		Raises:
			InvalidArguments: フルパスを指定
		"""
		if path.startswith('/'):
			raise Errors.InvalidArguments(cls.to_ue_save_dir, path)

		return DSN.joined(PackagePrefixs.Game, path[:path.rfind('/')], '/')

	@classmethod
	def to_ue_save_package_path(cls, path: str) -> str:
		"""アセットパスから保存先のパッケージパスに変換 ※誤変換を避けるため、アセット生成以外で利用しないこと

		Args:
			path: アセットパス
		Returns:
			UEアセットパス(パッケージ)
		Raises:
			InvalidArguments: フルパスを指定
		"""
		if path.startswith('/'):
			raise Errors.InvalidArguments(cls.to_ue_save_package_path, path)

		return DSN.joined(PackagePrefixs.Game, path, '/')

	@classmethod
	def to_ue_save_filepath(cls, ue_path: str) -> str:
		"""UEアセットパス(パッケージ)から保存先のファイルパスに変換 ※誤変換を避けるため、アセット生成以外で利用しないこと

		Args:
			ue_path: UEアセットパス(パッケージ)
		Returns:
			ファイルパス
		Raises:
			InvalidArguments: 不正なパスを指定
		"""
		if not ue_path.startswith(PackagePrefixs.Game):
			raise Errors.InvalidArguments(cls.to_ue_save_filepath, ue_path)

		return PackageName.LongPackageNameToFilename(ue_path, PackageName.GetAssetPackageExtension())

	# endregion
	# region マスター

	@classmethod
	def to_master_internal(cls, domain: str, src: str) -> str:
		"""アセットソースパスをアセットパス(マスター/内部)に変換

		Args:
			domain: アセットドメイン
			src: アセットソースパス(ドメイン相対)
		Returns:
			アセットパス(マスター/内部)
		"""
		return AssetFormats.InternalPath.value.format(domain=domain, src=src)

	@classmethod
	def to_master_filepath(cls, path: str) -> str:
		"""アセットパスからファイルパスに変換(マスター)

		Args:
			path: アセットパス
		Returns:
			ファイルパス(マスター)
		"""
		return AssetFormats.MasterFilepath.value.format(path=path)

	# endregion
