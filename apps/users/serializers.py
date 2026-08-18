from rest_framework import serializers
from apps.users.models import CustomUser, Address
from django.contrib.auth.password_validation import validate_password


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

   
    def validate(self, data):
        # Reject completely empty address payloads
        required = ["cep", "street", "number", "neighborhood", "city", "state", "label"]

        if not any(data.get(k) for k in required):
            raise serializers.ValidationError(
                detail={
                    "message": "Os campos do endereço não podem ficar vazios.",
                    "code": "empty_address_input",
                }
            )

        return data


    def validate_cep(self, value):
        if value is None:
            raise serializers.ValidationError(detail={"message": "CEP é obrigatório.", "code": "missing_cep"})

        # normalize: accept digits or digits+hyphen, return formatted as 12345-678
        digits = "".join([c for c in str(value) if c.isdigit()])
        if len(digits) != 8:
            raise serializers.ValidationError(detail={"message": "CEP inválido. Use 8 dígitos (ex: 24220000).", "code": "invalid_cep"})

        return f"{digits[:5]}-{digits[5:]}"


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

