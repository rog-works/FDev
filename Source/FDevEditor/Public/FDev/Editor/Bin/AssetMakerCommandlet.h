// @tranp.meta: {"version":"0.9.19","module":{"hash":"51574ff560a4d9a9de4e3523977c36de","path":"FDev.Editor.Bin.AssetMakerCommandlet"},"transpiler":{"version":"0.9.6","module":"tranp.app.implements.cpp.transpiler.py2cpp.Py2Cpp"}}
#pragma once
#include "UObject/ObjectMacros.h"
#include "Commandlets/Commandlet.h"
#include "FDev/Editor/Asset/AssetMakerFactory.h"
#include "FDev/Main/Const/ProjectConst.h"
#include "FDev/Main/Core/Core.h"
#include "AssetMakerCommandlet.generated.h"
// #include "enum.h"
// #include "typing.h"
// #include "tranp/app/compatible/cpp/cvar.h"
// #include "tranp/app/compatible/python/embed.h"
// enum ArgKeys
/**
 * コマンドランナー(アセット生成)
 */
UCLASS()
class FDEVEDITOR_API UFDevAssetMakerCommandlet : public UCommandlet {
	GENERATED_BODY()
	public:
	/**
	 * コマンドライン引数をパース
	 * @param argv コマンドライン引数
	 * @return (True = 強制実行, 引数一覧)
	 * @note
	 * ```
	 * ### 書式
	 * * 全文: '{実行ファイルパス}\\UnrealEditor-Cmd.exe {プロジェクトパス}.uproject -run=AssetMakerCommandlet -Maker="{メーカータグ}: {ソースパス or all}, ..."'
	 * * サンプル(Maker): -Maker="mfs, force"
	 * ```
	 */
	TTuple<bool, TArray<TTuple<FString, FString>>> parse_args(const FString& argv) {
		TArray<FString> blocks = FDevString::split(argv, "-");
		blocks.RemoveAt(0);
		TArray<TTuple<FString, FString>> args = {};
		bool force = false;
		for (auto& block : blocks) {
			TArray<FString> arg_pair = FDevString::split(FDevString::trim(block, ' '), "=");
			if (!(arg_pair.Num() == 2 && arg_pair[0] == "Maker")) {
				continue;
			}
			FString arg_value = arg_pair[1];
			// XXX 空白が含まれない場合、二重引用符が削除されてしまう仕様への対処
			if (arg_value.StartsWith("\"") && arg_value.EndsWith("\"")) {
				arg_value = arg_value.Mid(1, arg_value.Len() - 1 - (1));
			}
			TArray<FString> pairs = FDevString::split(arg_value, ", ");
			for (auto& pair : pairs) {
				TArray<FString> elems = FDevString::split(pair, ": ");
				if (elems.Num() == 2) {
					args.Add({elems[0], elems[1]});
				} else if (elems[0] != "force") {
					args.Add({elems[0], "all"});
				} else {
					force = true;
				}
			}
		}
		return {force, args};
	}
	public:
	/**
	 * エントリーポイント
	 * @param argv コマンドライン引数
	 */
	int Main(const FString& argv) override {
		auto [force, args] = this->parse_args(argv);
		for (auto& [tag, target] : args) {
			this->make_asset(tag, target, force);
		}
		return 0;
	}
	public:
	/**
	 * アセット生成
	 * @param tag モジュールタグ
	 * @param target 処理対象(アセット名 or all)
	 * @param force True = 強制実行
	 */
	void make_asset(const FString& tag, const FString& target, bool force) {
		UFDevAssetMaker* maker = UFDevAssetMakerFactory::create(tag, (this));
		if (target == "all") {
			maker->create_all(force);
		} else {
			maker->create(target, force);
		}
	}
};
