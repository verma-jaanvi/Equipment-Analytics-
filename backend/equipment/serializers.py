from rest_framework import serializers
from .models import DatasetUpload

class DatasetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetUpload
        fields = "__all__"
