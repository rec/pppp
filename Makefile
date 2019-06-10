all: pppp.sh

pppp.sh: pppp.sh.tmpl pppp.py write_pppp_bash.py
	python write_pppp_bash.py
