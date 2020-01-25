AM_TESTS_ENVIRONMENT = \
	SHOULD_OUTPUT= \
	WATCHER_STORE="@builddir@/store" \
	WATCHER_BIN="@top_builddir@/watcher" \
	WATCHER_LIBEXECDIR="@top_builddir@" \
	PATH="@top_builddir@:@top_srcdir@:$$PATH"

shell_ins = \
	err_errors_from_target_are_printed.sh \
	err_target_missing.sh \
	err_unknown_arg.sh \
	err_unknown_watcher.sh \
	test_change_output.sh \
	test_help.sh \
	test_id_is_checked.sh \
	test_id_is_respected.sh \
	test_no_change_no_output.sh \
	test_nyaa.sh \
	test_version.sh

TESTS = $(shell_ins)

EXTRA_DIST = init_test $(shell_ins:=.in)
CLEANFILES = $(shell_ins) store

SUFFIXES = .sh.in .sh

edit = sed \
	-e 's|@SHELL[@]|$(SHELL)|g' \
	-e 's|@VERSION[@]|$(VERSION)|g' \
	-e 's|@srcdir[@]|$(srcdir)|g'

$(shell_ins): Makefile
.sh.in.sh:
	@rm -f $@ $@.tmp
	@srcdir=''; \
		test -f ./$@.in || srcdir=$(srcdir)/; \
		$(edit) $${srcdir}$@.in >$@.tmp
	@chmod +x $@.tmp
	@chmod a-w $@.tmp
	@mv $@.tmp $@
