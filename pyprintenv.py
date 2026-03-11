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

import enum
import os
import platform
import re
import sys
import typing
import uuid

class OutputFormat(enum.Enum):
    NL = 1
    NUL = 2
    MULTILINE = 3

_dlmt = "ppe_" + str(uuid.uuid4())

def _str_variable(fmt: OutputFormat, variable: str, value: str) -> str:
    if fmt.NUL == fmt:
        return f"{variable}={value}\0"
    if '\n' in variable:  # TODO: А нужно ли проверять?
        raise ValueError(f"Multiline variable name: {variable=}")
    if fmt.NL == fmt or '\n' not in value:
        return f"{variable}={value}\n"
    if fmt.MULTILINE == fmt:
        return f"{variable}<<{_dlmt}\n{value}\n{_dlmt}\n"
    raise ValueError("Unknown format: {fmt=}")

def printenv(fmt: OutputFormat, variables: list[str] = None,
             encoding: str = None) -> None:
    if encoding:
        sys.stdout.reconfigure(encoding=encoding)  # TODO with/try
    if not variables:
        variables = os.environ.keys()
    for v in variables:
        if v in os.environ:
            print(_str_variable(fmt, v, os.environ[v]), end='')

def _open_env(file: str, env: str, **kwargs) -> typing.IO[typing.AnyStr]:
    if not file:
        if env not in os.environ:
            if 'encoding' in kwargs:
                sys.stdout.reconfigure(encoding=kwargs['encoding'])
            return sys.stdout
        file = os.environ[env]
    return open(file, **kwargs)

def trace(cmd: str, path: bool, encoding: str = None, shell: str = None,
          github_env: str = None, github_path: str = None) -> None:
    if "Windows" == platform.system():
        cmd = f"@{cmd} && @{sys.executable} pyprintenv.py -0 --encoding=utf-8"
        pd = ";"
        ign = set()
    else:
        if not shell:
            cmd = f"{cmd} && {sys.executable} pyprintenv.py -0 --encoding=utf-8"
        else:
            cmd = f"{shell} -c '{cmd} && {sys.executable} pyprintenv.py -0 --encoding=utf-8'"
        pd = ":"
        ign = {"SHLVL", "_"}
    with os.popen(cmd) as fi, \
         _open_env(github_env, "GITHUB_ENV", mode="a",
                   encoding=encoding) as fe, \
         _open_env(github_path, "GITHUB_PATH", mode="a",
                   encoding=encoding) as fp:
        for line in fi.buffer.read().split(b"\0"):
            if not line:
                # print("Empty: {line=}")
                continue
            m = re.match(r"([^=]*)=(.*)$",
                    line.decode(),  # TODO
                    flags=re.DOTALL)
            if not m:
                raise ValueError(
                        f"Don't match VAR=VALUE {line, line.decode(), m=}")
            if path and "path" == m.group(1).lower():
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
                        if '\n' in d:  # TODO: А нужно ли проверять?
                            raise ValueError(f"NewLine in PATH: {d=}")
                        print(d, file=fp)
            elif (m.group(1) not in os.environ or
                  os.environ[m.group(1)].lower() != m.group(2).lower()
                 ) and m.group(1) not in ign:
                print(_str_variable(OutputFormat.MULTILINE,
                                    m.group(1), m.group(2)), end='', file=fe)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("variables", nargs='*',
                        help="environment variables", default=None)
    parser.add_argument("-0", "--null", action='store_true',
                        help="end each output line with NUL, not newline")
    parser.add_argument("-g", "--github-multiline", action='store_true',
                        help="output multiline strings as GitHub Actions")
    parser.add_argument("--encoding",
                        help="output encoding (utf-8, ...)")
    parser.add_argument("--trace",
                        help="command to trace environment")
    parser.add_argument("--path", action='store_true',
                        help="store PATH separately, in GITHUB_PATH")
    parser.add_argument("--shell",
                        help=("shell to start cmd"
                              if "Windows" != platform.system()
                              else argparse.SUPPRESS))  # TODO
    parser.add_argument("--github-env",
                        help="GITHUB_ENV file name")
    parser.add_argument("--github-path",
                        help="GITHUB_PATH file name")
    args = parser.parse_args()
    if args.null and args.github_multiline:
        argparse.error("NUL flags and GitHub multiline flags mutually exlusive")
        sys.exit(1)
    if args.trace:
        trace(args.trace, args.path, args.encoding, args.shell,
              args.github_env, args.github_path)
    else:
        printenv((OutputFormat.NUL if args.null else
                  OutputFormat.MULTILINE if args.github_multiline else
                  OutputFormat.NL), args.variables, encoding=args.encoding)
