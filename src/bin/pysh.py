#!/bin/python3

import sys
import os
import subprocess
import readline
from pathlib import Path

args = sys.argv[1:]
os.environ["PATH"] = "/usr/bin:/bin"

def main():
    while True:
        try:
            HOME = os.environ.get("HOME")
            PATH = os.environ.get("PATH").split(":")
            cwd = str(Path.cwd())
            HOME = HOME.rstrip("/")
            if cwd == HOME:
                cwd = "~"
            if cwd.startswith(HOME + "/"):
                cwd = cwd.replace(HOME, "~")
            uInput = input(f"root@PythOS:{cwd}$ ")
            uInput = uInput.strip().split()

            if not uInput:
                continue
            elif uInput[0] == "cd":
                if not uInput[1:] or "".join(uInput[1:]).rstrip("/") == "~":
                    if not Path(HOME).exists():
                        print(f"pyshell: {HOME}: No such file or directory")
                        continue
                    else:
                        os.chdir(HOME)
                else:
                    targetPath = " ".join(uInput[1:])
                    if not Path(targetPath).exists():
                        print(f"pyshell: {targetPath}: No such file or directory")
                        continue
                    else:
                        os.chdir(targetPath)
            else:
                targetBin = uInput[0]
                continueLoop = True
                for path in PATH:
                    if continueLoop:
                        fullPath = os.path.join(path, targetBin)
                        if Path(fullPath).is_file():
                            with open(fullPath, "rb") as f:
                                start_bytes = f.read(2)
                            if start_bytes.startswith(b"#!"):
                                shebangPath = ""
                                with open(fullPath, "r") as file:
                                    shebangPath = file.read().splitlines()[0][2:].strip()
                                    subprocess.run([shebangPath, fullPath] + uInput[1:])
                                    continueLoop = False
                            else:
                                subprocess.run([fullPath] + uInput[1:])
                                continueLoop = False
                        else:
                            pyFullPath = fullPath + ".py"
                            if Path(pyFullPath).is_file():
                                with open(pyFullPath, "rb") as f:
                                    start_bytes = f.read(2)
                                if start_bytes.startswith(b"#!"):
                                    shebangPath = ""
                                    with open(pyFullPath, "r") as file:
                                        shebangPath = file.read().splitlines()[0][2:].strip()
                                        subprocess.run([shebangPath, pyFullPath] + uInput[1:])
                                        continueLoop = False
                                else:
                                    subprocess.run(["/bin/python", pyFullPath] + uInput[1:])
                                    continueLoop = False
                            else:
                                if Path(uInput[0]).is_file():
                                    with open(uInput[0], "rb") as f:
                                        startBytes = f.read(2)
                                        if startBytes == b"#!":
                                            with open(uInput[0], "r") as file:
                                                shebangPath = file.read().striplines()[0][2:].strip()
                                                subprocess.run([shebangPath, pyFullPath] + uInput[1:])
                                                continueLoop = False
                                        elif uInput[0].endswith(".py"):
                                            subprocess.run(["/bin/python3", uInput[0]] + uInput[1:])
                                            continueLoop = False
                                        else:
                                            subprocess.run([uInput[0]] + uInput[1:])
                    else:
                        break
                if continueLoop:
                    print(f"{uInput[0]}: command not found")
        except KeyboardInterrupt:
            print("")
            continue



if __name__ == "__main__":
    showInitMessage()
    main()