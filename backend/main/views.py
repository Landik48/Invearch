from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view, authentication_classes

class User(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): #получение пользователя
        def get_startups(class_):
            startups = class_.objects.filter(user=int(request.user.userid))
            startups_names = []
            for startup in startups:
                init_list = [startup.startup.startupid, startup.startup.name]
                if class_ == StartupOwners:
                    startups_interesed = InterestedParties.objects.filter(startup=int(startup.startup.startupid))
                    init_list.append([{'userid': user.user.userid, 
                                       'username': user.user.username,
                                       'description': user.user.description, 
                                       'social_networks': user.user.social_networks,
                                       'message': user.message} 
                                      for user in startups_interesed])
                
                startups_names.append(init_list)
            return startups_names

        data = {
            "userid": request.user.userid,
            "email": request.user.email,
            "username": request.user.username,
            "description": request.user.description,
            'social_networks': request.user.social_networks,
            "my_startups": get_startups(StartupOwners),
            "my_parties": get_startups(InterestedParties)
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
                    user.social_networks = request.data['social_networks']
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


class StartupsList(APIView): 
    def get(self, request): #получение всех стартапов
        startups = Startups.objects.all()
        serializer = StartupsListSerialize(startups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @authentication_classes([IsAuthenticated])
    def post(self, request): #добавление стартапа 
        serializer = StartupsSerializerAdd(data=request.data)
        if serializer.is_valid():
            if serializer.check_len(serializer.data):
                startup = Startups.objects.create(
                    name = request.data['name'],
                    description = request.data['description'],
                    picture = request.data['picture']
                )
                startup.save()
                return Response('Стартап создан', status=status.HTTP_201_CREATED)
            else:
                return Response("Слишком много символов", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Ошибка данных", status=status.HTTP_400_BAD_REQUEST)

class Startup(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, startupid): #получение конкретного стартапа
        startup = Startups.objects.get(startupid=int(startupid))
        data = {
            "startupid": startup.startupid,
            "name": startup.name,
            "description": startup.description,
            "picture": startup.picture,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, startupid): #связаться с организатором
        serializer = StartupsSerializerSend(data=request.data)
        if serializer.is_valid():
            if serializer.check_len(serializer.data):
                user = Users.objects.get(userid=(request.data['userid']))
                startup = Startups.objects.get(startupid=int(startupid))
                try:
                    connect = InterestedParties.objects.create(user=user, startup=startup, message=request.data['message'])
                    connect.save()
                    return Response("Заявка отправлена", status=status.HTTP_200_OK)
                except: return Response("Заявка уже была подана", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Слишком много символов", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Ошибка данных", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, startupid): #удаление стартапа
        startup = Startups.objects.get(startupid=int(startupid))
        startup.delete()