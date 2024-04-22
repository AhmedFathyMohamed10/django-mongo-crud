from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Note
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'This username is already taken'})

        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'This email is already registered'})

        return data
    
    def create(self, validated_data):
            # Create user
            user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            user.first_name = user.username
            user.last_name = user.username[:2]
            Token.objects.create(user=user)  # generate token for user
            user.save()
            return user
    
    
        
        

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'body', 'created_at', 'updated_at')

    # This method is responsible for creating a new object
    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    # This method is responsible for updating an exsiting object
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title) 
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance