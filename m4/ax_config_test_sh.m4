# SYNOPSIS
#
#   AX_CONFIG_TEST_SH(SH_FILE...)
#
# DESCRIPTION
#
#   Configures specified files and marks the configured ones as executable.
#   Useful for configuring shell scripts driving testing.
#
# LICENSE
#
#   Copyright (c) 2019 Tomas Volf <wolf@wolfsden.cz>
#
#   WTFPL ver. 2

#serial 1

AC_DEFUN([AX_CONFIG_TEST_SH], [AC_CONFIG_FILES([$1], [chmod -- +x $1])])
