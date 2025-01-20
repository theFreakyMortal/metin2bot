import os

for file in os.scandir("stones"):
    print(file.name)