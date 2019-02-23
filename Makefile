gui:
	python3 enigma.py
test:
	python3 -m pytest -s
install:
	sudo apt update
	sudo apt install -y python3-pip pytest
	sudo -H pip3 install --upgrade pip
	sudo -H pip3 install -r requirements.txt
clean:
	find . -name "*pyc*" -delete
benchmark:
	python3 benchmark.py