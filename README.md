# facebook_imob_chat_integration

Setup
-----
```bash
git clone git@github.com:i-mobility/facebook_imob_chat_integration.git
pyvenv .ve
.ve/bin/pip install -U pip setuptools wheel
.ve/bin/pip install -r requirements.txt
.ve/bin/pip install -e .
```

Running Standalone
------------------
```bash
.ve/bin/python -m imob_*
```

Building
--------
```bash
docker build . -t imobility/facebook_imob_chat_integration
```

Deploying
---------
* Define deployment specs for kubnernetes in the `deployment` directory.
* Remember to forward any ports you might need (defaults to 80).
* Apply with `kubectl apply`.


Testing
-------
The following will install testing dependencies and output to `nose2-junit.xml`:

```bash
.ve/bin/pip install -r requirements-test.txt
IMOB_DEV_MODE=1 .ve/bin/nose2 --plugin nose2.plugins.junitxml --junit-xml --coverage facebook_imob_chat_integration --with-coverage
```
