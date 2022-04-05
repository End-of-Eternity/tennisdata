# Tennis Data HTTP API

Simple API for serving tennis game data over HTTP.

## Installation

This project requires Python 3.9+
Clone this repository, then run,

```pip3 install -r requirements.txt```

The project can then be ran by,

```uvicorn tennisdata_app.main:app```

Full documentation for the API is served at http://localhost:8000/docs whilst the app is running.
Example files can be found in ./testfiles

## Issues

- Imported data is not sanity checked, which can corrupt the database (see database.py:123)
- Simple ID assignment breaks when using upload_data(replace=False) (see database.py:124)

## Specification, and Comments

You've been asked to import data from the [tennis-data](http://tennis-data.co.uk) website. The project should use python and provide:
* A way to import data from the source
- API provides a way to upload a zip file. (POST /games/upload/)
  I've since realised that "from the source" might have meant to access the data directly from http://tennis-data.co.uk.
  This could be achieved through urllib to download the file, and zipfile to decompress.

* A HTTP API to access the stored entities (no GUI needed)
- API provides two possible methods to do this.
    - GET /games/{game_id}
      Get game by specific ID (assigned on import by database.py)
    - GET /games/
      Get game by filter. It is possible to filter by all the keys that I thought one might be interested in.
      To keep database performance high, columns such as gambling data are not indexed,
      and are not present in the filter.

* A well organized repository showing your best practices
  - See file structure. Ideally I would have a pyproject.toml

* An example of your approach to unit test / TDD
  - Incomplete

* An easy and documented way to run the project
  - Running the project is documented above. Documentation on usage can be found on http://localhost:8000/docs

* An explanation of your choices (e.g the way you structured the data in storage) and assumptions.
  - Most choices are explained in comments. For the structure of the data in storage I chose SQLAlchemy for its robust
    and easy to use ORM implementation, and also because the FastAPI docs used it
    (https://fastapi.tiangolo.com/tutorial/sql-databases/).
  - I chose to use FastAPI mainly because I heard that this was primarily used by the data engineering team at
    Smartodds, however the speed benefits, and asynchronus code (at least without SQLAlchemy), and modern methods are
    far easier to develop with.
  - I should mention that this is my first time using both SQLAlchemy and FastAPI.

* When you take shortcuts, mention them and tell us what you would do with more time.
  - Any shortcuts taken are documented in comments.
  - I used Python 3.9 as it's what I've currently got installed. Ideally I would have installed 3.10.
  - I should probably also have a consistent format for docstrings.