class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'xp', 'streak', 'active', 'password', 'created_at', 'modified_at']
        read_only_fields = ['id', 'created_at', 'modified_at']

    def validate_email(self, value):
        """ Valida se o email tem domínio específico, caso necessário """
        if not value.endswith("@exemplo.com"):
            raise serializers.ValidationError("O email deve pertencer ao domínio 'exemplo.com'.")
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