from rest_framework import serializers

from companyusers.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "location",
            "ceo",
            "employees",
        )
