from rest_framework import serializers
from .models import User, Organisation

#Create serializers for User and Organisation.
class OrganisationSerializer(serializers.ModelSerializer):
  
    orgId = serializers.UUIDField(source='id', read_only=True)



    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    
    userId = serializers.UUIDField(source='id', read_only=True)



    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            password=validated_data['password'],
            phone=validated_data['phone']
        )
        # Create default organisation for the user
        organisation = Organisation.objects.create(name=f"{user.firstName}'s Organisation")
        organisation.users.add(user)
        return user


