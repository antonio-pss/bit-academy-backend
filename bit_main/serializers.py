from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'xp', 'streak', 'active', 'password', 'created_at', 'modified_at']
        read_only_fields = ['id', 'created_at', 'modified_at']

    def validate_password(self, value):
        """ Valida a senha usando as regras do Django """
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        """ Garante que a senha é armazenada como hash ao criar """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """ Garante que a senha é armazenada como hash ao atualizar """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """ Criação do usuário garantindo que a senha seja armazenada de forma segura """
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """ Autentica o usuário e gera tokens JWT """
        email = data["email"]
        password = data["password"]
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Credenciais inválidas.")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        """ Invalida o token de refresh """
        try:
            token = RefreshToken(data["refresh_token"])
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError("Token inválido.")
        return {}


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        User.objects.filter(email=value).exists()
        return value


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def validate_new_password(self, value):
        """ Aplica as regras de senha do Django """
        password_validation.validate_password(value)
        return value
