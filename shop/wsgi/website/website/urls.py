from django.conf.urls import include,url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # this is used to inlclude the urls stored in urls.py in SweetShop.
    url(r'^', include('SweetShop.urls')),
]
