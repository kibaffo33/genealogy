# genealogy

A package for recording genealogy in human and machine readable .json files. The .json file format has been chosen over the gedcom file format to enable better accessability and interoperability for the recorded data. The package will create .json records in the current working directory.

Dates are ISO format and require a year as the minumum. 'About' dates not accepted.

Requires Python 3.7+.

## Installation

```
pip install genealogy
```

## Usage

Create a person

```
>>> p = genealogy.person()

>>> p.create(fn=["Joe"], ln=["BLOGGS"], dob="1900-1-1", pob="Town, County")

>>> p.print()
{
    "id": "a1b2c3",
    "last_names": ["BLOGGS"],
    "first_names": ["Joe"],
    "date_of_birth": "1900-1-1",
    "place_of_birth": "Town, County",
    "date_of_death": null,
    "place_of_death": null,
    "direct_relatives": {
        "ascendants": [],
        "descendants": [],
        "partners": []
    },
    "life_events": [
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Lifetime",
            "notes": null,
            "sources": []
        }
    ]
}

>>> p.data['date_of_death'] = "1970-1-1"

>>> p.save()
a1b2c3.json saved.
```


Load a person

```
>>> p = genealogy.person()

>>> p.load("a1b2c3.json")

>>> p.print()
{
    "id": "a1b2c3",
    "last_names": ["BLOGGS"],
    "first_names": ["Joe"],
    "date_of_birth": "1900-1-1",
    "place_of_birth": "Town, County",
    "date_of_death": "1970-1-1",
    "place_of_death": null,
    "direct_relatives": {
        "ascendants": [],
        "descendants": [],
        "partners": []
    },
    "life_events": [
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Lifetime",
            "notes": null,
            "sources": []
        }
    ]
}

```


Add life event

```
>>> p = genealogy.person()

>>> p.load("a1b2c3.json")

>>> p.add_event(
        start="1900-1-1",
        description="Birth",
        notes="Town, County",
        sources=[
            "Birth Certificate of Joe BLOGGS dob 01/01/1900"
        ])

>>> p.save()
a1b2c3.json saved.

>>> p.print()
{
    "id": "a1b2c3",
    "last_names": ["BLOGGS"],
    "first_names": ["Joe"],
    "date_of_birth": "1900-1-1",
    "place_of_birth": "Town, County",
    "date_of_death": "1970-1-1",
    "place_of_death": null,
    "direct_relatives": {
        "ascendants": [],
        "descendants": [],
        "partners": []
    },
    "life_events": [
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Lifetime",
            "notes": null,
            "sources": []
        },
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Birth",
            "notes": "Town, County",
            "sources": [
                "Birth Certificate of Joe BLOGGS dob 01/01/1900"
            ]
        }
    ]
}
```


Edit data

```
>>> p = genealogy.person()

>>> p.load("a1b2c3.json")

>>> p.data['life_events][0]
{'start': None, 'finish': None, 'description': 'Lifetime', 'notes': None, 'sources': []}

>>> p.data['life_events][0]['sources'].append("Birth Certificate of Joe BLOGGS dob 01/01/1900")

>>> p.save()
a1b2c3.json saved.

>>> p.print()
{
    "id": "a1b2c3",
    "last_names": ["BLOGGS"],
    "first_names": ["Joe"],
    "date_of_birth": "1900-1-1",
    "place_of_birth": "Town, County",
    "date_of_death": "1970-1-1",
    "place_of_death": null,
    "direct_relatives": {
        "ascendants": [],
        "descendants": [],
        "partners": []
    },
    "life_events": [
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Lifetime",
            "notes": null,
            "sources": [
                "Birth Certificate of Joe BLOGGS dob 01/01/1900"
            ]
        },
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Birth",
            "notes": "Town, County",
            "sources": [
                "Birth Certificate of Joe BLOGGS dob 01/01/1900"
            ]
        }
    ]
}
```


Link parent(s) and child

```
>>> genealogy.link_child(
         parents=["g4h5i6", "m7n8o9"],
         child="a1b2c3")

>>> p = load("a1b2c3.json")

>>> p.print()
{
    "id": "a1b2c3",
    "last_names": ["BLOGGS"],
    "first_names": ["Joe"],
    "date_of_birth": "1900-1-1",
    "place_of_birth": "Town, County",
    "date_of_death": "1970-1-1",
    "place_of_death": null,
    "direct_relatives": {
        "ascendants": ["g4h5i6", "m7n8o9"],
        "descendants": [],
        "partners": []
    },
    "life_events": [
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Lifetime",
            "notes": null,
            "sources": [
                "Birth Certificate of Joe BLOGGS dob 01/01/1900"
            ]
        },
        {
            "start": "1900-1-1",
            "finish": null,
            "description": "Birth",
            "notes": "Town, County",
            "sources": [
                "Birth Certificate of Joe BLOGGS dob 01/01/1900"
            ]
        }
    ]
}

```
