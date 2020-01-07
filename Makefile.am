SUBDIRS = tests

bin_SCRIPTS = watcher
noinst_SCRIPTS = watcher-dummy

CLEANFILES = watcher    watcher-dummy
EXTRA_DIST = watcher.in watcher-dummy.in

libexec_watcherdir = @libexecdir@/watcher

nobase_dist_libexec_watcher_SCRIPTS = watcher-nyaa
nobase_dist_libexec_watcher_DATA = \
	lib/__init__.py \
	lib/torrent_parser.py

edit = sed \
	-e 's|@SHELL[@]|$(SHELL)|g' \
	-e 's|@VERSION[@]|$(VERSION)|g' \
	-e 's|@libexecdir[@]|$(libexecdir)|g'

watcher watcher-dummy: Makefile
	rm -f $@ $@.tmp
	srcdir=''; \
		test -f ./$@.in || srcdir=$(srcdir)/; \
		$(edit) $${srcdir}$@.in >$@.tmp
	chmod +x $@.tmp
	chmod a-w $@.tmp
	mv $@.tmp $@

watcher:       $(srcdir)/watcher.in
watcher-dummy: $(srcdir)/watcher-dummy.in

# vim: noet ts=8 sts=8 sw=8:
