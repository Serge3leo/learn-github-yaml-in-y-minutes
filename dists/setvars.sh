#!
# vim:set sw=4 ts=8 fileencoding=utf8:
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

r=$(realpath "${BASH_ARGV[0]}")
d=$(dirname "$r")
[ -d "$d/bin" ] || {
    printf "%s: FAIL: %s: не найден\n" "$0" "$d/bin" 1>&2
    return 1
}
LEARN_GITHUB="$d" ; export LEARN_GITHUB
PATH="$d/bin:$PATH"
return 0
