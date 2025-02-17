from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from event.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include('event.urls')),
    path('', homepage, name='homepage'),

]+ debug_toolbar_urls()
