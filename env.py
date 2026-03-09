#!/usr/bin/env python3
# vim:set sw=4 ts=8 et fileencoding=utf8:
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

if __name__ == '__main__':
    import os
    import sys

    end = '\n'
    if 1 < len(sys.argv) and "-0" == sys.argv[1]:
        end = '\0'
        del sys.argv[1]
    for k, v in os.environ.items():
        print(f"{k}={v}", end=end)
