"""URL configuration for the Django system.

The `urlpatterns` list routes URLs to views.
For more information please see:
https://docs.djangoproject.com/en/dev/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r"", include("general.urls", namespace="general")),
    url(r"^events/", include("events.urls", namespace="events")),
    url(r"^admin/", include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]
