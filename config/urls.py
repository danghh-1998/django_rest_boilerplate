from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
    url('api/', include('users.urls')),
    url('api/', include('clients.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
