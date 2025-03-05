from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .routers import router
from batches.viewsets import PredictView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('produce/', include('produce.urls')),
    # path('batch/', include('batches.urls')),
    # path('auth/', include('accounts.urls')),
    # path('api/', include(router.urls)),
    path('api/predict/', PredictView.as_view(), name='predict'),
    path('api/', include((router.urls, 'core_api'), namespace='core_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
