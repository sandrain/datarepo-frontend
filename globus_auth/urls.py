
# Django URL imports
from django.conf.urls import url, include

# Relative imports
from . import globus

# Globus URLs
urlpatterns = [
    url(r'^globus/', globus.globus_view),
    url(r'', include('django.contrib.auth.urls')),
    url(r'', include('social_django.urls', namespace='social')),
]