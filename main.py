"""
DllToLib&Inc v1.2 25.03.2023
(c) Mantissa для wasm.in
"""

import os
import sys
import subprocess
import re

"""
Используется регулярное выражение для поиска имен функций.
Проверить корректность выражения можно на сайте https://regex101.com/
"""


def parse_funName(input_text):
    lines = input_text.split("\n")
    exports = []
    for line in lines:
        match = re.search(r'^\s*\d+\s+[0-9a-fA-F]+\s+(?:[0-9a-fA-F]+\s+)?(.+?)(?=\s+\(forwarded|\s*$)', line)
        if match:
            if not match.group(1).startswith('['):
                exports.append(match.group(1))
    return exports


def main():
    os.chdir(directory)
    count = 0
    for file in os.listdir(directory):
        os.chdir(directory)
        if file.endswith(".dll"):
            def_file = _libdir + file[:-4] + ".def"
            inc_file = _incdir + file[:-4] + ".inc"
            #print(inc_file)
            subprocess.run(f"dumpbin /nologo /exports {file} > {def_file}", shell=True)
            with open(def_file, "r") as f:
                exports = parse_funName(f.read())
            with open(def_file, "w") as f:
                f.write("EXPORTS\n")
                for export in exports:
                    f.write(export + "\n")
            lib_file = _libdir + file[:-4] + ".lib"
            subprocess.run(f"lib /nologo /def:{def_file} /out:{lib_file} > nul", shell=True)
            with open(inc_file, "w") as f:
                for export in exports:
                    f.write("extern __imp_" + export + ":qword \n" + export + " TEXTEQU <__imp_" + export + ">\n")
            os.chdir(_libdir)
            os.remove(def_file)
            count += 1
            if count % 100 == 0:
                print(f"Progress {count} / {len([i for i in os.listdir(directory) if i.endswith('.dll')])}\n")

    print("Finished.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Select parameters correctly:\n"
              "1 - path to Dll \n"
              "2 - path to save .lib\n"
              "3 - path to save .inc\n")
        exit(-1)
    directory = sys.argv[1] + '\\'
    _libdir = sys.argv[2] + '\\'
    print(_libdir)
    _incdir = sys.argv[3] + '\\'
    print(_incdir)
    #os.system('chcp 65001')
    try:
        pass
        main()
    except Exception as E:
        print(E)