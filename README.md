# datapusher

Overvåker folder og sender data i nye/endrede filer som json til webserver.

## Overvåke folder for endringer i filer
TBD

## Eksempel på kode som leser fil og sender data
```
import pandas as pd
df = pd.read_csv("/home/stigbd/src/heming-langrenn/sprint-excel/test-data/Klasser.csv", sep=";")
# konvert dataframe (df) til datamodell (json)
...
# send data til webserver i en post-reqeust
...
```

## Development
### Requirements
- [pyenv](https://github.com/pyenv/pyenv-installer)
- [pipx](https://github.com/pipxproject/pipx)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://github.com/cjolowicz/nox-poetry)

```
% curl https://pyenv.run | bash
% pyenv install 3.9.1
% pyenv install 3.7.9
% python3 -m pip install --user pipx
% python3 -m pipx ensurepath
% pipx install poetry
% pipx install nox
% pipx inject nox nox-poetry
```

### Install
```
% git clone https://github.com/heming-langrenn/sprint-excel.git
% cd sprint-excel/datapusher
% pyenv local 3.9.1 3.7.9
% poetry install
```
### Run all sessions
```
% nox
```
### Run all tests with coverage reporting
```
% nox -rs tests
```
## Run cli script
```
% poetry shell
% sprint_datapusher --help
```
Alternatively you can use `poetry run`:
```
% poetry run sprint_datapusher --help
```
