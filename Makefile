SHELL := /bin/bash

python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1 | awk '{print $2}')))
python_3_version_full := $(wordlist 2,4,$(subst ., ,$(shell python3 --version 2>&1 | awk '{print $2}')))
python_version_major := $(word 1,${python_version_full})
python_3_version_major := $(word 1,${python_3_version_full})

python_command_run = ./.virtual_env/Scripts/python run.py
python_command_prepare = python -m venv --clear .virtual_env && ./.virtual_env/Scripts/pip3 install -r ./iris/requirements.txt
python_3_command_prepare = python3 -m venv --clear .virtual_env && ./.virtual_env/Scripts/pip3 install -r ./iris/requirements.txt

init_build := Installing virtual_env and requirements
end_build := Build process finished

all: check_and_prepare

run: check_and_run

check_and_prepare:
	@if [ "${python_version_major}" == "3" ];\
		then \
			echo ${init_build};\
			$(python_command_prepare);\
			echo ${end_build};\
		else if [ "${python_3_version_major}" == "3" ];\
				then \
					echo ${init_build};\
					${python_3_command_prepare};\
					echo ${end_build};\
				else \
					echo "Installing python3...";\
					sudo apt-get install python3;\
					make;\
			fi;\
	fi
	
check_and_run:
	@if [ -d "./.virtual_env" ]; \
		then ${python_command_run}; \
		else echo "Please run command make alone"; \
	fi
	

.PHONY : all
