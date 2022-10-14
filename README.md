<h1 align='center'>Python project template</h1>

## For start project write:

```shell
python3 -m venv venv
. venv/bin/activate
pip install -r requiremenets.txt
chmod +x run.sh
pre-commit install
```

## For run project write:

```shell
./run.sh
```

## For run tests write:

```shell
python3 -m unittest tests/__main__.py
```

## Used linters

### black

For reformatting code <br>
More about it: https://github.com/psf/black

### pyupgrade

For upgrade python code syntax for newer versions of the language <br>
More about it: https://github.com/asottile/pyupgrade

### reorder-python-imports

Tool for automatically reordering python imports <br>
More about it: https://github.com/asottile/reorder_python_imports

### autoflake

Removes unused imports and unused variables from Python code <br>
More about it: https://github.com/PyCQA/autoflake
