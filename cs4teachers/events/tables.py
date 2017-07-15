"""Tables for the events application."""

import django_tables2 as tables
from events.models import Resource


class ResourceTable(tables.Table):
    """Table for listing resources."""

    name = tables.TemplateColumn("<a href='{{ record.url }}'>{{ record.name }}</a>")

    class Meta:
        model = Resource
        attrs = {"class": "table"}
        fields = ("name", "description")
