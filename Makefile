run:
	./enigma.py
test:
	python3 -m pytest
install:
	sudo apt update
	sudo apt install -y python3-pip pytest
	sudo -H pip3 install --upgrade pip
	sudo -H pip3 install -r requirements.txt
clean:
	find . -name "*pyc*" -delete
