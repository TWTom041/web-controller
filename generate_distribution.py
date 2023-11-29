from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import os
import shutil

packname = "web-controller"

shutil.rmtree(f"dist/{packname}/_internal")
os.mkdir(f"dist/{packname}/_internal")

os.chdir(f"dist/{packname}/_internal")
print("downloading python")
resp = urlopen("https://www.python.org/ftp/python/3.9.11/python-3.9.11-embed-amd64.zip")
zipfile = ZipFile(BytesIO(resp.read()))
zipfile.extractall()
zipfile.close()
with open("python39._pth", "a") as f:
    f.write("Lib\nLib\site-packages")

print("writing files")
os.chdir("../../..")
shutil.copytree("venv/Lib", f"dist/{packname}/_internal/Lib")
shutil.copytree("plugins", f"dist/{packname}/_internal/plugins")
shutil.copy2("libvlc.dll", f"dist/{packname}/_internal")
shutil.copy2("libvlccore.dll", f"dist/{packname}/_internal")
shutil.copy2("vlc.exe", f"dist/{packname}/_internal")

shutil.copytree("static", f"dist/{packname}/_internal/static")
shutil.copytree("templates", f"dist/{packname}/_internal/templates")
shutil.copy2("main.py", f"dist/{packname}/_internal")
shutil.copy2("put_ngrok.py", f"dist/{packname}/_internal")
shutil.copy2("gen_ca.py", f"dist/{packname}/_internal")
shutil.copy2("set_password.py", f"dist/{packname}/_internal")

shutil.copy2("LICENSE", f"dist/{packname}/_internal/python39.exe")
shutil.copytree("LICENSES", f"dist/{packname}/_internal/LICENSES")

print("writing batch files")

with open(f"dist/{packname}/change_password.bat", "w") as f:
    f.write("@echo off\npushd _internal & .\python.exe .\set_password.py %* & popd")

with open(f"dist/{packname}/gen_ca.bat", "w") as f:
    f.write("@echo off\npushd _internal & .\python.exe .\gen_ca.py %* & popd")

with open(f"dist/{packname}/main.bat", "w") as f:
    f.write("@echo off\npushd _internal & .\python.exe .\main.py %* & popd")

with open(f"dist/{packname}/put_ngrok.bat", "w") as f:
    f.write("@echo off\npushd _internal & .\python.exe .\put_ngrok.py %* & popd")

print("creating zip file")
shutil.make_archive(f"dist/{packname}-win32-amd64", "zip", "dist", packname)