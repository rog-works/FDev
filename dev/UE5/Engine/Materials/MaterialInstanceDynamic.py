# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialInstanceDynamic.h

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Math.Color import LinearColor
from UE5.Core.Math.MathFwd import Vector
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.Object import NewObject, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, UFUNCTION, BlueprintCallable, BlueprintType
from UE5.Engine.Engine.Texture import Texture
from UE5.Engine.Materials.Material import MaterialInterface


@Embed.alias('U', prefix=True)
@UCLASS(BlueprintType)
class MaterialInstanceDynamic(MaterialInterface):
	"""マテリアルダイナミックインスタンス"""

	scalars: dict[str, float]
	vectors: dict[str, LinearColor]
	textures: dict[str, CP[Texture]]

	def __init__(self) -> None:
		super().__init__()
		# @python
		self.scalars = {}
		self.vectors = {}
		self.textures = {}

	@classmethod
	def Create(cls, parent: CP[MaterialInterface], outer: CP[UObject]) -> 'CP[MaterialInstanceDynamic]':
		"""マテリアルを基にインスタンスを生成

		Args:
			parent: マテリアル(基)
			outer: 管理オブジェクト
		Returns:
			インスタンス
		"""
		return NewObject(cls, outer)

	@UFUNCTION(BlueprintCallable)
	def K2_GetScalarParameterValue(self, name: Name | str) -> float:
		"""Returns: 値"""
		return self.scalars[name if isinstance(name, str) else name.ToString()]

	@UFUNCTION(BlueprintCallable)
	def SetScalarParameterValue(self, name: Name | str, value: float) -> None:
		"""Args: name: パラメーター名, value: 値"""
		self.scalars[name if isinstance(name, str) else name.ToString()] = value

	@UFUNCTION(BlueprintCallable)
	def K2_GetVectorParameterValue(self, name: Name | str) -> LinearColor:
		"""Returns: 値"""
		return self.vectors[name if isinstance(name, str) else name.ToString()]

	@UFUNCTION(BlueprintCallable)
	def SetVectorParameterValue(self, name: Name | str, value: Vector | LinearColor) -> None:
		"""Args: name: パラメーター名, value: 値"""
		if isinstance(value, Vector):
			self.vectors[name if isinstance(name, str) else name.ToString()] = LinearColor(value.X, value.Y, value.Z, 1.0)
		else:
			self.vectors[name if isinstance(name, str) else name.ToString()] = LinearColor(value.R, value.G, value.B, value.A)

	@UFUNCTION(BlueprintCallable)
	def K2_GetTextureParameterValue(self, name: Name | str) -> CP[Texture]:
		"""Returns: 値"""
		return self.textures[name if isinstance(name, str) else name.ToString()]

	@UFUNCTION(BlueprintCallable)
	def SetTextureParameterValue(self, name: Name | str, value: CP[Texture]) -> None:
		"""Args: name: パラメーター名, value: 値"""
		self.textures[name if isinstance(name, str) else name.ToString()] = value
