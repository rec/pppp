all: pppp.sh

pppp.sh: pppp.sh.tmpl pppp.py _write_pppp_bash.py
	python _write_pppp_bash.py
