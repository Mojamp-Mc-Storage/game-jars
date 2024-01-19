import datetime
import requests, json, os, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

version_manifest = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

manifest = requests.get(version_manifest).json()
if not os.path.exists("release"): os.mkdir("release")
if not os.path.exists("snapshot"): os.mkdir("snapshot")
for x in manifest["versions"]:
    if not os.path.exists(x["type"]+"/"+x["id"]+"/client.jar"):
        vManifest = requests.get(x["url"]).json()
        try:
            os.makedirs(x["type"]+"/"+x["id"])
            print(x["type"], x["id"], "->", vManifest["downloads"]["client"]["url"])
            if "client" in vManifest["downloads"]:
                f = open(x["type"]+"/"+x["id"]+"/client.jar", "wb")
                f.write(requests.get(vManifest["downloads"]["client"]["url"]).content)
                f.close()
            print(x["type"], x["id"], "->", vManifest["downloads"]["server"]["url"])
            if "server" in vManifest["downloads"]:
                f = open(x["type"]+"/"+x["id"]+"/server.jar", "wb")
                f.write(requests.get(vManifest["downloads"]["server"]["url"]).content)
                f.close()
        except: 1

for root, dirs, files in os.walk("."):
    for x in dirs:
        if len(os.listdir(os.path.join(root, x))) == 0 and not os.path.join(root, x).__contains__(".git"):
            os.rmdir(os.path.join(root, x))