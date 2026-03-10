@echo off
rem vim:set sw=4 ts=8 et fileencoding=utf8:
rem SPDX-License-Identifier: BSD-2-Clause
rem SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

if NOT exist "%~dp0\bin\learn_github.bat" (
    echo "%0: FAIL: %~dp0\bin\learn_github.bat: Not found" 1>&2
    exit /b 1
)

set _LEARN_GITHUB=%~dp0
set LEARN_GITHUB=%_LEARN_GITHUB:~0,-1%
set _LEARN_GITHUB=
PATH %~dp0\bin;%PATH%
PATH c:\none;%PATH%
rem TODO LEARN_GITHUB_ML
