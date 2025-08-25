from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from accounts.permissions import RolePermission
from accounts.authentication import JWTAuthentication
from backend.utils.response import success_response, error_response
from ..models import Room
from ..serializers.roomserializers import RoomCreateSerializer, RoomUpdateSerializer, RoomListSerializer

class RoomCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']
    # parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = RoomCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            room = serializer.create(serializer.validated_data)
            return success_response(RoomListSerializer().to_representation(room), "Room created successfully", 201)
        return error_response("Validation error", serializer.errors)

class RoomListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management', 'guest']

    def get(self, request):
        rooms = Room.objects.all()
        data = [RoomListSerializer().to_representation(r) for r in rooms]
        return success_response(data)


class RoomDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management', 'guest']
    
    def get(self, request, room_id):
        room = Room.objects(id=room_id).first()
        if not room:
            return error_response("Room not found", 404)
        return success_response(RoomListSerializer().to_representation(room))


class RoomUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']
    # parser_classes = [MultiPartParser, FormParser]

    def put(self, request, room_id):
        room = Room.objects(id=room_id).first()
        if not room:
            return error_response("Room not found", 404)
        serializer = RoomUpdateSerializer(room, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            updated_room = serializer.update(room, serializer.validated_data)
            return success_response(RoomListSerializer().to_representation(updated_room), "Room updated successfully")
        return error_response("Validation error", serializer.errors)


class RoomDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management', 'guest']
    
    def delete(self, request, room_id):
        room = Room.objects(id=room_id).first()
        if not room:
            return error_response("Room not found", 404)
        room.delete()
        return success_response(message="Room deleted successfully")


# class RoomDetailView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [RolePermission]
#     allowed_roles = ['management', 'guest']
    
#     def get(self, request, room_id):
#         room = Room.objects(id=room_id).first()
#         if not room:
#             return error_response("Room not found", 404)
#         return success_response(RoomListSerializer().to_representation(room))