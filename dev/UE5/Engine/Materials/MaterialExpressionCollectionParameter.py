# @see Engine/Source/Runtime/Engine/Public/Materials/MaterialParameterCollection.h

from tranp.app.compatible.python.embed import Embed
from UE5.Core.Misc.Guid import Guid
from UE5.Core.Templates.SharedPointer import ObjectPtr
from UE5.Core.UObject.NameTypes import Name
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS
from UE5.Engine.Materials.MaterialExpression import MaterialExpression
from UE5.Engine.Materials.MaterialParameterCollection import MaterialParameterCollection


@Embed.alias('U', prefix=True)
@UCLASS()
class MaterialExpressionCollectionParameter(MaterialExpression):
	"""マテリアルパラメーターコレクション"""

	Collection: ObjectPtr[MaterialParameterCollection]
	ParameterName: Name
	ParameterId: Guid

	def __init__(self) -> None:
		"""インスタンスを生成"""
		super().__init__()
		self.Collection = ObjectPtr[MaterialParameterCollection]()
		self.ParameterName = Name('')
		self.ParameterId = Guid()

	@Embed.python
	def __str__(self) -> str:
		"""文字列表現"""
		return f'<const_by: name: "{self.ParameterName}" collection: {"ok" if self.Collection.Get else "ng"}>'
