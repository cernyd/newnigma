gui:
	python3 enigma.py
guiv:
	python3 enigma.py --verbose
cli:
	echo "Run the command 'python3 enigma.py --cli'"
test:
	python3 enigma.py -T
benchmark:
	python3 enigma.py --benchmark 1000000
install:
	sudo apt update
	sudo apt install -y python3-pip python3-pytest
	sudo -H pip3 install --upgrade pip
	sudo -H pip3 install -r requirements.txt
	chmod +x enigma.py
clean:
	find . -name "*pyc*" -delete
