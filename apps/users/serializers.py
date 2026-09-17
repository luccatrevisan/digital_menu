from rest_framework import serializers
from apps.users.models import CustomUser, Address
from django.contrib.auth.password_validation import validate_password
import requests

VIA_CEP_URL = "https://viacep.com.br/ws/"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "password"]

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username muito curto.")
        return value
 
    def create(self, validated_data): 
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"]
        )

        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_cep(self, value):
        digits = "".join([c for c in str(value).strip() if c.isdecimal()])

        if len(digits) != 8:
            raise serializers.ValidationError("CEP inválido. Use apenas 8 dígitos e evite hífen (ex: 12345000).")

        try:
            cep_response = requests.get(VIA_CEP_URL + digits + "/json/", timeout=5)
            '''
            ViaCEP output: {
                                "cep": "01001000", -> only numbers, without hifen.
                                "uf": "SP"
                            }
            '''

        except requests.exceptions.Timeout:
            raise serializers.ValidationError("Não foi possível verificar o CEP. Tente novamente mais tarde.")
        
        except requests.exceptions.RequestException:
            raise serializers.ValidationError("Não foi possível verificar o CEP. Tente novamente.")

        data = cep_response.json()

        if data.get("erro"):
            # if there is a key "erro" in the API output, it means that the CEP doesn't exist.
            raise serializers.ValidationError("Esse CEP não existe. Confira o valor digitado.")

        if data.get("uf") != "RJ":
            # validation to avoid CEPs from places outside the delivery area
            raise serializers.ValidationError("Infelizmente não atendemos no seu estado ainda! Por enquanto nossa área de atuação está focada no RJ.")

        return digits