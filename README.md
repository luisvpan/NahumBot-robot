To activate venv:

En linux

```bash
python -m venv .venv
source .venv/bin/activate
```

En guincods

```bash
python -m venv .venv
.venv/Scripts/activate
```

To install dependencies:

```bash
python -m pip install --editable .
pip install "uvicorn[standard]"
pip install opencv-python
```

Para ejecutar el servidor (Si, en español pa que se arrechen):

```bash
PYTHONPATH=./src uvicorn server.main:app --reload --port 8050
```

guincocs

```bash
fastapi dev src/server/main.py
```
