Address Extraction App
==============================

Application to extract addresses and match the document with the corresponding object.

This project copies many functions from https://github.com/cfillies/semkibardoc to extract addresses that will serve as training for the Spacy models.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── controller         <- Contain the MVC architecture of a GUI.
    │
    ├── entities           <- Encapsulate business objects of the application. They encapsulate the most general and high-level rules.
    │
    ├── infrastructure     <- Interaction with the storage service.
    │
    ├── service            <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── use_cases          <- Contains application specific business rules.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

Project Guidelines
------------
To install external packages:

    * pip install -r requirements/requirements.txt
--------