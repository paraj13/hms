from django.urls import path
from .views.roomview import RoomListCreateView, RoomDetailView
from .views.serviceviews import ServiceListCreateView, ServiceDetailView

urlpatterns = [
    # path("create", RoomCreateView.as_view(), name="room-create"),
    # path("list", RoomListView.as_view(), name="room-list"),
    # path("detail/<str:room_id>", RoomDetailView.as_view(), name="room-detail"),
    # path("update/<str:room_id>", RoomUpdateView.as_view(), name="room-update"),
    # path("delete/<str:room_id>", RoomDeleteView.as_view(), name="room-delete"),
    path("rooms/", RoomListCreateView.as_view(), name="room-list-create"),
    path("rooms/<str:room_id>", RoomDetailView.as_view(), name="room-detail"),
    
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<str:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]