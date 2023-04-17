from django.contrib import admin

from .models import (User, Category, Review, Comment,
                     Genre, Title, GenreTitle)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('date_joined',)
    empty_value_display = '-Пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    search_fields = ('id', 'name', 'slug')
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    search_fields = ('id', 'name', 'slug')
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'year', 'description')
    list_display_links = ('id', 'name', 'category', 'year')
    search_fields = ('name', 'year', 'description')
    list_filter = ('genre', 'category')


@admin.register(GenreTitle)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_id', 'title_id')
    list_display_links = ('id', 'genre_id', 'title_id')
    search_fields = ('id', 'genre_id', 'title_id')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_id', 'author', 'text', 'score', 'pub_date',)
    list_display_links = ('id', 'title_id', 'author', 'text', 'score', 'pub_date')
    search_fields = ('author__username', 'text', 'pub_date')
    list_filter = ('pub_date',)


@admin.register(Comment)
class ReviewComment(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date')
    list_display_links = ('id', 'text', 'author', 'pub_date')
    search_fields = ('author__username', 'text', 'pub_date')
    list_filter = ('pub_date',)
