gui:
	python3 enigma.py
guiv:
	python3 enigma.py --verbose
cli:
	echo "Run the command 'python3 enigma.py --cli'"
test:
	python3 enigma.py -T
benchmark:
	python3 enigma.py --benchmark 10000
install:
	sudo apt update
	sudo apt install -y python3-pip pytest
	sudo -H pip3 install --upgrade pip
	sudo -H pip3 install -r requirements.txt
clean:
	find . -name "*pyc*" -delete
