import sys
import os
from cx_Freeze import setup, Executable

files = ["UFO.ico", "GameMusic/", "Images/", "sounds/", "chrisTutorial.txt", "map.txt", "bossMap.txt", "poisonBoss.txt", "poison.txt"]

target = Executable(
    script = "AlienApocalypse.py",
    base = "Win32Gui",
    icon = "UFO.ico"
)

build_exe_options = {
    "excludes" : ["tkinter","unittest"],
    "include_files" : files,
    "packages" : ["pygame"]
}

setup(
    name = "Alien Apocalypse",
    version = "1.0",
    description = "Alien Apocalypse Survival Game",
    options = {"build_exe" : build_exe_options},
    executables = [target]
)
res = []
for (sounds,dir_name,file_names) in os.walk("./"):
    #print(file_names)
    if dir_name == "__pycache__" or dir_name == ".vscode" or dir_name == "Coding Concepts":
        continue
    res.extend(file_names)
#print(res)
res2 = []
for i in range (len(res)):
    str1 = res[i]
    length = len(str1)
    type = str1[length - 3:]
    if type == 'png' or type == 'mp3'or type == 'txt' or type == '.py':
        res2.append(str1)
    
print(res2)
build_exe_options = {
    "include_files":[]
}