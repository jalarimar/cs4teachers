"""Administration configuration for the events application."""

from django.contrib import admin
from django.db import models
from events.models import (
    Event,
    ThirdPartyEvent,
    Location,
    Session,
    Series,
    Sponsor,
    Resource,
    LocationImage,
    EventImage,
)
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from tinymce.widgets import TinyMCE


class SessionAdmin(admin.ModelAdmin):
    """Admin interface for Session model."""

    exclude = ("slug",)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ("name", "event")
    search_fields = ["name", "event"]
    list_filter = ("event",)
    filter_vertical = ("resources", "locations",)


class SessionInline(admin.StackedInline):
    """Admin interface for Session model when displayed inline."""

    model = Session
    extra = 5
    exclude = ("slug",)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    filter_vertical = ("resources", "locations",)


class LocationAdmin(admin.ModelAdmin):
    """Admin interface for Location model."""

    exclude = ("slug",)
    formfield_overrides = {
        map_fields.AddressField: {"widget": map_widgets.GoogleMapsAddressWidget},
        models.TextField: {'widget': TinyMCE()},
    }


class ResourceAdmin(admin.ModelAdmin):
    """Admin interface for Resource model."""

    exclude = ("slug",)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ("name", "url")


class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model."""

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "description", "start_date", "end_date", "series", "location", "sponsors"]
            }
        ),
        (
            "Visibility",
            {
                "fields": ["is_published"]
            }
        ),
        (
            "Advanced",
            {
                "fields": ["slug"],
                "classes": ("grp-collapse", "grp-closed")
            }
        ),
    ]
    inlines = [SessionInline]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ("name", "series", "location", "start_date", "end_date")
    list_filter = ("is_published",)
    search_fields = ["name"]
    filter_vertical = ("sponsors",)


class ThirdPartyEventAdmin(admin.ModelAdmin):
    """Admin interface for ThirdPartyEvent model."""

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "url",
                    "start_date",
                    "end_date",
                    "description",
                    "location",
                ]
            }
        ),
        (
            "Visibility",
            {
                "fields": ["is_published"]
            }
        ),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ("name", "location", "start_date", "end_date")
    list_filter = ("is_published",)
    search_fields = ["name"]


admin.site.register(Event, EventAdmin)
admin.site.register(ThirdPartyEvent, ThirdPartyEventAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Series)
admin.site.register(Sponsor)
admin.site.register(LocationImage)
admin.site.register(EventImage)
