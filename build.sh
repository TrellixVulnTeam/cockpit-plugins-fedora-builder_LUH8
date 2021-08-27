#! /bin/bash
PLUGIN="cockpit-file-sharing"
VERSION="2.3.1"
SRC=$PLUGIN-$VERSION.tar.gz

rm -rf build/package
rm -rf topdir scratch
mkdir -p {scratch,topdir/SOURCES}
wget -N "https://github.com/45Drives/$PLUGIN/archive/v$VERSION.tar.gz" -O topdir/SOURCES/$SRC
tar -xzf topdir/SOURCES/$SRC --strip-components 3 -C scratch $PLUGIN-$VERSION/packaging/el8/main.spec
tar -xzf topdir/SOURCES/$SRC --strip-components 1 -C scratch $PLUGIN-$VERSION/manifest.json
cat << EOF > scratch/fill_spec.py
#!/bin/python
import json, io, re
camel_to_snake = re.compile(r'(?<!^)(?=[A-Z])')

manifest = json.load(io.open("manifest.json"))
spec = io.open("main.spec").read()

rep = {}

def read_dict(src, dst, prefix = ""):
    for key in src:
        k = camel_to_snake.sub("_", key).lower()
        dkey = k if prefix == "" else prefix+"_"+k
        val = src[key]
        ty = type(val)
        if ty is dict:
            read_dict(val, dst, dkey)
        elif ty is list:
            if len(val) > 0 and type(val[0]) is dict :
                pass
            else:
                dst[dkey] = " ".join(val)
        else:
            dst[dkey] = val

read_dict(manifest, rep, "package")

for key in rep:
    spec = spec.replace("::"+key+"::", str(rep[key]))

io.open(manifest['name']+".spec", mode = "w").write(spec)
EOF
chmod +x scratch/fill_spec.py
cd scratch
./fill_spec.py
cd ..
rpmbuild -bs  --define "_topdir topdir" scratch/$PLUGIN.spec
cp -r topdir/SRPMS/* ./