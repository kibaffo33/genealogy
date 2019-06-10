import json, os
from uuid import uuid4


template = {
    "id": None,
    "last_names": [],
    "first_names": [],
    "date_of_birth": None,
    "place_of_birth": None,
    "date_of_death": None,
    "place_of_death": None,
    "direct_relatives": {"ascendants": [], "descendants": [], "partners": []},
    "life_events": [
        {
            "start": str(),
            "finish": None,
            "title": "Lifetime",
            "description": None,
            "notes": None,
            "sources": [],
        }
    ],
}


class person:
    """A person record"""

    def __init__(self, **kwargs):
        self.data = template
        self.filename = str()
        ref = kwargs.get("load", None)
        if ref:
            self.load(ref)
            self.id = self.data["id"]

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def create(self, **kwargs):
        self.data["id"] = str(uuid4().hex)[:6]
        self.id = self.data["id"]
        self.data["last_names"] = kwargs.get("ln", [])
        self.data["first_names"] = kwargs.get("fn", [])
        self.data["date_of_birth"] = kwargs.get("dob", None)
        self.data["place_of_birth"] = kwargs.get("pob", None)
        self.filename = f"{self.data['id']}.json"

        if self.data["date_of_birth"]:
            self.data["life_events"][0]["start"] = self.data["date_of_birth"]

    def load(self, id):
        self.filename = f"{id}.json"
        assert os.access(
            self.filename, os.F_OK
        ), f"Filename {self.filename} does not exists"
        self.data = json.load(open(self.filename, "r", encoding="utf-8"))

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
            print(f"{self.filename} saved.")

    def add_event(self, **kwargs):
        self.data["life_events"].append(
            {
                "start": kwargs.get("start", str()),
                "finish": kwargs.get("finish", None),
                "title": kwargs.get("title", None),
                "description": kwargs.get("description", None),
                "notes": kwargs.get("notes", None),
                "sources": kwargs.get("sources", []),
            }
        )

    def sort_life_events(self):

        self.data["life_events"].sort(key=lambda x: dict.get(x, "start"))

    def print_unsourced_events(self):
        for event in self.data["life_events"]:
            if len(event["sources"]) == 0:
                print(f"{event['start']} {event['title']}")


def link_child(**kwargs):
    """Add child as descendants and parents as ascendants."""

    parents = kwargs.get("parents", [])
    child = kwargs.get("child", None)

    assert len(parents) > 0, "Missing input for parents"
    assert child, "Missing input for child"

    for p in parents:
        assert os.access(f"{p}.json", os.F_OK), f"{p}.json does not exist"
    assert os.access(f"{child}.json", os.F_OK), f"{child}.json does not exist"

    for p in parents:
        ascendant = person(load=p)
        if child not in ascendant.data["direct_relatives"]["descendants"]:
            ascendant.data["direct_relatives"]["descendants"].append(child)
            ascendant.save()

        descendant = person(load=child)
        if p not in descendant.data["direct_relatives"]["ascendants"]:
            descendant.data["direct_relatives"]["ascendants"].append(p)
            descendant.save()


def link_partners(partners):
    """Add corresponding ids as partners"""

    try:
        assert len(partners) == 2, "Takes two partners only"
        a = person()
        a.load(partners[0])
        a.data["direct_relatives"]["partners"].append(partners[1])
        a.save()
        b = person()
        b.load(partners[1])
        b.data["direct_relatives"]["partners"].append(partners[0])
        b.save()
    except AssertionError as error:
        print(error)


def index():
    """Return a sorted list of all person records."""

    count = 0
    unsorted_id_name = []
    for file in os.listdir("."):
        if len(file) == 11 and file.endswith(".json"):
            count += 1
            p = person()
            p.load(str(file)[:-5])
            unsorted_id_name.append(f"{p.data['id']} - {p.data['last_names'][0]}, {' '.join(p.data['first_names'])} dob {p.data['date_of_birth']}.")

    sorted_names = []
    for name in unsorted_id_name:
        sorted_names.append(name[9:])
    sorted_names.sort()

    sorted_index = []
    for name in sorted_names:
        for id_name in unsorted_id_name:
            if name in id_name:
                if id_name not in sorted_index:
                    sorted_index.append(id_name)
    assert len(sorted_index) == count, "Error sorting index"

    for record in sorted_index:
        print(record)
    print(f"{count} records.")


def orphan_records():
    """Return a list of records which have no relatives linked."""

    orphans = []
    for file in os.listdir("."):
        if len(file) == 11 and file.endswith(".json"):
            count = 0
            p = person()
            p.load(str(file)[:-5])
            for relative in p.data["direct_relatives"]:
                count += len(p.data["direct_relatives"][relative])
            if count == 0:
                orphans.append(f"{p.data['id']} - {p.data['last_names'][0]}, {' '.join(p.data['first_names'])} dob {p.data['date_of_birth']}.")

    for orphan in orphans:
        print(orphan)


def find(**kwargs):
    """Scan through .json files and return ids of matches. Query first names, last names, dob, occupation, addresses."""

    records = list()
    for file in os.listdir("."):
        if len(file) == 11 and file.endswith(".json"):
            p = person()
            p.load(file[:-5])
            records.append(p.data)

    results = list()

    first_name = kwargs.get("fn", None)
    if first_name:
        for r in records:
            if first_name in r["first_names"]:
                results.append(r)

    last_name = kwargs.get("ln", None)
    if last_name:
        for r in records:
            if last_name in r["last_names"]:
                results.append(r)

    dob = kwargs.get("dob", None)
    if dob:
        for r in records:
            if dob in r["date_of_birth"]:
                results.append(r)

    occupation = kwargs.get("occupation", None)
    if occupation:
        for r in records:
            for event in r["life_events"]:
                if (
                    event["title"].lower() == "occupation"
                    or event["description"].lower() == "occupation"
                    and occupation.lower() in event["notes"].lower()
                ):
                    results.append(r)

    address = kwargs.get("address", None)
    if address:
        for r in records:
            for event in r["life_events"]:
                if (
                    event["title"].lower() == "address"
                    and address.lower() in event["notes"].lower()
                ):
                    results.append(r)

    for r in results:
        print(
            f"{r['id']} - "
            f"{r['last_names'][0]}, {' '.join(r['first_names'])} "
            f"dob {r['date_of_birth']}."
        )
