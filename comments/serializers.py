from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()  # its a read only field
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # gets the request context passed to 
        # CommentSerializer from the view
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    """
    we’ll use the rest  framework’s field level validation methods.  
    They’re called: validate_fieldName,  
    and in our case the field name is ‘image’,  so our method’s name will be validate_image.
    If we follow this naming convention,  this method will be called automatically  
    and validate the uploaded image every  time we create or update a post.
    """


    class Meta:
        model = Comment
        fields = [
            'id',  'owner', 'created_at', 'updated_at',
            'content', 'post', 'is_owner', 'profile_id', 'profile_image'
        ]


class CommentDetailSerializer (CommentSerializer):
    post = serializers.ReadOnlyField(source='post.id')