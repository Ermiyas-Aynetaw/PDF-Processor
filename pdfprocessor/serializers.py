from rest_framework import serializers
from .models import DocumentAnalysis


class DocumentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAnalysis
        fields = "__all__"
