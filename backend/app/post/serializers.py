import bs4
import requests
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from webpreview import web_preview
from app.post.models import Post, ClapPost, Comment, CodeSnippet, Website, ClapComment

user = get_user_model()


class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = ['code', 'prog_language']


class UserPostSerializer(serializers.ModelSerializer):
    logged_in_user_is_following = serializers.SerializerMethodField()

    def get_logged_in_user_is_following(self, user):
        return user in self.context['request'].user.followees.all()

    class Meta:
        model = user
        fields = ['id', 'username', 'avatar', 'logged_in_user_is_following']


class CommentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True)
    is_from_logged_in_user = SerializerMethodField()
    logged_in_user_clapped = SerializerMethodField()

    def get_logged_in_user_clapped(self, comment):
        user = self.context['request'].user
        if user == comment.user:
            return False
        if comment in Comment.objects.filter(claps__user=user, post=comment.post):
            return True
        return False

    def get_is_from_logged_in_user(self, comment):
        user = self.context['request'].user
        if user == comment.user:
            return True
        return False

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created', 'claps', 'user', 'post', 'is_from_logged_in_user', 'logged_in_user_clapped']
        read_only_fields = ['id', 'created', 'claps']


class WebsiteSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['url', 'title', 'description', 'image_url']


class ClapPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClapPost
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    code_snippet = CodeSnippetSerializer(read_only=True)
    website = WebsiteSerilaizer(read_only=True)
    claps = ClapPostSerializer(many=True, read_only=True)
    logged_in_user_bookmarked = SerializerMethodField()
    logged_in_user_clapped = SerializerMethodField()

    def get_logged_in_user_bookmarked(self, post):
        user = self.context['request'].user
        if user == post.user:
            return False
        if post in user.bookmarked_posts.all():
            return True
        return False

    def get_logged_in_user_clapped(self, post):
        user = self.context['request'].user
        if user == post.user:
            return False
        if post in Post.objects.filter(claps__user=user):
            return True
        return False

    class Meta:
        model = Post
        fields = ['id', 'bookmarked_by', 'content', 'category',
                  'check_to_save', 'created', 'comments', 'claps', 'user',
                  'code_snippet', 'website', 'shared', 'logged_in_user_bookmarked', 'logged_in_user_clapped']

        read_only_fields = ['id', 'created', 'user', 'bookmarked_by', 'claps', 'saved_website']

    def create_code_snippet(self, data):
        data = data.pop('snippet', None)
        if data:
            serializer = CodeSnippetSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return instance
        return None

    def create_website(self, data):
        url = data.get('website', None)['url']
        should_save = data.get("check_to_save", False)

        if url and should_save:
            req = requests.get(url)
            html = req.content

            tree = bs4.BeautifulSoup(html, 'lxml')

            body = tree.body
            if body is None:
                return None

            for tag in body.select('script'):
                tag.decompose()
            for tag in body.select('style'):
                tag.decompose()

            text = body.get_text(separator='\n')

            title, description, image = web_preview(url)

            instance = Website.objects.create(url=url, title=title, description=description,
                                              image_url=image, saved_website=text)
            return instance
        return None

    def create(self, validated_data):
        data = self.context['request'].data

        validated_data['code_snippet'] = self.create_code_snippet(data=data)
        validated_data['website'] = self.create_website(data=data)
        validated_data['user'] = self.context['request'].user

        post = super().create(validated_data=validated_data)
        return post
