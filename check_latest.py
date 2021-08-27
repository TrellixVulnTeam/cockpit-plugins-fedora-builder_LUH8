#! /bin/python3
import requests
import json
from packaging import version
import sys

current = "latest.json"
builder = sys.argv[1]


def get_latest_release(pkg):
    url = "https://api.github.com/repos/45Drives/{pkg}/releases/latest".format(
        pkg=pkg)
    with requests.get(url) as req:
        return json.loads(req.text)

watching = json.load(open(current))
for pkg, ver in watching.items():
    release = get_latest_release(pkg)
    latest = release['tag_name'].strip("v")
    if version.parse(ver) < version.parse(latest):
        print("Requesting build for {}-{}, current version {}".format(pkg, latest, ver))
        try:
            requests.post(builder, json={
                "release": release
            })
            watching[pkg] = latest
        except:
            print("Couldnt update {}".format(pkg))
    else:
        print("{} is up to date".format(pkg))
json.dump(watching, open(current, 'w'))
