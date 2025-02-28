from rest_framework import routers

from batches.viewsets import DashboardViewSet, BatchViewSet
from accounts.viewsets import AuthViewSet

router = routers.SimpleRouter()

router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'user', AuthViewSet, basename='user')
router.register(r'inventory', BatchViewSet, basename='inventory')

urlpatterns = router.urls