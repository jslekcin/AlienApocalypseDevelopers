import sys
import os
from cx_Freeze import setup, Executable

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