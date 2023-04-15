from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User, Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для GET-запроса к Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор для GET-запроса к Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для POST-запроса к Title."""
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'category', 'genre', 'description'
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """ Сериализатор для GET-запроса к Title."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'category', 'genre', 'description'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = "__all__"
        model = Review
        read_only_fields = ("author", "title", "rating",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("author",)


class AllcomentsSerializer(serializers.ModelSerializer): 
    author = serializers.StringRelatedField(read_only=True) 

    class Meta: 
        fields = "__all__"
        model = Comment 
