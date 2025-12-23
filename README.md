# BAHAMAS
Bayesian and Human Reliability Analysis-Aided Method for the Reliability Analysis of Software (BAHAMAS)

## Webpage
https://idaholab.github.io/BAHAMAS/ 

## Installation

Install required libraries:

```bash
  conda create -n bahamas_libs python=3.13
  conda activate bahamas_libs
  pip install toml streamlit==1.35 streamlit-aggrid==1.1.5 numpy>=1.24 pandas==2.3 scipy openpyxl pytest plotly kaleido matplotlib streamlit-option-menu jsonpointer streamlit_extras
```

This can be installed with pip (perferably in a venv):

```bash
pip install --verbose .
```

or


```bash
pip install --verbose --editable .
```
and then run with a command like:

```bash
bahamas -i examples/bnn.toml
```

The tests can be run with:

```bash
pytest
```
