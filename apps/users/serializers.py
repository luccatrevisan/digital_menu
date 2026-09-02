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
    cep = serializers.CharField(
        required=True, 
        error_messages={
            "required" : {
                "message" : "O CEP é obrigatório.",
                "code"  : "missing_cep"
            },
            "blank" : {
                "message" : "O CEP não pode estar vazio.",
                "code"  : "empty_cep"
            }
        })

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_cep(self, value):
        '''
        normalize: accept numbers only and 8 digits (without hifen)        
        '''

        digits = "".join([c for c in str(value).strip() if c.isdecimal()])


        if len(digits) != 8:
            raise serializers.ValidationError(
                detail={
                    "message": "CEP inválido. Use apenas 8 dígitos (ex: 12345000).",
                    "code": "invalid_cep"
                }
            )

        try:
            cep_response = requests.get(VIA_CEP_URL + digits + "/json/", timeout=5)
            '''
            When a CEP with a valid format but nonexistent value is queried the response will contain an "erro" value equal to "true". This means the queried CEP was not found in the database.

            {
                "cep": "01001000",
                "logradouro": "Praça da Sé", -> equivalent to 'street'
                "bairro": "Sé", -> equivalent to 'neighbourhood'
                "localidade": "São Paulo", -> equivalent to 'city'
                "uf": "SP", -> equivalent to 'state'
            }
            '''
        except requests.exceptions.Timeout:
            raise serializers.ValidationError(
                detail={
                    "message": "Não foi possível verificar o CEP. Tente novamente.",
                    "code": "cep_timeout"
                }
            )
        except requests.exceptions.RequestException:
            raise serializers.ValidationError(
                detail={
                    "message": "Não foi possível verificar o CEP. Tente novamente.",
                    "code": "cep_unavailable"
                }
            )

        if "erro" in cep_response.json():
            raise serializers.ValidationError(
                detail={
                    "message" : "Esse CEP não existe. Confira o valor digitado.",
                    "code" : "inexistent_cep"
                }
            )


        return digits


    def validate_street(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError(detail={"message": "O nome da rua não pode ficar vazio.", "code": "missing_street"})

        return str(value).strip()


    def validate_number(self, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise serializers.ValidationError(detail={"message": "O número do endereço é obrigatório.", "code": "missing_number"})

        return str(value).strip()


    def validate_neighborhood(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError(detail={"message": "O bairro não pode ficar vazio.", "code": "missing_neighborhood"})

        return str(value).strip()


    def validate_city(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError(detail={"message": "A cidade não pode ficar vazia.", "code": "missing_city"})

        return str(value).strip()


    def validate_state(self, value):
        if not isinstance(value, str) or not value.strip().isalpha() or len(value.strip()) != 2:
            raise serializers.ValidationError(detail={"message": "O estado deve conter exatamente 2 letras (UF).", "code": "invalid_state"})

        return value.strip().upper()


    def validate_label(self, value):
        allowed = {"CASA", "TRABALHO"}
        if not value or str(value).strip().upper() not in allowed:
            raise serializers.ValidationError(detail={"message": "Tipo de endereço inválido. Opções: CASA, TRABALHO.", "code": "invalid_label"})

        return str(value).strip().upper()

