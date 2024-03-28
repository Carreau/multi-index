from flask import Flask

import requests
from copy import copy
import bs4

app = Flask(__name__)

PYPI_URL = "https://pypi.org/simple/"

# we currently assume that /simple repository for the nightly mirror
# have a strict structure where the wheels urls are relative to the root and starting with a `/`,
# so we can modify href and preprend the domain.
NIGHTLY_MIRROR = [
    (
        "https://pypi.anaconda.org/scientific-python-nightly-wheels/simple/",
        "https://pypi.anaconda.org",
    )
]


@app.route("/")
def index():
    """
    Just proxy the main pypi root page,
    this means we can only proxy nightly of packages that do exist on PyPI.
    """
    return requests.get(PYPI_URL).text


@app.route("/<package>/")
def simple(package):
    fixed_nightly = []
    for mir, root in NIGHTLY_MIRROR:
        assert mir.endswith("/")
        assert not root.endswith("/")
        resp = requests.get(mir + package)
        page = bs4.BeautifulSoup(resp.text)

        nightly = page.html.body.find_all("a")

        for old_a in nightly:
            a = copy(old_a)
            if a.attrs["href"].startswith("/"):
                a.attrs["href"] = root + a.attrs["href"]
                fixed_nightly.append(a)

    # we get the PyPI page and appends the wheels to it.
    resp = requests.get(PYPI_URL + package)
    page = bs4.BeautifulSoup(resp.text)
    for n in fixed_nightly:
        page.html.body.append(n)

    return str(page)


if __name__ == "__main__":
    app.run(debug=True)
