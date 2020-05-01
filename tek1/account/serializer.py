from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from account.models import Temp


class TempSerializer(serializers.ModelSerializer):
    # id =serializers.IntegerField(read_only=True)
    uid =serializers.IntegerField()
    name =serializers.CharField(max_length=100)
    address =serializers.CharField(max_length=100)
    gender=serializers.CharField(max_length=100,default='m')
    pincode=serializers.IntegerField(default=24510)
    dob=serializers.CharField(default='saumya', max_length=200)

    class Meta:
        model = Temp
        fields = ['uid', 'name', 'address','pincode','gender', 'dob']

    def create(self, validated_data):
        return Temp.objects.create(**validated_data)
