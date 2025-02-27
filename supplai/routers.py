from rest_framework import routers

from batches.viewsets import AverageHealthCheckView

router = routers.SimpleRouter()

router.register(r'health-check', AverageHealthCheckView, basename='health-check')

urlpatterns = router.urls