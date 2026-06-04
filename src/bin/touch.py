import os
from pathlib import Path
import sys
import time

createFile = True
executes = []
args = sys.argv[1:]
targetFiles = []
ignoreErrors = False
currentTime = time.time()
onlyA = False
onlyM = False

def main():
    """Update the access and modification times of each FILE to the current time."""
    parseArg()
    for item in executes:
        item()
    if "--help" in args:
        return
    createFileFunc()

def ignoreErrorsToggle():
    """Ignore errors from system"""
    global ignoreErrors
    ignoreErrors = True

def createFileToggle():
    """Do not create any files"""
    global createFile
    createFile = False

def createFileFunc():
    if not createFile: return
    if not targetFiles:
        operandNone()
        return
    for file in targetFiles:
        try:    
            if Path(file).exists:
                if onlyA or onlyM:
                    continue
                Path(file).touch()
            else:
                Path(file).touch()
        except Exception as e:
            touchError(file, e)
            if ignoreErrors:
                continue
            else: return
def changeAccessTime():
    """Change only the access time"""
    global onlyA
    onlyA = True
    for file in targetFiles:
        if Path(file).exists():
            fileMetadata = os.stat(file)
            fileATime = fileMetadata.st_atime
            fileMTime = fileMetadata.st_mtime

            os.utime(file, (currentTime, fileMTime))
        else:
            Path(file).touch()

def changeModTime():
    """Change only the modififcation time"""
    global onlyM
    onlyM = True
    for file in targetFiles:
        if Path(file).exists():
            fileMetadata = os.stat(file)
            fileATime = fileMetadata.st_atime
            fileMTime = fileMetadata.st_mtime

            os.utime(file, (fileATime, currentTime))
        else:
            Path(file).touch()

def helpMenu():
    """Print help information."""
    print(f"{main.__doc__}\n")
    print("Options:")
    spaceInLine = len(max(argList, key=len)) + 1
    for item in argList.keys():
        spaceRemaining = spaceInLine - len(item)
        space = " " * spaceRemaining
        space = ""
        for _ in range(spaceRemaining):
            space += " "
        print(f"  {item}{space}{argList[item].__doc__}")

def parseArg():
    for arg in args:
        if arg.startswith("-"):
            if arg in argList:
                executes.append(argList[arg])
        else:
            targetFiles.append(arg)

def operandNone():
    print("touch: missing file operand")
    print("Try 'touch --help' for more information.")

def touchError(file, error):
    print(f"touch: cannot touch '{file}': {error}")

argList = {
    "--help": helpMenu,
    "-a": changeAccessTime,
    "-m": changeModTime, 
    "-c": createFileToggle, 
    "-i": ignoreErrorsToggle
}
                
if __name__ == "__main__":
    main()