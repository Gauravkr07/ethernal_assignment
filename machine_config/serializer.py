from rest_framework import serializers
from machine_config.models import  Machine, MachineData
from django.contrib.auth.models import User,Group

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class MachineDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineData
        fields = '__all__'

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     password_confirm = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password_confirm', 'email')

#     def validate(self, data):
#         if data['password'] != data['password_confirm']:
#             raise serializers.ValidationError({"password": "Passwords must match."})
#         return data

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             email=validated_data['email']
#         )
#         return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('Manager', 'Manager'), ('Supervisor', 'Supervisor'), ('Operator', 'Operator')])

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'role')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        # For providing role to user inserted according to position
        group, created = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        return user
