from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vote,Poll,Choice
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','email','password')
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        user=User.objects.create(**validated_data)
        Token.objects.create(user=user)
        return user
    
    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     return instance

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
