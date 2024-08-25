from django.urls import path, include
from rest_framework.routers import DefaultRouter
from machine_config.views import MachineViewSet, MachineDataViewSet, MachineDetailView,register

router = DefaultRouter()
router.register(r'machines', MachineViewSet)
router.register(r'machine-data', MachineDataViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('machine/<int:pk>/',MachineDetailView.as_view(), name='machine-details'),
    path('register/', register, name='register'),
]
