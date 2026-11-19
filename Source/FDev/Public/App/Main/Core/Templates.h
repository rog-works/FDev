/**
 * メソッド抽出テンプレート
 * 
 * @example
 * template<typename T, typename ...Args>
 * void bind(T* obj, const PluckMethod<T, void, Args...>::method& method) { ... }
 * 
 * bind(&a_obj, &A::func);
 */
template<typename T, typename TReturn, typename... TArgs>
struct PluckMethod {
	typedef TReturn (T::*method) (TArgs...);
};
