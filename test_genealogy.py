"""Testing"""

import genealogy
import datetime
import os


def test_genealogy():

    test_generated_ids = []

    # Creation
    a = genealogy.person()
    a.create(fn=["Joe"], ln=["BLOGGS"], dob="1900-01-01", pob="Town, County")
    assert "Joe" in a.data["first_names"], "Missing first name at creation"
    assert "BLOGGS" in a.data["last_names"], "Missing last name at creation"
    assert a.data["date_of_birth"] == "1900-01-01", "DOB incorrect at creation"
    assert a.data["place_of_birth"] == "Town, County", "POB incorrect at creation"

    # Saving
    a.save()
    test_generated_ids.append(a.data["id"])
    assert "Joe" in a.data["first_names"], "Missing first name after creation"
    assert "BLOGGS" in a.data["last_names"], "Missing last name after creation"
    assert a.data["date_of_birth"] == "1900-01-01", "DOB incorrect after creation"
    assert a.data["place_of_birth"] == "Town, County", "POB incorrect after creation"

    # Loading
    b = genealogy.person(load=a.data["id"])
    assert "Joe" in b.data["first_names"], "Missing first name at load"
    assert "BLOGGS" in b.data["last_names"], "Missing last name at load"
    assert b.data["date_of_birth"] == "1900-01-01", "DOB incorrect at load"
    assert b.data["place_of_birth"] == "Town, County", "POB incorrect at load"

    # Adding Events
    b.add_event(
        start="1931-04-26",
        title="Address",
        description="1 The Street, Town, Country",
        sources=["1931 Census Record of 1 The Street, Town, Country"],
    )
    assert (
        b.data["life_events"][-1]["start"] == "1931-04-26"
    ), "Date missing from new  event"
    assert (
        b.data["life_events"][-1]["title"] == "Address"
    ), "Title missing from new  event"
    assert (
        b.data["life_events"][-1]["description"] == "1 The Street, Town, Country"
    ), "Description missing from new event"
    assert (
        b.data["life_events"][-1]["sources"][0]
        == "1931 Census Record of 1 The Street, Town, Country"
    ), "Source missing from new event"

    # Sorting Events
    def date_converstion(s):
        return datetime.datetime.strptime(s, "%Y-%m-%d")

    b.add_event(
        start="1900-01-01",
        title="Birth",
        description="Town, Country",
        sources=["Birth Certificate of Joe BLOGGS dob 01/01/1900"],
    )
    b.sort_life_events()
    assert date_converstion(b.data["life_events"][0]["start"]) < date_converstion(
        b.data["life_events"][-1]["start"]
    )
    assert date_converstion(b.data["life_events"][1]["start"]) < date_converstion(
        b.data["life_events"][-1]["start"]
    )

    # TODO Link Partners Test

    # TODO Link Child Test
