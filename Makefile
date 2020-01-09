all: pppp.sh

pppp.sh: pppp.sh.tmpl pppp.py _write_pppp_bash.py
	./_write_pppp_bash.py
