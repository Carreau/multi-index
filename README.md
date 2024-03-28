# proxy server to expose multiple pypi index on the same url. 

In one terminal:


```
$ python multi_index/__init__.py
```

Then you can 

```
$ pip install --index-url http://127.0.0.1:5000 --pre --upgrade numpy scipy
```

And pip will see both the stables package of PyPI and the nightly wheels of https://pypi.anaconda.org/scientific-python-nightly-wheels
