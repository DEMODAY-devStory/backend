from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class UserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            # 데이터가 unique하지 않음
            return Response(data={'message': "이미 가입된 회원입니다"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # 기타 오류 (발생하지 않을 것으로 추정)
            return Response(exception=Exception)

        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

# @method_decorator(csrf_exempt, name='dispatch')
# class UserLoginView(GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         user = serializer.validate(request.data)

#         if user is None:
#             response = {
#                 "success": "false",
#                 "status_code": status.HTTP_200_OK,
#                 "id": "",
#             }
#         else:
#             try:
#                 img = UserImg.objects.get(user_id=user.id).image
#             except:
#                 img = ""
#             response = {
#                 "success": "true",
#                 "status_code": status.HTTP_200_OK,
#                 "id": user.id,
#                 "img": str(img),
#             }

#         return Response(response, status=status.HTTP_200_OK)
