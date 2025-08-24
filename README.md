## Before developing

> [!CAUTION]
> Create a new branch just for you!!

> [!CAUTION]
> The code was developed on wsl 2, as a result I recommend running the code on a linux based system.

```bash
# Step 1.1 - create a virtual env
python -m venv env  # venv called `env`
```
```bash
# Step 1.2 - activate virtual env
source env/bin/activate
```
```bash
# Step 2 - intall dependencies
pip install -r requirements.txt
```

> [!CAUTION]
> Run the `main.py` from the root of the project, otherwise the assets will not be found.

```bash
# Step 3 - run the code
python3 main.py
```