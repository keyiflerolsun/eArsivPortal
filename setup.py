# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from setuptools import setup
from io         import open

setup(
    # ? Genel Bilgiler
    name         = "eArsivPortal",
    version      = "1.1.0",
    url          = "https://github.com/keyiflerolsun/eArsivPortal",
    description  = "GİB e-Arşiv Portal e-Fatura Oluşturucu",
    keywords     = ["eArsivPortal", "KekikAkademi", "keyiflerolsun"],

    author       = "keyiflerolsun",
    author_email = "keyiflerolsun@gmail.com",

    license      = "GPLv3+",
    classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3"
    ],

    # ? Paket Bilgileri
    packages         = ["eArsivPortal"],
    python_requires  = ">=3.10",
    install_requires = [
        "setuptools",
        "wheel",
        "urllib3",
        "requests",
        "pydantic",
        "parsel",
        "cssselect",
        "xmltodict"
    ],

    # ? PyPI Bilgileri
    long_description_content_type = "text/markdown",
    long_description              = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data          = True
)