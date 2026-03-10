#!/usr/bin/env python3
# vim:set sw=4 ts=8 et fileencoding=utf8:
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Сергей Леонтьев (leo@sai.msu.ru)

r"""
Регистрация изменений переменных окружения, PATH, получение $GITHUB_ENV и
$GITHUB_PATH

Использование:
    python trace_env_path.py "${{ ... }}\setvars.bat"
или
    python trace_env_path.py "bash -c '. ${{ ... }}/setvars.sh'"

TODO:
    python pyprintenv.py [VARIABLE]...
    python pyprintenv.py [-0|--null] [VARIABLE]...
    python pyprintenv.py --trace=<cmd>
"""

__date__ = "10 March 2026"
__version__ = "$Revision: 0 $"
__author__ = ("Сергей Леонтьев (leo@sai.msu.ru)")

import os
import platform
import re
import sys
import uuid

def printenv(null: bool, variables: list[str] = None) -> None:
    if not variables:
        variables = os.environ.keys()
    # sys.stdout.reconfigure(encoding='utf-8')
    end = '\0' if null else '\n'
    for v in variables:
        if v in os.environ:
            print(f"{v}={os.environ[v]}", end=end)

def trace(cmd: str, github_env: str = None, github_path: str = None,
          shell: str = None) -> None:
    if not github_env:
        github_env = os.environ.get("GITHUB_ENV", "/dev/stdout")
    if not github_path:
        github_path = os.environ.get("GITHUB_PATH", "/dev/stdout")
    dlmt = uuid.uuid4()
    if "Windows" == platform.system():
        cmd = f"@{cmd} && @python pyprintenv.py -0"
        pd = ";"
        ign = set()
    else:
        if not shell:
            cmd = f"{cmd} && env -0"
        else:
            cmd = f"{shell} -c '{cmd} && env -0'"
        pd = ":"
        ign = {"SHLVL", "_"}
    with os.popen(cmd) as f, \
         open(github_env, mode="a") as fe, \
         open(github_path, mode="a") as fp:
        for l in f.buffer.read().split(b"\0"):
            if not l:
                # print("Empty: {l=}")
                continue
            m = re.match(r"([^=]*)=(.*)$", l.decode(), flags=re.DOTALL)
            assert m, f"pm.py: Don't match VAR=VALUE {l, l.decode(), m=}"
            if "path" == m.group(1).lower():
                o = (os.environ["PATH"] if "PATH" in os.environ else
                     os.environ["Path"])
                n = m.group(2)
                oi, ni = len(o), len(n)
                while (oi and ni and o[oi:].lower() == n[ni:].lower()):
                    # print(f"{oi, ni, o[oi:], n[ni:]=}")
                    oi = max(0, o.rfind(pd, 0, oi))
                    np = ni
                    ni = max(0, n.rfind(pd, 0, np))
                if ni:
                    assert -1 == np or len(n) == np or n[np] == pd
                    # TODO в случае, если PATH изменился с конца, он дублируется
                    for d in n[:(np if 0 < np else len(n))].split(pd)[::-1]:
                        print(d, file=fp)
            elif (m.group(1) not in os.environ or
                  os.environ[m.group(1)].lower() != m.group(2).lower()
                 ) and m.group(1) not in ign:
                if '\n' not in m.group(2):
                    print(f"{m.group(1)}={m.group(2)}", file=fe)
                else:
                    print(f"{m.group(1)}<<{dlmt}\n{m.group(2)}\n{dlmt}", file=fe)

if __name__ == '__main__':
    import argparse
    import locale

    # TODO Перезапуск в "Python UTF-8 Mode"
    if "UTF-8" != locale.getencoding():
        sys.argv.insert(0, "utf8")
        sys.argv.insert(0, "-X")
        os.execvp(sys.executable, sys.argv)
    assert "UTF-8" == locale.getencoding(), "Must start with `-X utf8`"

    parser = argparse.ArgumentParser()
    parser.add_argument("variables", nargs='*',
                        help="Environment variables", default=None)
    parser.add_argument("-0", "--null", action='store_true',
                        help="End each output line with NUL, not newline")
    parser.add_argument("--trace",
                        help="Command for trace")
    if "Windows" != platform.system():
        parser.add_argument("--shell",
                            help="Shell to start cmd")
    parser.add_argument("--github-env",
                        help="GITHUB_ENV file")
    parser.add_argument("--github-path",
                        help="GITHUB_PATH file")
    args = parser.parse_args()
    if args.trace:
        trace(args.trace, args.github_env, args.github_path, args.shell)
    else:
        printenv(args.null, args.variables)
