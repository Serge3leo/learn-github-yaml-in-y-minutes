@echo off
rem vim:set sw=4 ts=8 et fileencoding=utf8:
rem SPDX-License-Identifier: BSD-2-Clause
rem SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

if NOT "%LEARN_GITHUB_DIR%bin\"=="%~dp0" (
    echo "%0: FAIL, LEARN_GITHUB_DIR=%LEARN_GITHUB_DIR%" 1>&2
    exit /b 1
)
echo "Хорь, LEARN_GITHUB_DIR=%LEARN_GITHUB_DIR%" 1>&2
exit /b 0
