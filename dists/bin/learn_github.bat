@echo off
rem vim:set sw=4 ts=8 et fileencoding=utf8:
rem SPDX-License-Identifier: BSD-2-Clause
rem SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

echo "~dp0=%~dp0"
echo "%LEARN_GITHUB%\bin\"
echo "LEARN_GITHUB=%LEARN_GITHUB%"
if NOT "%LEARN_GITHUB%\bin\"=="%~dp0" (
    echo "%0: FAIL, LEARN_GITHUB=%LEARN_GITHUB%" 1>&2
    exit /b 1
)
echo "Хорь, LEARN_GITHUB=%LEARN_GITHUB%" 1>&2
exit /b 0
