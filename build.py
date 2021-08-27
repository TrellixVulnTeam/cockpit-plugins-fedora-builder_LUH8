#!/bin/python3
import tarfile
import json
import io
import re
import os
import requests
import shutil
from pathlib import Path

PAYLOAD_PATH = "hook_payload"
TOPDIR = "topdir"
SOURCES = TOPDIR + "/SOURCES/"
TMP = TOPDIR+"/tmp"
CAMEL_TO_SNAKE = re.compile(r'(?<!^)(?=[A-Z])')

dirpath = Path(TMP)
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)

Path(SOURCES).mkdir(parents=True, exist_ok=True)
Path(TMP).mkdir(parents=True, exist_ok=True)

hook_payload = json.load(io.open(PAYLOAD_PATH)
                         ) if os.path.exists(PAYLOAD_PATH) else {}

src_url = hook_payload['release']['tarball_url']
with requests.get(src_url) as req:
    src_bytes = io.BytesIO(req.content)


with tarfile.open(fileobj=src_bytes, mode="r:gz") as src:
    top = src.getmembers()[0].name
    spec = "BuildRequires: make\n" + \
        src.extractfile(top+"/packaging/el8/main.spec").read().decode('utf8')
    manifest = json.load(src.extractfile(top+"/manifest.json"))
    rel_name = manifest['name']+"-"+manifest['version'];
    src.extractall(TMP)
    with io.open(SOURCES +  
        rel_name+".tar.gz", 'wb') as tar:
        with tarfile.open(fileobj=tar, mode='x:gz') as tar:
            tar.add(TMP+"/"+top, rel_name)

def read_dict(src, dst, prefix=""):
    for key in src:
        k = CAMEL_TO_SNAKE.sub("_", key).lower()
        dkey = k if prefix == "" else prefix+"_"+k
        val = src[key]
        ty = type(val)
        if ty is dict:
            read_dict(val, dst, dkey)
        elif ty is list:
            if len(val) > 0 and type(val[0]) is dict:
                pass
            else:
                dst[dkey] = " ".join(val)
        else:
            dst[dkey] = val


params = {}
read_dict(manifest, params, "package")

for key in params:
    spec = spec.replace("::"+key+"::", str(params[key]))

io.open(SOURCES+manifest['name']+".spec", mode="w").write(spec)


                 
