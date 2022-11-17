from rest_framework import serializers
from src.api.models import Check, Printer


class PrinterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Printer
        fields = ['name', 'api_key', 'check_type', 'point_id']


class CheckSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Check
        fields = ['id', 'status']

