"""Models for the events application."""

from os.path import join
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django_google_maps import fields as map_fields

UPLOAD_BASE_PATH = "uploads/events"


class Location(models.Model):
    """Model for location of session."""

    slug = AutoSlugField(unique=True, populate_from="name")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("events:location", kwargs={"location_slug": self.slug})

    def __str__(self):
        """Text representation of Location object.

        Returns:
            Name of location (str).
        """
        return self.name


class LocationImage(models.Model):
    """Model for image of location model."""

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=join(UPLOAD_BASE_PATH, "locations/images/"))
    location = models.ForeignKey(
        Location,
        related_name="images",
    )

    def __str__(self):
        """Text representation of LocationImage object.

        Returns:
            Name of image (str).
        """
        return self.name


class Series(models.Model):
    """Model for event series."""

    slug = AutoSlugField(unique=True, populate_from="name")
    name = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True)
    logo = models.ImageField(upload_to=join(UPLOAD_BASE_PATH, "series/logos/"), null=True, blank=True)
    description = models.TextField()

    def find_closest_event(self):
        """Find the closest event of the series.

        Chooses the first event to match one of the following rules:
        1. Event currently occuring.
        2. Closest event in future.
        3. Closest event in past.

        Returns:
            Event object, or None if no events.
        """
        from events.utils import calculate_days_difference
        events = self.events.filter(is_published=True)
        closest_event = None
        for event in events:
            event.days_difference = calculate_days_difference(event)
            if closest_event is None or (
                event.days_difference >= 0 and event.days_difference < closest_event.days_difference
            ):
                closest_event = event
            elif closest_event is None or (
                event.days_difference < 0 and event.days_difference > closest_event.days_difference
            ):
                closest_event = event
        return closest_event

    def __str__(self):
        """Text representation of Series object.

        Returns:
            Name of series (str).
        """
        return self.name


class Sponsor(models.Model):
    """Model for sponsor of event."""

    name = models.CharField(unique=True, max_length=200)
    url = models.URLField()
    logo = models.ImageField(upload_to=join(UPLOAD_BASE_PATH, "sponsors/logos/"), null=True, blank=True)

    def __str__(self):
        """Text representation of Sponsor object.

        Returns:
            Name of sponsor (str).
        """
        return self.name


class EventBase(models.Model):
    """Abstract base class for event models."""

    def create_slug(self):
        """Create slug for event.

        Returns:
            String of slug.
        """
        if hasattr(self, "series") and self.series:
            return "{}-{}".format(self.series.slug, self.name)
        else:
            return self.name

    slug = AutoSlugField(unique=True, populate_from=create_slug, editable=True, blank=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)

    class Meta:
        """Meta attributes of the class."""

        abstract = True


class Event(EventBase):
    """Model for event in database."""

    location = models.ForeignKey(
        Location,
        related_name="events",
        null=True,
    )
    series = models.ForeignKey(
        Series,
        related_name="events",
        null=True,
        blank=True,
    )
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name="events",
        blank=True,
    )

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("events:event", kwargs={"event_slug": self.slug})

    def __str__(self):
        """Text representation of Event object.

        Returns:
            Name of event (str).
        """
        if self.series:
            return "{}: {}".format(self.series.name, self.name)
        else:
            return self.name


class EventImage(models.Model):
    """Model for image of event model."""

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=join(UPLOAD_BASE_PATH, "events/images/"))
    event = models.ForeignKey(
        Event,
        related_name="images",
    )

    def __str__(self):
        """Text representation of EventImage object.

        Returns:
            Name of image (str).
        """
        return self.name


class Resource(models.Model):
    """Model for resource used in sessions."""

    slug = AutoSlugField(unique=True, populate_from="name")
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=join(UPLOAD_BASE_PATH, "resources/images/"), null=True, blank=True)

    def __str__(self):
        """Text representation of Resource object.

        Returns:
            Name of resource (str).
        """
        return self.name


class Session(models.Model):
    """Model for session of event."""

    slug = AutoSlugField(unique_with=["event__slug"], populate_from="name")
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(join(UPLOAD_BASE_PATH, "sessions/images/"), null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    locations = models.ManyToManyField(
        Location,
        related_name="sessions",
        blank=True,
    )
    resources = models.ManyToManyField(
        Resource,
        related_name="sessions",
        blank=True,
    )

    def __str__(self):
        """Text representation of Session object.

        Returns:
            Name of session (str).
        """
        return self.name


class ThirdPartyEvent(EventBase):
    """Model for third party event in database."""

    url = models.URLField()
    location = models.ForeignKey(
        Location,
        related_name="third_party_events",
        null=True,
    )

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("events:third_party_event", kwargs={"event_slug": self.slug})

    def __str__(self):
        """Text representation of Event object.

        Returns:
            Name of event (str).
        """
        return self.name
