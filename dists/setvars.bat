@echo off
rem vim:set sw=4 ts=8 et fileencoding=utf8:
rem SPDX-License-Identifier: BSD-2-Clause
rem SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

if NOT exist "%~dp0\bin\learn_github.bat" (
    echo "%0: FAIL: %~dp0\bin\learn_github.bat: Not found" 1>&2
    exit /b 1
)

rem TODO: WARNING: У %LEARN_GITHUB_DIR% остаётся завершающий `\`

set LEARN_GITHUB_DIR=%~dp0
PATH %~dp0\bin;%PATH%
