PLUGIN="cockpit-file-sharing"
VERSION="2.3.1"
SRC=$(PLUGIN)-$(VERSION).tar.gz

srpm:
	rm -rf build/package
	rm -rf topdir scratch
	mkdir -p {scratch,topdir/SOURCES}
	wget -N "https://github.com/45Drives/$(PLUGIN)/archive/v$(VERSION).tar.gz" -O topdir/SOURCES/$(SRC)
	tar -xzf topdir/SOURCES/$(SRC) --strip-components 3 -C scratch $(PLUGIN)-$(VERSION)/packaging/el8/main.spec
	tar -xzf topdir/SOURCES/$(SRC) --strip-components 1 -C scratch $(PLUGIN)-$(VERSION)/manifest.json
	cp fill_spec.py scratch/;\
	cd scratch;\
	./fill_spec.py
	rpmbuild -bs  --define "_topdir topdir" scratch/$(PLUGIN).spec
	cp -r topdir/SRPMS/* $(outdir)
	rm topdir scratch -rf
	