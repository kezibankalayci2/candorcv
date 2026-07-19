$ErrorActionPreference = 'Stop'
python -m compileall -q app tests
python -m unittest discover -s tests -v

