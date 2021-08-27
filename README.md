# cockpit-plugins-fedora-builder


Script and workflows to auto generate rpm packages for 45Drives cockpit plugins.

* build.py is used by [45Drives_spec_builder](https://copr.fedorainfracloud.org/coprs/jose-pr/cockpit-file-sharing/package/45Drives_spec_builder/)
as a custom script that generates the spec file and correctly formatted source tar.gz from a release github webhook
* check_latest.py is used by a workflow in this repo that runs every hour and if it finds a new version of any of the packages triggers a build 
by simulating a github release webhook
* force_rebuild.py is a tool to force a new build for a package

Enable repo: 
```bash
dnf copr enable jose-pr/cockpit-file-sharing 
```
Install packages: 
```bash
dnf install cockpit-file-sharing
dnf install cockpit-navigator
dnf install cockpit-benchmark
```
