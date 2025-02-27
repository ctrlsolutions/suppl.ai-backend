from rest_framework import routers

from batches.viewsets import DashboardViewSet

router = routers.SimpleRouter()

router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = router.urls