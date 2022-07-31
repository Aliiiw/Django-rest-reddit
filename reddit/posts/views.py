from turtle import pos
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Post, Vote
from .serializers import PostSerializers, VoteSerializers


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
        

class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You have voted before!")
        serializer.save(voter=self.request.user, post= Post.objects.get(pk=self.kwargs['pk']))
        
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("You have never voted on this Post!")
            
        
        