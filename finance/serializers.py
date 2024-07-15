from rest_framework import serializers
from .models import Project, Transaction

class ProjectSerializer(serializers.ModelSerializer):
    total_transactions = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_total_transactions(self, obj):
        return obj.total_transactions()

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
