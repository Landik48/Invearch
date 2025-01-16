from rest_framework import serializers
from .models import Users, Startups
import re

class StartupsListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Startups
        fields = '__all__' 

class LoginSerialize(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = Users
        fields = ('email', 'password')

class UserEditSerialize(serializers.Serializer):
    userid = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    description = serializers.CharField(required=True)
    social_networks = serializers.CharField(required=True)
    def update(self, validated_data):
        user = Users.objects.get(userid=validated_data['userid'])
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.description = validated_data['description']
        return user.save()
    def validate(self, data):
        values = ['username', 'description', 'email', 'userid', 'social_networks']
        if len(data) != 5 or not all(value in data for value in values):
             raise serializers.ValidationError("Error validate")
        return data
    
class UserRegister(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    social_networks = serializers.CharField(required=True)
    def check_pass(self, validated_data):
        password = validated_data['password']
        check_nums = any(character.isdigit() for character in password)
        check_symbols = bool(re.search(r'[^A-Za-z0-9s]', password))
        def has_both_cases(s):
            has_lower = any(char.islower() for char in s)
            has_upper = any(char.isupper() for char in s)
            return has_lower and has_upper
        if len(password) >= 8 and check_nums and check_symbols and has_both_cases(password): 
            return True
        else:
            return False
    def check_len(self, validated_data):
         description = validated_data['description']
         for key in validated_data:
            if len(validated_data[key]) > 100 and validated_data[key] != description:
                return False
            elif len(validated_data[key]) > 500 and validated_data[key] == description:
                return False 
            else: 
                return True
    def validate(self, data):
        values = ['username', 'description', 'email', 'password', 'social_networks'] 
        if len(data) != 5 or not all(value in data for value in values):
             raise serializers.ValidationError("Error validate")
        return data
    
class UsersSerialize(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__' 


class StartupsSerializerSend(serializers.Serializer):
    userid = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    def check_len(self, validated_data):
         message = validated_data['message']
         for key in validated_data:
            if len(validated_data[key]) > 100 and validated_data[key] != message:
                return False
            elif len(validated_data[key]) > 500 and validated_data[key] == message:
                return False 
            else: 
                return True
    def validate(self, data):
        values = ['userid', 'message'] 
        if len(data) != 2 or not all(value in data for value in values):
             raise serializers.ValidationError("Error validate")
        return data
    
class StartupsSerializerAdd(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    picture = serializers.CharField(required=True)
    def check_len(self, validated_data):
         description = validated_data['description']
         picture = validated_data['picture']
         for key in validated_data:
            if len(validated_data[key]) > 100 and (validated_data[key] != description or validated_data[key] != picture):
                return False
            elif len(validated_data[key]) > 500 and (validated_data[key] == description or validated_data[key] == picture):
                return False 
            else: 
                return True
    def validate(self, data):
        values = ['name', 'description', 'picture'] 
        if len(data) != 3 or not all(value in data for value in values):
             raise serializers.ValidationError("Error validate")
        return data