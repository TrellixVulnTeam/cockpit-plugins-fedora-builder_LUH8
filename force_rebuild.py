#! /bin/python3
import requests
import json
from packaging import version
import sys
from argparse import ArgumentParser


current = "latest.json"

parser = ArgumentParser()
parser.add_argument("--builder", required= False)
parser.add_argument("--release", required= False, default= "latest")
parser.add_argument("package")
parser.add_help = True
args = parser.parse_args()

pkg = args.package
builder =  args.builder if  args.builder != None else open("_builder").read().strip()
release = args.release

def get_latest_release(pkg):
    url = "https://api.github.com/repos/45Drives/{}/releases/{}".format(
        pkg, release)
    with requests.get(url) as req:
        return json.loads(req.text)


release = get_latest_release(pkg)
latest = release['tag_name'].strip("v")
print("Requesting build for {}-{}".format(pkg, latest))
try:
    requests.post(builder, json={
        "release": release
    })
except:
    print("Couldnt update {}".format(pkg))
