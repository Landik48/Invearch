from .serializer import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password

class User(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): #получение пользователя
        data = {
            "userid": request.user.userid,
            "email": request.user.email,
            "username": request.user.username,
            "description": request.user.description,
            "coins": request.user.startups,
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request): #изменение данных(кроме пароля)
        serializer = UserEditSerialize(data=request.data)
        if serializer.is_valid():
            event = serializer.update(serializer.data)
            return Response("Данные обновлены", status=status.HTTP_200_OK)
        return Response("Ошибка валидации данных", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request): #изменение пароля
        pass

    def delete(self, request): #удаление пользователя
        pass


@api_view(['POST'])
def auth(request): #авторизация
    try:
        serializer = LoginSerialize(data=request.data)
        user = Users.objects.filter(email=request.data['email'])
        if serializer.is_valid() and user:
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            if check_password(password, user.get().password):
                user_auth = authenticate(request, email=email, password=password)
                if user_auth is not None:
                    login(request, user_auth)
                    return Response("Вы вошли в систему!",status=status.HTTP_200_OK)
            return Response("Пароль неверный", status=status.HTTP_400_BAD_REQUEST)
        return Response("Пользователь с такой почтой не найден", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Неверный запрос", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(self, request): #регистрация
    serializer = UserRegister(data=request.data)
    if serializer.is_valid():
        if serializer.check_len(serializer.data):
            if serializer.check_pass(serializer.data):
                user_serializer = UsersSerialize(data=serializer.data)
                password = user_serializer.validated_data.get('password')
                if user_serializer.is_valid():
                    user_serializer.save(password=make_password(password))
                    return Response('register complete')
                else:
                    return Response("email error")
            else:
                return Response("password error", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("limit error", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("error validate", status=status.HTTP_400_BAD_REQUEST)


class Startups(APIView): 
    def get(self, request): #информация о стартапе
        pass

    def post(self, request): #связаться с организатором(при его одобрении)
        pass

    def delete(self, request): #удаление стартапа
        pass