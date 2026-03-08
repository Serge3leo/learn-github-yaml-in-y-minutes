#!
# vim:set sw=4 ts=8 fileencoding=utf8:
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

set -e

r=$(realpath "$0")
d=$(dirname "$r")
[ -d "$d/bin" ] || {
    printf "%s: FAIL: %s: не найден\n" "$0" "$d/bin" 1>&2
    exit 1
}
LEARN_GITHUB_DIR="$d"
PATH="$d/bin:$PATH"
exit 0
