python -m venv .venv
source .venv/bin/activate
python -m pip install .

To execute server
pip install "uvicorn[standard]"
cd src/server
uvicorn main:app

pip install opencv-python

PYTHONPATH=./src python src/server/main.py --reload
PYTHONPATH=./src uvicorn server.main:app --reload

PYTHONPATH=./src uvicorn server.main:app --reload --port=8050
PYTHONPATH=./src uvicorn server.main:app --reload --host 127.0.0.1 --port 8050

cd personal-dev/alderromel-bot
uvicorn server.main:app --reload --port=8050 --log-level debug
PYTHONPATH=./src uvicorn server.main:app --reload --port 8050 --log-level debug
PYTHONPATH=./src uvicorn server.main:app --reload --port 8050 --host 0.0.0.0 --log-level debug

////
cd personal-dev/alderromel-bot
source .venv/bin/activate
PYTHONPATH=./src uvicorn server.main-2:app --reload --port 8050
