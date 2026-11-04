from typing import Annotated

from tranp.app.compatible.cpp.cvar import CP, CRef
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Math.Color import LinearColor
from UE5.Core.Misc.Guid import Guid
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.Object import GenStruct, UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS, USTRUCT
from UE5.Engine.Engine.Texture import Texture
from UE5.Engine.Materials.Material import MaterialInterface


@Embed.alias('F', prefix=True)
class MaterialParameterInfo:
	"""パラメーター情報 @see Engine/Source/Runtime/Engine/Public/MaterialTypes.h"""

	def __init__(self, name: Name) -> None:
		"""インスタンスを生成

		Args:
			name: パラメーター名
		"""
		...


@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class StaticSwitchParameter(GenStruct):
	"""静的パラメーター(StaticBool) Note: @see Engine/Source/Runtime/Engine/Public/StaticParameterSet.h"""

	def __init__(self, info: Annotated[MaterialParameterInfo, Embed.immutable], enable: bool, updated: bool, guid: Guid) -> None:
		"""インスタンスを生成

		Args:
			info: パラメーター情報 @immutable
			enable: True = 有効
			updated: True = 上書き
			guid: UUID
		"""
		...


@Embed.alias('F', prefix=True)
@Embed.ignore(GenStruct)
@USTRUCT()
class StaticParameterSetRuntimeData(GenStruct):
	"""静的パラメーターコレクション(ランタイム) Note: @see Engine/Source/Runtime/Engine/Public/StaticParameterSet.h"""

	StaticSwitchParameters: list[StaticSwitchParameter]

	def __init__(self) -> None:
		"""インスタンスを生成"""
		self.StaticSwitchParameters = []

	def Empty(self) -> None:
		"""パラメーターを全て削除"""
		...


@Embed.alias('F', prefix=True)
class MaterialUpdateContext:
	"""更新コンテキスト Note: @see Engine/Source/Runtime/Engine/Public/MaterialShared.h"""
	...


@Embed.alias('F', prefix=True)
@USTRUCT()
class StaticParameterSet(UObject):
	"""静的パラメーターコレクション Note: @see MaterialInstance.h"""

	def GetRuntime(self) -> CRef[StaticParameterSetRuntimeData]:
		"""インスタンスを生成"""
		return CRef(StaticParameterSetRuntimeData())

	def Empty(self) -> None:
		"""パラメーターを全て削除"""
		...


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialInstanceConstant(MaterialInterface):
	"""マテリアルインスタンス"""

	@Embed.pure
	def GetStaticParameters(self) -> StaticParameterSet:
		"""静的パラメーターコレクションを取得

		Note:
			```
			* 戻り値を直接上書きすることはできないため、一旦ローカル変数にコピーし、UpdateStaticPermutationに渡すことで更新
			@see Engine/Public/Materials/MaterialInstance.h
			```
		Returns:
			静的パラメーターコレクション
		"""
		return StaticParameterSet()
	
	def UpdateStaticPermutation(self, static_params: Annotated[StaticParameterSet, Embed.immutable], context: CP[MaterialUpdateContext]) -> None:
		"""静的パラメーターコレクションを更新

		Args:
			static_params: 静的パラメーターコレクション @immutable
			context: 更新コンテキスト
		Note:
			内部実装がRHI_APIに依存しているため、依存モジュールに`RHI`の追加が必要
		"""
		...

	def SetVectorParameterValueEditorOnly(self, info: Annotated[MaterialParameterInfo, Embed.immutable], value: LinearColor) -> None:
		"""Args: into: パラメーター情報 @immutable, value: 値"""
		...

	def SetScalarParameterValueEditorOnly(self, info: Annotated[MaterialParameterInfo, Embed.immutable], value: float) -> None:
		"""Args: into: パラメーター情報 @immutable, value: 値"""
		...

	def SetTextureParameterValueEditorOnly(self, info: Annotated[MaterialParameterInfo, Embed.immutable], value: CP[Texture]) -> None:
		"""Args: into: パラメーター情報 @immutable, value: 値"""
		...

	def ClearParameterValuesEditorOnly(self) -> None:
		"""動的パラメーター群を削除"""
		...
