from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
import sys

"""
Contains all the magic required to load the `confit` module, which is neither
in PYTHONPATH, nor has the `.py` extension that is required for automated
loading. By import it here, any other module in this folder can do:
```
from import_confit import confit
```
"""

spec = spec_from_loader("confit", SourceFileLoader("confit", "confit"))
if not spec:
    raise RuntimeError("Failed to load 'confit' module! Please run tests from the repository root.")
confit = module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(confit)
sys.modules['confit'] = confit
ConfitError = confit.ConfitError
