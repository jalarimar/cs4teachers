"""Create test data of event models."""

from datetime import date
from unittest.mock import MagicMock
from django.core.files import File
from events.models import (
    Series,
    Event,
    Location,
    Sponsor,
    Resource,
    ThirdPartyEvent,
)


class EventDataGenerator:
    """Class for generating test data for events."""

    def create_series(self, number):
        """Create series object.

        Args:
            number: Identifier of the series (int).

        Returns:
            Series object.
        """
        logo = MagicMock(spec=File, name="ImageMock")
        logo.name = "Logo for Series {}".format(number)
        series = Series(
            name="Series {}".format(number),
            description="Description for Series {}".format(number),
            logo=logo,
        )
        series.save()
        return series

    def create_event(self, number, series=None, location=None, start_date=None, end_date=None, is_published=True):
        """Create event object.

        Args:
            number: Identifier of the event (int).
            location: Location of the event (Location).
            start_date: Date of the event start (Date).
            end_date: Date of the event end (Date).
            is_published: Boolean if event is public (bool).

        Returns:
            Event object.
        """
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = date.today()
        event = Event(
            name="Event {}".format(number),
            series=series,
            description="Description for Event {}".format(number),
            start_date=start_date,
            end_date=end_date,
            location=location,
            is_published=is_published,
        )
        event.save()
        return event

    def create_location(self, number):
        """Create location object.

        Args:
            number: Identifier of the location (int).

        Returns:
            Location object.
        """
        location = Location(
            name="Location {}".format(number),
            address="Erskine Building, Science Rd, Ilam, Christchurch",
            geolocation="-43.5225594,172.5811949",
            description="Description for Location {}".format(number),
        )
        location.save()
        return location

    def create_resource(self, number):
        """Create resource object.

        Args:
            number: Identifier of the resource (int).

        Returns:
            Resource object.
        """
        resource = Resource(
            name="Resource {}".format(number),
            url="https://www.{}.com/".format(number),
            description="Description for Resource {}".format(number),
        )
        resource.save()
        return resource

    def create_sponsor(self, number):
        """Create sponsor object.

        Args:
            number: Identifier of the sponsor (int).

        Returns:
            Sponsor object.
        """
        logo = MagicMock(spec=File, name="ImageMock")
        logo.name = "Logo for Sponsor {}".format(number)
        sponsor = Sponsor(
            name="Sponsor {}".format(number),
            url="https://www.{}.com/".format(number),
            logo=logo,
        )
        sponsor.save()
        return sponsor

    def create_third_party_event(self, number, location=None, start_date=None, end_date=None, is_published=True):
        """Create third party event object.

        Args:
            number: Identifier of the event (int).
            location: Location of the event (Location).
            start_date: Date of the event start (Date).
            end_date: Date of the event end (Date).
            is_published: Boolean if event is public (bool).

        Returns:
            ThirdPartyEvent object.
        """
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = date.today()
        third_party_event = ThirdPartyEvent(
            name="Third Party Event {}".format(number),
            description="Description for Third Party Event {}".format(number),
            start_date=start_date,
            end_date=end_date,
            location=location,
            url="https://www.{}.com/".format(number),
            is_published=is_published,
        )
        third_party_event.save()
        return third_party_event
