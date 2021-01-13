from rest_framework import serializers

from custom_user.models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    company_name = serializers.CharField(max_length=60, required=True)

    class Meta:
        model = User
        fields = ('email', 'company_name', 'username', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def save(self, *args, **kwargs):
        new_user = User(username=self.validated_data['username'],
                        email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': "Passwords must match"})
        new_user.set_password(password)
        new_user.save()
        return new_user
