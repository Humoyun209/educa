from rest_framework import serializers

from courses.models import Content, Course, Module


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()
        

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Content
        fields = ['order', 'item']
        

class ModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['title', 'description', 'order', 'contents']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)
    class Meta:
        model = Course
        fields = '__all__'