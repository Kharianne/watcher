AC_PREREQ([2.69])

AC_INIT([watcher], [0.0.1], [wolf@wolfsden.cz])

AC_CONFIG_SRCDIR([watcher.in])
AC_CONFIG_SRCDIR([watcher-dummy.in])

AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE([
	-Wall -Werror foreign color-tests parallel-tests subdir-objects dist-xz
])

AC_CONFIG_FILES([Makefile])
AX_CONFIG_TEST_SH([watcher])
AX_CONFIG_TEST_SH([watcher-dummy])

AC_CONFIG_FILES([tests/Makefile])
AX_CONFIG_TEST_SH([tests/err_unknown_watcher])
AX_CONFIG_TEST_SH([tests/err_unknown_arg])
AX_CONFIG_TEST_SH([tests/err_target_missing])
AX_CONFIG_TEST_SH([tests/test_no_change_no_output])
AX_CONFIG_TEST_SH([tests/test_change_output])
AX_CONFIG_TEST_SH([tests/test_help])
AX_CONFIG_TEST_SH([tests/test_version])

AC_OUTPUT

# vim: noet ts=8 sts=8 sw=8:
