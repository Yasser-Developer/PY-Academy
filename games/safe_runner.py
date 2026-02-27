from __future__ import annotations

import ast
import builtins
import multiprocessing
from dataclasses import dataclass
from io import StringIO
import sys
from typing import Any


@dataclass(frozen=True)
class RunResult:
    success: bool
    output: str


_ALLOWED_BUILTINS = {
    "print": builtins.print,
    "range": builtins.range,
    "len": builtins.len,
    "int": builtins.int,
    "float": builtins.float,
    "str": builtins.str,
    "bool": builtins.bool,
    "list": builtins.list,
    "dict": builtins.dict,
    "set": builtins.set,
    "tuple": builtins.tuple,
    "enumerate": builtins.enumerate,
    "zip": builtins.zip,
    "min": builtins.min,
    "max": builtins.max,
    "sum": builtins.sum,
    "abs": builtins.abs,
}


_DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Attribute,
    ast.Lambda,
    ast.ClassDef,
    ast.With,
    ast.AsyncWith,
    ast.Await,
    ast.AsyncFunctionDef,
    ast.Try,
    ast.Raise,
    ast.Global,
    ast.Nonlocal,
    ast.Yield,
    ast.YieldFrom,
)


def _validate_ast(code: str) -> None:
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as e:
        raise ValueError(str(e)) from e

    for node in ast.walk(tree):
        if isinstance(node, _DISALLOWED_NODES):
            raise ValueError("این کد شامل دستور غیرمجاز است.")

        if isinstance(node, ast.Call):
            # Only allow calling by simple name: print(...), range(...), my_func(...)
            if not isinstance(node.func, ast.Name):
                raise ValueError("فراخوانی این نوع تابع/متد مجاز نیست.")

            # Block any attempt to call dunder-ish names.
            if node.func.id.startswith("__"):
                raise ValueError("فراخوانی این نوع تابع مجاز نیست.")


def _exec_in_subprocess(code: str, queue: multiprocessing.Queue) -> None:
    stdout = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout
    try:
        safe_globals: dict[str, Any] = {"__builtins__": _ALLOWED_BUILTINS}
        safe_locals: dict[str, Any] = {}
        compiled = compile(code, "<user_code>", "exec")
        exec(compiled, safe_globals, safe_locals)
        queue.put(RunResult(success=True, output=stdout.getvalue()))
    except Exception as e:
        queue.put(RunResult(success=False, output=str(e)))
    finally:
        sys.stdout = old_stdout


def run_user_code(code: str, timeout_seconds: int = 2) -> RunResult:
    if not code or not code.strip():
        return RunResult(success=False, output="کد خالی است.")

    if len(code) > 8000:
        return RunResult(success=False, output="کد خیلی طولانی است.")

    _validate_ast(code)

    ctx = multiprocessing.get_context("spawn")
    queue: multiprocessing.Queue = ctx.Queue()
    proc = ctx.Process(target=_exec_in_subprocess, args=(code, queue), daemon=True)
    proc.start()
    proc.join(timeout_seconds)

    if proc.is_alive():
        proc.terminate()
        proc.join(1)
        return RunResult(success=False, output="زمان اجرای کد زیاد شد (Timeout).")

    if queue.empty():
        return RunResult(success=False, output="خطای نامشخص در اجرای کد.")

    return queue.get()

