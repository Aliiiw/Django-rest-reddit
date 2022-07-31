from django.shortcuts import render
from rest_framework import generics
from .models import Post
from .serializers import PostSerializers

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers