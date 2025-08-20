from rest_framework.views import APIView
from backend.utils.response import success_response, error_response
from ..serializers import (
    UserCreateSerializer, UserUpdateSerializer, UserListSerializer, UserLoginSerializer
)
from ..permissions import RolePermission
from ..authentication import JWTAuthentication
from backend.utils.jwt_helper import generate_access_token, generate_refresh_token
from ..models import User, RefreshToken
import datetime

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
        return error_response(message="Validation failed", errors=serializer.errors, status_code=400)


# -------------------- LIST --------------------
class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']

    def get(self, request):
        # Get role from query params
        role = request.GET.get("role")

        if role:
            users = User.objects(role=role)
        else:
            users = User.objects.all()
        
        serializer = UserListSerializer(users, many=True)
        return success_response(data=serializer.data, message="Users fetched successfully")


# -------------------- UPDATE --------------------
class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']

    def put(self, request, user_id):
        user = User.objects(id=user_id).first()
        if not user:
            return error_response(message="User not found", status_code=404)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=user.to_dict(), message="User updated successfully")
        return error_response(message="Validation failed", errors=serializer.errors, status_code=400)


# -------------------- DELETE --------------------
class UserDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']

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
            user = serializer.validated_data["user"]

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            # save refresh token in DB
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
            RefreshToken(user_id=str(user.id), token=refresh_token, expires_at=expires_at).save()

            return success_response(
                data={
                    "user": user.to_dict(),
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                message="Login successful"
            )

        return error_response(
            message="Validation failed",
            errors=serializer.errors,
            status_code=400
        )


# -------------------- LOGOUT --------------------
class LogoutUserView(APIView):
    
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return error_response(message="Refresh token required", status_code=400)

        token_entry = RefreshToken.objects(token=refresh_token).first()
        if not token_entry:
            return error_response(message="Invalid refresh token", status_code=400)

        token_entry.delete()
        return success_response(message="Logout successful, refresh token revoked")

class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RolePermission]
    allowed_roles = ['management']

    def get(self, request):
        total_users = User.objects.count()
       

        data = {
            "total_users": total_users,
           
        }

        return success_response(message="Dashboard data fetched successfully", data=data)
