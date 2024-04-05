from rest_framework.serializers import CharField, Serializer
from .models import Secrets, Entries
from rest_framework import serializers


class SecretsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Secrets
        fields = '__all__'

class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entries
        fields = '__all__'
 