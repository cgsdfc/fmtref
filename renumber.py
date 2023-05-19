import re
from pathlib import Path as P

pat: re.Pattern = re.compile(r"\[(\d+)\]")


def makefunc(i):
    def func(match: re.Match):
        x = i
        return f"[{x}]"

    return func

inputs = P("./input.txt").read_text(encoding='utf8').splitlines()
out = []

for i, line in enumerate(inputs, 1):
    res = pat.sub(makefunc(i), line)
    out.append(res)

P("output.txt").write_text("\n".join(out), encoding='utf8')
