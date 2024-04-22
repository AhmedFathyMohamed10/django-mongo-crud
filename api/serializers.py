from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'author', 'title', 'body', 'created_at', 'updated_at')

    # This method is responsible for creating a new object
    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    # This method is responsible for updating an exsiting object
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title) 
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance