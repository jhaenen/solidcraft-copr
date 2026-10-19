# COPR "make_srpm" build method: COPR runs `make -f .copr/Makefile srpm outdir=... spec=...`
# from the repository root, as root, with network access.
srpm:
	dnf -y install rpmdevtools rpm-build
	spectool -g -C $(outdir) solidcraft.spec
	rpmbuild -bs --define "_sourcedir $(outdir)" --define "_srcrpmdir $(outdir)" solidcraft.spec
