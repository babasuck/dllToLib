"""
DllToLib&Inc v1.3 26.03.2023
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
    empty_count = 0
    for file in os.listdir(directory):
        os.chdir(directory)
        if file.endswith(".dll"):
            def_file = _libdir + file[:-4] + ".def"
            inc_file = _incdir + file[:-4] + ".inc"
            #print(inc_file)
            res = subprocess.run(f"dumpbin /nologo /exports {directory}/{file} > {def_file}", shell=True)
            if res.returncode != 0:
                if res.returncode == 1:
                    print("Make sure set path to dumpbin.exe to PATH variable.\n")
                    exit(-1)
                else:
                    print(f"Error with {def_file}\n")
                    count += 1
                    continue
            with open(def_file, "r") as f:
                exports = parse_funName(f.read())
            if len(exports) == 0:
                os.remove(def_file)
                empty_count += 1
                continue
            with open(def_file, "w") as f:
                f.write("EXPORTS\n")
                for export in exports:
                    f.write(export + "\n")
            lib_file = _libdir + file[:-4] + ".lib"
            res = subprocess.run(f"lib /nologo /def:{def_file} /MACHINE:x64 /out:{lib_file} > nul", shell=True)
            if res.returncode != 0:
                if res.returncode == 1:
                    print("Make sure set path to lib.exe to PATH variable.\n")
                    exit(-1)
                else:
                    print(f"Error with {lib_file}\n")
                    count += 1
                    continue
            with open(inc_file, "w") as f:
                for export in exports:
                    f.write("extern __imp_" + export + ":qword \n" + export + " TEXTEQU <__imp_" + export + ">\n")
            os.chdir(_libdir)
            os.remove(def_file)
            count += 1
            if count % 10 == 0:
                print(f"Progress {count} / {len([i for i in os.listdir(directory) if i.endswith('.dll')])}", end="\r", flush=True)

    print("\nFinished.\n"
          f"Empty count - {empty_count}\n")


if __name__ == "__main__":
    if len(sys.argv) < 4:
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
