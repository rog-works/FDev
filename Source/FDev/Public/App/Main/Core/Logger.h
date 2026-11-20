#pragma once

#include "Logs.h"

/** ログカテゴリー(アプリケーション用) */
FDEV_API DECLARE_LOG_CATEGORY_EXTERN(LogApp, Log, All);

#define CORE_LOGGER_INFO(flag, format, ...) if (Logs::ok(flag)) { UE_LOG(LogApp, Display, TEXT(format), ##__VA_ARGS__) }
#define CORE_LOGGER_WARNING(format, ...) UE_LOG(LogApp, Warning, TEXT(format), ##__VA_ARGS__)

#if WITH_EDITOR
#define CORE_LOGGER_ERROR(format, ...) UE_LOG(LogApp, Error, TEXT(format), ##__VA_ARGS__)
#else
#define CORE_LOGGER_ERROR(format, ...) UE_LOG(LogApp, Fatal, TEXT(format), ##__VA_ARGS__)
#endif

#ifdef UE_BUILD_DEVELOPMENT
	/** デバッグログ出力フラグ */
	#define CORE_LOGGING_DEBUG 1
#elif _DEBUG
	/** デバッグログ出力フラグ */
	#define CORE_LOGGING_DEBUG 1
#endif

#ifdef CORE_LOGGING_DEBUG
	/**
	 * ログ出力(INFO)
	 *
	 * @param flag 出力フラグ
	 * @param format 出力フォーマット
	 * @param args 可変長引数
	 */
	#define log_info(flag, format, ...) CORE_LOGGER_INFO(flag, format, ##__VA_ARGS__)

	/**
	 * ログ出力(WARNING)
	 *
	 * @param format 出力フォーマット
	 * @param args 可変長引数
	 */
	#define log_warning(format, ...) CORE_LOGGER_WARNING(format, ##__VA_ARGS__)
#else
	/**
	 * ログ出力(INFO)
	 *
	 * @param flag 出力フラグ
	 * @param format 出力フォーマット
	 * @param args 可変長引数
	 */
	#define log_info(flag, format, ...)

	/**
	 * ログ出力(WARNING)
	 *
	 * @param format 出力フォーマット
	 * @param args 可変長引数
	 */
	#define log_warning(format, ...)
#endif

/**
 * ログ出力(ERROR)
 *
 * @param format 出力フォーマット
 * @param args 可変長引数
 */
#define log_error(format, ...) CORE_LOGGER_ERROR(format, ##__VA_ARGS__)

/**
 * ログ出力(ゲーム画面に出力)
 *
 * @param format 出力フォーマット
 * @param args 可変長引数
 */
#define CORE_LOGGER_SCREEN(format, color, ...) if (GEngine) { GEngine->AddOnScreenDebugMessage(-1, 15.f, color, FString::Printf(TEXT(format), ##__VA_ARGS__)); }
#define CORE_LOGGER_INFO_SCREEN(format, ...) CORE_LOGGER_SCREEN(format, FColor::White, ##__VA_ARGS__)
#define CORE_LOGGER_WARNING_SCREEN(format, ...) CORE_LOGGER_SCREEN(format, FColor::Yellow, ##__VA_ARGS__)
#define CORE_LOGGER_ERROR_SCREEN(format, ...) CORE_LOGGER_SCREEN(format, FColor::Purple, ##__VA_ARGS__)

/**
 * ログ出力(INFO)
 *
 * @param format 出力フォーマット
 * @param args 可変長引数
 */
#define log_info_screen(format, ...) log_info(format, ##__VA_ARGS__); CORE_LOGGER_INFO_SCREEN(format, ##__VA_ARGS__)

/**
 * ログ出力(WARNING)
 *
 * @param format 出力フォーマット
 * @param args 可変長引数
 */
#define log_warning_screen(format, ...) log_warning(format, ##__VA_ARGS__); CORE_LOGGER_WARNING_SCREEN(format, ##__VA_ARGS__)

/**
 * ログ出力(ERROR)
 *
 * @param format 出力フォーマット
 * @param args 可変長引数
 */
#define log_error_screen(format, ...) log_error(format, ##__VA_ARGS__);  CORE_LOGGER_ERROR_SCREEN(format, ##__VA_ARGS__)
