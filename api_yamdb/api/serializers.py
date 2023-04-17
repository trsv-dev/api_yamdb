from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User, Category, Genre, Title, Review, Comment
from django.db.models import Avg
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueTogetherValidator


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
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """ Сериализатор для GET-запроса к Title."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(default=0)
    

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'category', 'genre', 'description', 'rating'
        )
        

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв для этого произведения.'
            )
        return data

        
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        
        
class AllcomentsSerializer(serializers.ModelSerializer): 
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta: 
        fields = "__all__"
        model = Comment


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username')
        read_only_fields = ['id', ]

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" зарезервировано в системе'
            )
        return data



class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ['id', ]