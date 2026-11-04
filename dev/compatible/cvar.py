from typing import Any, override

from tranp.app.compatible.cpp.cvar import CP, CSP, T_co, T_New


class AtomicCSP(CSP[T_co]):
	"""C++型変数の互換クラス(共有ポインター/強スレッド整合性)

	Note:
		```
		### 書式変換
		* 型宣言: `TSharedPtr<${型名}, ESPMode::ThreadSafe>`
		* 生成: `MakeShared<${関数コール}, ESPMode::ThreadSafe>`
		@see data/template/func_call/cvar_new_smart.j2
		@see data/template/func_call/cvar_new_smart_list.j2
		@see data/template/func_call/cvar_smart_empty.j2
		@see data/template/type/custom_type.j2
		@see config.yml
		### 課題
		XXX CSPを返却してしまうためoverride
		```
	"""

	@classmethod
	@override
	def empty(cls) -> 'AtomicCSP[T_co] | None':
		return AtomicCSP(None)

	@classmethod
	@override
	def new(cls, origin: T_New) -> 'AtomicCSP[T_New]':
		return AtomicCSP(CP(origin))


def unpack_shared(cvar_type: type[CSP[Any]]) -> type[CSP]:
	"""共有ポインター型からC++型を取得

	Args:
		cvar_type: 共有ポインター型
	Returns:
		C++型
	Note:
		```
		* isinstanceはサブクラスを判定できないが、C++上はただのアドレス型の比較になるため特に問題が無い
		* これに対応するため、Python上はC++型のみ評価することで、結果的に同等の条件になるようこじつける
		* 当然ながら、Python上はサブクラスを評価しない点に注意が必要
		@see data/template/func_call/generic_call.j2
		```
	Examples:
		```python
		if isinstance(var, unpack_shared(CSP[Var])): ...  # OK
		if isinstance(var, CSP[Var]): ...  # NG
		```
	"""
	return getattr(cvar_type, '__origin__')
