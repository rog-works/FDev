// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class FDevEditor : ModuleRules
{
	public FDevEditor(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicIncludePaths.Add(System.IO.Path.Combine(ModuleDirectory, "Public"));

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core", "CoreUObject", "Engine",
			"FDev",
		});

		// シャドーイングのエラーを抑制
		CppCompileWarningSettings.ShadowVariableWarningLevel = WarningLevel.Off;
		// 例外の有効化
		this.bEnableExceptions = true;
	}
}
