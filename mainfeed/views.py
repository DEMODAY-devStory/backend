import operator
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from account.models import User
from profiles.models import Hashtag

from .serializers import *

class RecommendView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = RecommendSerializer

    def list(self, request, *args, **kwargs):
        my_profile = Profile.objects.get(user=self.request.user)
        my_hashtag = Hashtag.objects.filter(profile=my_profile).values_list('hashtag_name',flat=True)

        user_queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=kwargs['pk']).values_list('user', flat=True)
        following_queryset = User.objects.get(id=self.request.user).follower.values_list('following_id', flat=True)
        user_list = list(set(user_queryset)-set(following_queryset))
        
        commonhash_dict = {}
        for user in user_list:
            following_hashtag = Hashtag.objects.filter(profile=user).values_list('hashtag_name',flat=True)
            common = len(set(following_hashtag)&set(my_hashtag))
            commonhash_dict[user]=common

        commonhash_dict = dict(sorted(commonhash_dict.items(),key=operator.itemgetter(1),reverse=True))

        queryset = []
        for user in commonhash_dict:
            queryset.append(Profile.objects.get(user=user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset[:5], many=True)
        return Response(serializer.data)

'''
    def retrieve(self, request, *args, **kwargs):
        queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=kwargs['pk']) # 자기자신 제외 해시태그 갖고있는 사람들
        following_list = User.objects.get(id=self.request.user).follower.values_list('following_id', flat=True) # request user가 팔로우하고 있는 사람 리스트
        for i in following_list: queryset = queryset.exclude(user=i) # 리스트에서 한 명 씩 제거
        serializer = self.get_serializer(queryset[:5], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
'''
