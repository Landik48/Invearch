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
        # startups = получение модельки для содержательного отображения
        data = {
            "userid": request.user.userid,
            "email": request.user.email,
            "username": request.user.username,
            "description": request.user.description,
            "startups": str(request.user.startups),
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request): #изменение данных
        serializer = UserRegister(data=request.data)
        if serializer.is_valid():
            if serializer.check_len(serializer.data):
                if serializer.check_pass(serializer.data):
                    user = Users.objects.get(userid=request.user.userid)
                    user.username = request.data['username']
                    user.email = request.data['email']
                    user.description = request.data['description']
                    user.password = make_password(request.data['password'])
                    user.save()
                    return Response("Данные обновлены", status=status.HTTP_200_OK)
                else:
                    return Response("Слабый пароль", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Слишком много символов", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Ошибка валидации данных", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request): #выход и удаление пользователя
        if request.data['option'] == 'exit':
            logout(request)
            return Response("Вы вышли из системы!", status=status.HTTP_200_OK)
        elif request.data['option'] == 'delete':
            user = Users.objects.get(userid=int(request.user.userid))
            user.delete()
            return Response("Аккаунт удалён", status=status.HTTP_200_OK)


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
                    return Response("Успешно!", status=status.HTTP_200_OK)
            return Response("Пароль неверный", status=status.HTTP_400_BAD_REQUEST)
        return Response("Пользователь с такой почтой не найден", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Неверный запрос", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request): #регистрация
    serializer = UserRegister(data=request.data)
    if serializer.is_valid():
        if serializer.check_len(serializer.data):
            if serializer.check_pass(serializer.data):
                user_serializer = UsersSerialize(data=serializer.data)
                if user_serializer.is_valid():
                    password = user_serializer.validated_data.get('password')
                    user_serializer.save(password=make_password(password))
                    return Response('Вы зарегистрированы', status=status.HTTP_200_OK)
                else:
                    return Response("Почта занята")
            else:
                return Response("Слабый пароль", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Слишком много символов", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Ошибка данных", status=status.HTTP_400_BAD_REQUEST)


class Startups(APIView): 
    def get(self, request): #информация о стартапе
        pass

    def post(self, request): #связаться с организатором(при его одобрении)
        pass

    def delete(self, request): #удаление стартапа
        pass