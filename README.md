Quickstart

git clone https://github.com/Pezdabolius/TestCat.git

python -m venv my_venv
my_venv\Scripts\activate
pip install -r requirements.txt

docker compose up

Start pytest:

 pytest cat/tests.py --ds=core.settings     
