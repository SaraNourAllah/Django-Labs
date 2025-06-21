from rest_framework import serializers
from  .models import Courses


class CourseSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=100)
    image=serializers.ImageField()

    def create(self, validated_data):
        return Courses.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance