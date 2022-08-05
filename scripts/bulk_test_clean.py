import re
import sys
fout = open("tests_fixed.txt", "w", encoding="utf-8")
for line in open("tests.txt", encoding="utf-8"):
    print(re.sub("\ ([a-яА-Яa-zA-Z])\)", r"\n\1)", line), file=fout, end ="",)