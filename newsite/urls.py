from django.contrib import admin
from django.urls import path, include
#import settings for profile images configuration
from django.conf import settings
#import (static) folder to access the profile images' location
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/',  include('base.api.urls'))
]

#set configure MEDIA_ROOT to MEDIA_URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
