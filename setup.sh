sudo apt update -y
sudo apt upgrade -y
sudo apt install curl -y
sudo apt install python3.8 python3.8-dev python3.8-venv python3-venv idle-python3.8 python3-pip virtualenv gcc default-libmysqlclient-dev libssl-dev -y
sudo apt install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt