from rest_framework import serializers
from .models import Profile
from followers.models import Follower

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()  # its a read only field
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        # gets the request context passed to 
        # ProfileSerializer from the view
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        """
        If the logged in user is following this  profile an instance will be returned.
        If the logged in user is not following  this profile, None will be returned.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # print(f'{following} following')
            return following.id if following else None
        # If the user isn’t authenticated  at all, I’ll return None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]