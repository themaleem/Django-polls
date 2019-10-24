from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vote,Poll,Choice


class UserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    first_name=serializers.CharField(max_length=100)
    last_name=serializers.CharField(max_length=100)
    email=serializers.EmailField(max_length=100)

    def create(self,validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class VoteSerializer(serializers.ModelSerializer):
    # user=UserSerializer(many=True,required=False)
    class Meta:
        model= Vote
        fields="__all__"
    
class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)
    class Meta:
        model= Choice
        fields="__all__"

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        model= Poll
        fields="__all__"
