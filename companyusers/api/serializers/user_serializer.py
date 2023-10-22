from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from companyusers.models import Company

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # add required and optional fields here
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "state",
            "country",
            "city",
        )
        lookup_field = "email"


class UserDetailSerializer(serializers.ModelSerializer):
    # create a field "address" which is a combination of address1 and address2
    address = serializers.SerializerMethodField()
    updated_address = serializers.CharField(write_only=True, required=False)

    updated_fullname = serializers.CharField(write_only=True, required=False)
    fullname = serializers.SerializerMethodField()

    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = User
        # add required and optional fields here
        fields = (
            "id",
            "fullname",
            "updated_fullname",
            "email",
            "company",
            "state",
            "country",
            "city",
            "postcode",
            "education",
            "phone",
            "address",
            "updated_address",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_address(self, obj):
        return f"{obj.address1} {obj.address2}"

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def to_internal_value(self, data):
        if "fullname" in data:
            data["updated_fullname"] = data["fullname"]
            del data["fullname"]

        if "address" in data:
            data["updated_address"] = data["address"]
            del data["address"]

        if "company" in data:
            company_name = data["company"]
            company = Company.objects.filter(name=company_name).first()
            if not company:
                company_options_list = list(
                    Company.objects.values_list("name", flat=True)
                )
                _str = ",".join(company_options_list)
                raise serializers.ValidationError(
                    {"error": f"Company name must be one of these: {_str}"}
                )
            data["company"] = company.id

        return super().to_internal_value(data)

    def create(self, validated_data):
        # check if user is authorized to create a user
        if not self.context["request"].user.is_superuser:
            raise serializers.ValidationError(
                {"error": "You are not authorized to create a user"}
            )

        name = validated_data.get("updated_fullname")
        updated_address = validated_data.get("updated_address", "\n")
        address1, address2 = updated_address.split("\n")
        company = validated_data.get("company")

        user = User.objects.create(
            email=validated_data.get("email"),
            first_name=name.split(" ")[0],
            last_name=name.split(" ")[1],
            address1=address1,
            address2=address2,
            city=validated_data.get("city"),
            state=validated_data.get("state"),
            country=validated_data.get("country"),
            postcode=validated_data.get("postcode"),
            phone=validated_data.get("phone"),
            education=validated_data.get("education"),
            company=company,
        )

        # create the user password and the token
        user.set_password(validated_data.get("password"))
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user

    # def to_representation(self, instance):
    #     print("Inside to_representation")
    #     data = super().to_representation(instance)
    #     data["company"] = instance.company.name
    #     return data

    def update(self, instance, validated_data):
        updated_address = validated_data.get(
            "updated_address", f"{instance.address1}\n{instance.address2}"
        )
        address1 = updated_address.split("\n")[0]
        address2 = updated_address.split("\n")[1]

        name = validated_data.get(
            "updated_fullname", f"{instance.first_name} {instance.last_name}"
        )
        instance.first_name = name.split(" ")[0]
        instance.last_name = name.split(" ")[1]
        instance.address1 = address1
        instance.address2 = address2
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.country = validated_data.get("country", instance.country)
        instance.postcode = validated_data.get("postcode", instance.postcode)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.education = validated_data.get("education", instance.education)
        instance.save()
        return instance
