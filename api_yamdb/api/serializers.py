from rest_framework import serializers

from reviews.models import User, Category, Genre, Title, Review, Comment

###

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    

    class Meta:
        fields = "__all__"
        model = Review
        read_only_fields = ("author", "title",)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("author",)