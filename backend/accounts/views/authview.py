from rest_framework.views import APIView
from backend.utils.response import success_response, error_response
from ..serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserLoginSerializer
)
from ..permissions import RolePermission
from ..authentication import JWTAuthentication
from backend.utils.jwt_helper import generate_jwt
from ..models import User

# -------------------- CREATE --------------------
class CreateUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                data=user.to_dict(),
                message="User created successfully!",
                status_code=201
            )
        return error_response(
            message="Validation failed",
            errors=serializer.errors,
            status_code=400
        )


# -------------------- LIST --------------------
class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']  # only management can see all users

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return success_response(
            data=serializer.data,
            message="Users fetched successfully"
        )


# -------------------- UPDATE --------------------
class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']  # only management can update

    def put(self, request, user_id):
        user = User.objects(id=user_id).first()
        if not user:
            return error_response(message="User not found", status_code=404)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=user.to_dict(),
                message="User updated successfully"
            )
        return error_response(
            message="Validation failed",
            errors=serializer.errors,
            status_code=400
        )


# -------------------- DELETE --------------------
class UserDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']  # only management can delete

    def delete(self, request, user_id):
        user = User.objects(id=user_id).first()
        if not user:
            return error_response(message="User not found", status_code=404)

        user.delete()
        return success_response(message="User deleted successfully")


# -------------------- LOGIN --------------------
class LoginUserView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_jwt(user)
            return success_response(
                data={"user": user.to_dict(), "token": token},
                message="Login successful"
            )
        return error_response(
            message="Validation failed",
            errors=serializer.errors,
            status_code=400
        )
        