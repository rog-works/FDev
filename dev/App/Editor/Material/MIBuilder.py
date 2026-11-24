from tranp.app.compatible.cpp.cvar import CP
from UE5.Core.Math.Color import LinearColor
from UE5.Core.Misc.Guid import Guid
from UE5.Core.UObject.NameTypes import Name
from UE5.Engine.Engine.Texture import Texture
from UE5.Engine.Materials.MaterialInstanceConstant import MaterialInstanceConstant, MaterialParameterInfo, MaterialUpdateContext, StaticSwitchParameter

from App.Main.Core.Asset.AssetPaths import AssetPaths
from App.Main.Core.Asset.Assets import Assets
from App.Main.Core.Lang.Convertion import safe_addr
from App.Main.Core.Lang.Json.Json import Json
from compatible.error import Errors
from const.const_asset import AssetDomains


class MIBuilder:
	"""アセットビルダー(マテリアルインスタンス)"""

	__assets: CP[Assets] | None
	__mi: CP[MaterialInstanceConstant] | None
	bools: dict[str, bool]
	floats: dict[str, float]
	vectors: dict[str, LinearColor]
	textures: dict[str, CP[Texture]]

	def __init__(self, assets: CP[Assets], mi: CP[MaterialInstanceConstant]) -> None:
		"""インスタンスを生成

		Args:
			assets: アセットマネージャー
			mi: マテリアルインスタンス
		"""
		self.__assets = assets
		self.__mi = mi
		self.bools = {}
		self.floats = {}
		self.vectors = {}
		self.textures = {}

	@property
	def assets(self) -> CP[Assets]:
		"""Returns: アセットマネージャー"""
		return safe_addr(self.__assets)

	@property
	def mi(self) -> CP[MaterialInstanceConstant]:
		"""Returns: マテリアルインスタンス"""
		return safe_addr(self.__mi)

	def a_bool(self, name: str, enable: bool) -> None:
		"""Args: name: パラメーター名, enable: True = 有効"""
		self.bools[name] = enable

	def a_float(self, name: str, value: float) -> None:
		"""Args: name: パラメーター名, value: 値"""
		self.floats[name] = value

	def a_vector(self, name: str, x: float, y: float, z: float) -> None:
		"""Args: name: パラメーター名, x: X, y: Y, z: Z"""
		self.vectors[name] = LinearColor(x, y, z, 1.0)

	def a_texture(self, name: str, src: str) -> None:
		"""Args: name: パラメーター名, src: 画像ソースパス"""
		self.textures[name] = self.assets.on.asset_of(Texture, AssetPaths.to_path(AssetDomains.Texture.value, src))

	def build(self) -> None:
		"""パラメーターを構築"""
		# パラメーターの削除
		self.mi.on.ClearParameterValuesEditorOnly()
		static_params = self.mi.on.GetStaticParameters()
		static_collection = static_params.GetRuntime()
		static_collection.on.Empty()
		static_params.Empty()

		# パラメーターを構築
		for key, value in self.floats.items():
			self.mi.on.SetScalarParameterValueEditorOnly(MaterialParameterInfo(Name(key)), value)

		for key, vector in self.vectors.items():
			self.mi.on.SetVectorParameterValueEditorOnly(MaterialParameterInfo(Name(key)), vector)

		for key, texture in self.textures.items():
			self.mi.on.SetTextureParameterValueEditorOnly(MaterialParameterInfo(Name(key)), texture)

		for key, enable in self.bools.items():
			bool_param = StaticSwitchParameter(MaterialParameterInfo(Name(key)), enable, True, Guid.NewGuid())
			static_collection.on.StaticSwitchParameters.append(bool_param)

		context = MaterialUpdateContext()
		self.mi.on.UpdateStaticPermutation(static_params, CP(context))


class MIBuildCommandRunner:
	"""マテリアルインスタンスビルドコマンドランナー"""

	@classmethod
	def via_src(cls, data: Json) -> str:
		"""生成元のマテリアルのソースパスを取得

		Args:
			data: コマンドデータ
		Returns:
			アセットソースパス(ドメイン相対/マテリアル)
		"""
		return data['via'].as_string

	@classmethod
	def run(cls, builder: CP[MIBuilder], data: Json) -> None:
		"""実行処理
		
		Args:
			builder: マテリアルインスタンスビルダー
			data: コマンドデータ
		"""
		exports = data['exports']
		for key in exports.keys:
			com = exports[key]
			if com.is_bool:
				builder.on.a_bool(key, com.as_bool)
			elif com.is_float:
				builder.on.a_float(key, com.as_float)
			elif com.is_array:
				builder.on.a_vector(key, com.at(0).as_float, com.at(1).as_float, com.at(2).as_float)
			elif com.is_string:
				builder.on.a_texture(key, com.as_string)
			else:
				raise Errors.Never(cls.run, key, com)

		builder.on.build()
