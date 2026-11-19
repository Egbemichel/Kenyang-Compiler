"""A small virtual machine that runs the intermediate code directly.

The real compiler output is a native program (see codegen.py). This machine
exists for two reasons: it lets anyone run a Kenyang program on a computer with
no assembler, and it gives the tests a second, independent answer to compare
with the native program.
"""

from __future__ import annotations

from src.ir import (
    BinOp, CallInstr, IntConst, IRFunction, IRProgram, Jump, JumpIfFalse,
    JumpIfTrue, Label, Move, Operand, ReadInstr, ReturnInstr, StrConst, UnOp,
    Var, WriteInstr,
)
from src.optimiser import fold_binary, wrap

TRUE_WORD = "tɛtɛp"
FALSE_WORD = "nse"


class RuntimeFault(Exception):
    """A mistake that only shows up while the program runs."""


class Machine:
    def __init__(self, program: IRProgram, stdin: str = "") -> None:
        self.program = program
        self.funcs = {f.name: f for f in program.functions}
        self.stdin = stdin
        self.in_pos = 0
        self.out: list[str] = []
        self.depth = 0

    def run(self) -> str:
        self.call("main", [])
        return "".join(self.out)

    # ------------------------------------------------------------------ input

    def getc(self) -> str | None:
        if self.in_pos >= len(self.stdin):
            return None
        ch = self.stdin[self.in_pos]
        self.in_pos += 1
        return ch

    def read_int(self) -> int:
        ch = self.getc()
        while ch is not None and (ch in " \t\r\n" or not ch.isascii()):
            ch = self.getc()
        negative = False
        if ch == "-":
            negative = True
            ch = self.getc()
        value = 0
        while ch is not None and ch.isascii() and ch.isdigit():
            value = value * 10 + int(ch)
            ch = self.getc()
        return wrap(-value if negative else value)

    # ------------------------------------------------------------------ calls

    def call(self, name: str, args: list[object]) -> object:
        self.depth += 1
        if self.depth > 20000:
            raise RuntimeFault("the program called itself too deeply")
        func = self.funcs[name]
        result = self.execute(func, args)
        self.depth -= 1
        return result

    def execute(self, func: IRFunction, args: list[object]) -> object:
        env: dict[str, object] = dict(zip(func.params, args))
        body = func.body
        labels = {i.name: n for n, i in enumerate(body) if isinstance(i, Label)}

        def val(op: Operand) -> object:
            if isinstance(op, IntConst):
                return op.value
            if isinstance(op, StrConst):
                return self.program.strings[op.index]
            return env.get(op.name, 0)

        pc = 0
        while pc < len(body):
            ins = body[pc]
            pc += 1
            if isinstance(ins, Label):
                continue
            if isinstance(ins, Move):
                env[ins.dst.name] = val(ins.src)
            elif isinstance(ins, BinOp):
                a, b = val(ins.left), val(ins.right)
                if ins.op in ("/", "%") and b == 0:
                    raise RuntimeFault("division by zero")
                env[ins.dst.name] = fold_binary(ins.op, a, b)  # type: ignore[arg-type]
            elif isinstance(ins, UnOp):
                v = val(ins.operand)
                env[ins.dst.name] = wrap(-v) if ins.op == "neg" else int(v == 0)  # type: ignore[operator]
            elif isinstance(ins, Jump):
                pc = labels[ins.target]
            elif isinstance(ins, JumpIfFalse):
                if not val(ins.cond):
                    pc = labels[ins.target]
            elif isinstance(ins, JumpIfTrue):
                if val(ins.cond):
                    pc = labels[ins.target]
            elif isinstance(ins, CallInstr):
                result = self.call(ins.name, [val(a) for a in ins.args])
                if ins.dst is not None:
                    env[ins.dst.name] = result
            elif isinstance(ins, ReturnInstr):
                return val(ins.value) if ins.value is not None else None
            elif isinstance(ins, WriteInstr):
                v = val(ins.value)
                if ins.ty == "bool":
                    self.out.append((TRUE_WORD if v else FALSE_WORD) + "\n")
                else:
                    self.out.append(f"{v}\n")
            elif isinstance(ins, ReadInstr):
                env[ins.dst.name] = self.read_int()
        return None


def run(program: IRProgram, stdin: str = "") -> str:
    return Machine(program, stdin).run()
