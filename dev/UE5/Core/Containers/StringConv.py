# @see Engine/Source/Runtime/Core/Public/Containers/StringConv.h

from tranp.app.compatible.cpp.classes import uint8
from tranp.app.compatible.cpp.cvar import CRef

from compatible.error import Errors


def UTF8_TO_TCHAR(buff: CRef[list[uint8]]) -> str:
	"""UTF-8のバイト配列をUTF-16に変換

	Args:
		buff: UTF-8のバイト配列 ※実際はCP[char] @cpp
	Returns:
		UTF-16のバイト配列 ※実際はCP[TCHAR] @cpp
	Note:
		```
		* XXX Pythonで型ヒントを成り立たせるのは不可能であり、UTF-16のバイト配列を扱うことは無い
		* XXX トランスパイルによって書式を変換するため、Pythonでは使用禁止
		* XXX @see data/template/func_call/default.j2
		```
	"""
	raise Errors.Never
