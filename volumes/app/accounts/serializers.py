from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    password1 = None
    password2 = None
    full_name = serializers.CharField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['full_name'] = self.validated_data.get('full_name', '')
        return data_dict

    def validate_password(self, value):
        # Check password strength
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        # Set password1 value from password
        attrs['password1'] = attrs.get('password')
        return attrs

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data.get('full_name')
        user.nick_name = user.full_name
        user.username = self.cleaned_data.get('email')
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('full_name', 'email', 'password')


class CustomLoginSerializer(LoginSerializer):
    username = None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = self._validate_email(email, password)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include \"email\" and \"password\".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        exclude = ('username', 'password', 'last_login', 'date_joined',
                   'create_at', 'updated_at', 'groups', 'user_permissions')

    def get_fields(self):
        fields = super().get_fields()
        try:
            user = self.context['request'].user
            if user.is_staff and not user.is_superuser:
                fields.pop('is_superuser', None)
                fields.pop('is_staff', None)
            elif not user.is_staff and not user.is_superuser:
                fields.pop('is_superuser', None)
                fields.pop('is_staff', None)
                fields.pop('is_active', None)
        except AttributeError:
            fields.pop('is_superuser', None)
            fields.pop('is_staff', None)
            fields.pop('is_active', None)

        return fields

    def run_validation(self, data=None):
        mutable_data = self.initial_data.copy()  # Create a mutable copy of the initial data
        instance = user = getattr(self, 'instance', None)
        exclude_list = getattr(self.Meta, 'exclude', ())

        # check permissions for fields based level of user
        if user.is_staff and not user.is_superuser:
            if 'is_staff' in mutable_data:
                msg = "You do not have permission to update the field \
                    'is_staff'."
                raise serializers.ValidationError(
                    {'is_staff': msg}, code='FORBIDDEN')
            if 'is_superuser' in mutable_data:
                msg = "You do not have permission to update the field \
                    'is_superuser'."
                raise serializers.ValidationError(
                    {'is_superuser': msg}, code='FORBIDDEN')
        if not user.is_staff and not user.is_superuser:
            if 'is_staff' in mutable_data:
                msg = "You do not have permission to update the field \
                    'is_staff'."
                raise serializers.ValidationError(
                    {'is_staff': msg}, code='FORBIDDEN')
            if 'is_superuser' in mutable_data:
                msg = "You do not have permission to update the field \
                    'is_superuser'."
                raise serializers.ValidationError(
                    {'is_superuser': msg}, code='FORBIDDEN')
            if 'is_active' in mutable_data:
                msg = "You do not have permission to update the field \
                    'is_active'."
                raise serializers.ValidationError(
                    {'is_active': msg}, code='FORBIDDEN')

        # check for extra field that not user access
        receive_fields = tuple(mutable_data.keys())
        for field in receive_fields:
            if field in exclude_list:
                msg = f"You do not have permission to update the \
                    field '{field}'."
                raise serializers.ValidationError(
                    {f'{field}': msg}, code='FORBIDDEN')

        # check if these three bolean not exist in receiving req
        # set default value from db
        if 'is_active' not in mutable_data and instance is not None:
            mutable_data['is_active'] = instance.is_active
        if 'is_superuser' not in mutable_data and instance is not None:
            mutable_data['is_superuser'] = instance.is_superuser
        if 'is_staff' not in mutable_data and instance is not None:
            mutable_data['is_staff'] = instance.is_staff

        return super().run_validation(mutable_data)


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    new_password1 = None
    new_password2 = None
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value,
                                              self.context['request'].user)
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password = self.validate_new_password(new_password)

        attrs['new_password1'] = new_password
        attrs['new_password2'] = new_password

        return attrs

    def save(self):
        password = self.validated_data['new_password1']
        self.context['request'].user.set_password(password)
        self.context['request'].user.save()
        return self.context['request'].user
