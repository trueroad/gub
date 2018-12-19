# -*-Makefile-*-
.PHONY: all default packages rest update-versions print-success print-branches
.PHONY: nsis arbora arbora-installers
default: all

ARBORA_BRANCH="master"
ARBORA_REPO_URL=ssh+git://lilypond.org/~/arbora.git
ARBORA_REPO_URL=git+file://localhost/home/janneke/vc/arbora

PLATFORMS=mingw

# derived info
ARBORA_SOURCE_URL=$(ARBORA_REPO_URL)?branch=$(ARBORA_BRANCH)
ARBORA_DIRRED_BRANCH=$(shell $(PYTHON) gub/repository.py --branch-dir '$(ARBORA_SOURCE_URL)')
ARBORA_FLATTENED_BRANCH=$(shell $(PYTHON) gub/repository.py --full-branch-name '$(ARBORA_SOURCE_URL)')
# FOR BUILDING from GIT
#BUILD_PACKAGE='$(ARBORA_SOURCE_URL)'
BUILD_PACKAGE=arbora
INSTALL_PACKAGE = arbora

MAKE += -f arbora.make

# FOR BUILDING from GIT
INSTALLER_BUILDER_OPTIONS =\
 --version-db=versiondb/arbora.versions\
 $(if $(ARBORA_BRANCH), --branch=arbora=$(ARBORA_FLATTENED_BRANCH),)\
#

include gub.make
include compilers.make

#all: packages rest
all: arbora rest
ifeq ($(findstring mingw, $(PLATFORMS)),mingw)
rest: nsis
endif
rest: arbora-installers print-success

#avoid building native BUILD_PLATFORM
#PYTHON = PATH=$(CWD)/target/tools/root/usr/bin:$(PATH) python
arbora:
	$(foreach p, $(PLATFORMS), $(call INVOKE_GUB,$(p)) $(BUILD_PACKAGE) && ) true #

arbora-installers:
	$(foreach p, $(PLATFORMS), $(call INVOKE_INSTALLER_BUILDER,$(p)) $(INSTALL_PACKAGE) &&) true #

nsis:
	$(GUB) tools::nsis

update-versions:
	$(PYTHON) gub/versiondb.py --no-sources --version-db=versiondb/arbora.versions --download --platforms="mingw" --url=http://lilypond.org/blog/janneke/software/arbora

print-success:
	@echo "success!!"
	@echo Arbora installer in uploads/arbora*.mingw.exe

print-branches:
	@echo "--branch=guile=$(GUILE_FLATTENED_BRANCH)"
	@echo "--branch=lilypond=$(LILYPOND_FLATTENED_BRANCH)"
	@echo "--branch=arbora=$(ARBORA_FLATTENED_BRANCH)"
