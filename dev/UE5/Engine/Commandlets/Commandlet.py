# @see Engine/Source/Runtime/Engine/Classes/Commandlets/Commandlet.h

from tranp.app.compatible.python.embed import Embed
from UE5.CoreUObject.UObject.Object import UObject
from UE5.CoreUObject.UObject.ObjectMacros import UCLASS


@Embed.alias('U', prefix=True)
@UCLASS()
class Commandlet(UObject):
	"""コマンドランナー(基底)

	Note:
		命名規則: 派生クラスは`XxxCommandlet`と言う名称にすること
	"""

	@Embed.allow_override
	def Main(self, argv: str) -> int:
		"""エントリーポイント

		Args:
			argv: コマンドライン引数
		"""
		...
