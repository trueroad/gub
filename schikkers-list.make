# -*-Makefile-*-
.PHONY: all default packages rest update-versions print-success print-branches
.PHONY: nsis schikkers-list schikkers-list-installers
default: all

SCHIKKERS_LIST_BRANCH="master"
SCHIKKERS_LIST_REPO_URL=git://github.com/janneke/schikkers-list.git
SCHIKKERS_LIST_REPO_URL=git+file://localhost/home/janneke/vc/schikkers-list

GUILE_GNOME_BRANCH="master"
GUILE_GNOME_REPO_URL=git://git.sv.gnu.org/guile-gnome.git

PLATFORMS=linux-x86 mingw

# derived info
SCHIKKERS_LIST_SOURCE_URL=$(SCHIKKERS_LIST_REPO_URL)?branch=$(SCHIKKERS_LIST_BRANCH)
SCHIKKERS_LIST_DIRRED_BRANCH=$(shell $(PYTHON) gub/repository.py --branch-dir '$(SCHIKKERS_LIST_SOURCE_URL)')
SCHIKKERS_LIST_FLATTENED_BRANCH=$(shell $(PYTHON) gub/repository.py --full-branch-name '$(SCHIKKERS_LIST_SOURCE_URL)')

GUILE_GNOME_SOURCE_URL=$(GUILE_GNOME_REPO_URL)?branch=$(GUILE_GNOME_BRANCH)
GUILE_GNOME_DIRRED_BRANCH=$(shell $(PYTHON) gub/repository.py --branch-dir '$(GUILE_GNOME_SOURCE_URL)')
GUILE_GNOME_FLATTENED_BRANCH=$(shell $(PYTHON) gub/repository.py --full-branch-name '$(GUILE_GNOME_SOURCE_URL)')

# FOR BUILDING from GIT
#BUILD_PACKAGE='$(SCHIKKERS_LIST_SOURCE_URL)'
BUILD_PACKAGE=schikkers-list
INSTALL_PACKAGE = schikkers-list

MAKE += -f schikkers-list.make

# FOR BUILDING from GIT
INSTALLER_BUILDER_OPTIONS =\
 --version-db=versiondb/schikkers-list.versions\
 $(if $(GUILE_GNOME_BRANCH), --branch=guile-gnome=$(GUILE_GNOME_FLATTENED_BRANCH),)\
 $(if $(SCHIKKERS_LIST_BRANCH), --branch=schikkers-list=$(SCHIKKERS_LIST_FLATTENED_BRANCH),)\
#

include gub.make
include compilers.make

#all: packages rest
all: schikkers-list rest
ifeq ($(findstring mingw, $(PLATFORMS)),mingw)
rest: nsis
endif
rest: schikkers-list-installers print-success

#avoid building native BUILD_PLATFORM
#PYTHON = PATH=$(CWD)/target/tools/root/usr/bin:$(PATH) python
schikkers-list:
	$(foreach p, $(PLATFORMS), $(call INVOKE_GUB,$(p)) $(BUILD_PACKAGE) && ) true #

schikkers-list-installers:
	$(foreach p, $(PLATFORMS), $(call INVOKE_INSTALLER_BUILDER,$(p)) $(INSTALL_PACKAGE) &&) true #

nsis:
	$(GUB) tools::nsis

update-versions:
	$(PYTHON) gub/versiondb.py --no-sources --version-db=versiondb/schikkers-list.versions --download --platforms="mingw,linux-x86" --url=http://lilypond.org/schikkers-list/download/

print-success:
	@echo "success!!"
	@echo Schikkers-List installer in uploads/schikkers-list*.mingw.exe

print-branches:
	@echo "--branch=guile=$(GUILE_GNOME_FLATTENED_BRANCH)"
	@echo "--branch=lilypond=$(LILYPOND_FLATTENED_BRANCH)"
	@echo "--branch=schikkers-list=$(SCHIKKERS_LIST_FLATTENED_BRANCH)"
