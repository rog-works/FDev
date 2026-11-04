// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class FDev : ModuleRules
{
	public FDev(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicIncludePaths.Add(System.IO.Path.Combine(ModuleDirectory, "Public"));

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core", "CoreUObject", "Engine",
		});

		// シャドーイングのエラーを抑制
		CppCompileWarningSettings.ShadowVariableWarningLevel = WarningLevel.Off;
		// 例外の有効化
		this.bEnableExceptions = true;
	}
}
