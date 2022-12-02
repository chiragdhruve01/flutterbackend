from rest_framework import serializers
from . import models

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
