import django_gcp.urls
import django_twined.urls
from django.conf.urls import include, re_path
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^gcp/", include(django_gcp.urls)),
    re_path(r"^integrations/octue/", include(django_twined.urls)),
]
