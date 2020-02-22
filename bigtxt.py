import os
import random
import unicodedata

def filt(word):
    return unicodedata.normalize('NFKD', word).encode('ascii', errors='ignore').decode('ascii')

fileList = [{"dir": x[0],"files": x[2]} for x in os.walk("./")]
fileDescList = []

for df in fileList:
    dirDescObj = {
        "dir":df["dir"],
        "txtFiles":[]
    }

    for file in df["files"]:
        if file[-4:] == ".txt":
            dirDescObj["txtFiles"].append(file)
    fileDescList.append(dirDescObj)

fileText = []
for file in fileDescList:
    for txtFile in file["txtFiles"]:
        with open(f"{file['dir']}\{txtFile}", "r") as f:
            fileText.append(f"{f.read()}")
        print(f"copied {txtFile}")

random.shuffle(fileText)
shuffleText = " ".join(fileText)
with open('testtext.txt', "w") as f:
    print(f"copied {txtFile}")
    f.write(filt(shuffleText))
