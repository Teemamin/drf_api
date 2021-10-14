from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    image_field = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()  # its a read only field
    is_liked = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # gets the request context passed to 
        # ProfileSerializer from the view
        request = self.context['request']
        return request.user == obj.owner

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            liked = Like.objects.filter(
                owner=user, post=obj
            ).first()
            # print(liked)
            return liked.id if liked else None
        return None

    """
    we’ll use the rest  framework’s field level validation methods.  
    They’re called: validate_fieldName,  
    and in our case the field name is ‘image’,  so our method’s name will be validate_image.
    If we follow this naming convention,  this method will be called automatically  
    and validate the uploaded image every  time we create or update a post.
    """
    def validate_image(self, value):
        # value is the uploaded image
        """
         check if the file size is  bigger than two megabytes. The default  
         file size unit is a byte. If  we multiply it by 1024, we’ll get kilobytes.  
         Multiplied again by 1024, we’ll get megabytes
        """
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    class Meta:
        model = Post
        fields = [
            'id', 'image', 'owner', 'created_at', 'updated_at', 'title',
            'content', 'image_field', 'is_owner', 'profile_id', 'image_filter', 'is_liked'
        ]
