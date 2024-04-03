from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from news import models
from news.api import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dateutil import parser
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Refresh TokenObtainPairView (add user)
class AuthorizateView(TokenObtainPairView):
    serializer_class = serializers.AuthorizateSerializer
    
class RegistrationAPIView(generics.GenericAPIView):
    
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegistrationSerializer




    def post(self, request):
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)


        serializer.save()
        user=models.Author.objects.get(email=serializer.data['email'],)
        refresh = RefreshToken.for_user(user)
        return Response({'user':serializer.data,      
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)




class WeddingListCreateAPIVew(APIView):
    serializer_class = serializers.WeddingSerilizer
    permission_classes = (AllowAny,)
    
    def get(self, request):
        articles = models.Wedding.objects.all()
        serializer = serializers.WeddingSerilizer(articles, many=True)
        return Response(serializer.data)
    

class WeddingNameListAPIVew(APIView):
    serializer_class = serializers.WeddingNameSerilizer
    permission_classes = (AllowAny,)
    
    def get(self, request):
        articles = models.WeddingName.objects.all()
        serializer = serializers.WeddingNameSerilizer(articles, many=True)
        return Response(serializer.data)
    
class WeddingNameGetId(APIView):
    serializer_class = serializers.WeddingSerilizer

    def get(self,request,pk):
        try:
            queryset = self.get_queryset(pk)
        except ObjectDoesNotExist:
            return Response([{"error":"Токого поста не существует"},])
        serializer = serializers.WeddingSerilizer(queryset,many=True)

        return Response(serializer.data)

    def get_queryset(self,pk):
        
        return models.Wedding.objects.filter(WeddingName = models.WeddingName.objects.get(id = pk))
    

class WeddingNameGetId(APIView):
    serializer_class = serializers.WeddingSerilizer

    def get(self,request,pk):
        try:
            queryset = self.get_queryset(pk)
        except ObjectDoesNotExist:
            return Response([{"error":"Токого поста не существует"},])
        serializer = serializers.WeddingSerilizer(queryset,many=True)

        return Response(serializer.data)

    def get_queryset(self,pk):
        
        return models.Wedding.objects.filter(WeddingName = models.WeddingName.objects.get(id = pk))
    
class UserListViewAnalis(generics.GenericAPIView):
    
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)



    def get(self,request,pk):
    
        coming = models.Wedding.objects.filter(WeddingName = models.WeddingName.objects.get(id = pk),coming = True,spouse = False,I_cant_come=False).count()
        spouse = models.Wedding.objects.filter(WeddingName = models.WeddingName.objects.get(id = pk),spouse = True,coming = False ,I_cant_come =False).count()
        I_cant_come = models.Wedding.objects.filter(WeddingName = models.WeddingName.objects.get(id = pk),I_cant_come = True,coming = False,spouse = False).count()
        return Response({'coming':coming,'spouse':spouse,'I_cant_come':I_cant_come})   
    

class UserListView(generics.ListAPIView):
    queryset = models.Wedding.objects.all()
    serializer_class = serializers.WeddingSerilizer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,]
    search_fields = ['name']
    filterset_fields = ['WeddingName__id',]

class WeddingPostNews(generics.GenericAPIView):
    serializer_class = serializers.WeddingSerilizer
    permission_classes = (AllowAny,)
    
    def post(self,request):
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
       
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
  
          
    
class WeddingPostNewsExel(generics.GenericAPIView):
    serializer_class = serializers.WeddingSerilizer
    permission_classes = (AllowAny,)
    
    
    def post(self,request):
        pass
        # # Паттерн создания сериализатора, валидации и сохранения - довольно
        # # стандартный, и его можно часто увидеть в реальных проектах.
        
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        

        # # Путь к JSON-файлу с учетными данными
        # credentials = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\admin\\Desktop\\test\\comps.json')
        # client = gspread.authorize(credentials)

        # # Открываем таблицу
        # spreadsheet = client.open('NewDatabase')
        # worksheet = spreadsheet.worksheet('Sheet1')
        # rows = worksheet.get_all_values()

        # # Определяем номер последней строки
        # last_row_number = len(rows) + 1
        
        # coming = ''
        # spouse =''
        # I_cant_come = ''
        # if serializer.data['coming'] == True:
        #     coming = '✔'
        # if serializer.data['spouse'] == True:
        #     spouse = '✔'
        # if serializer.data['I_cant_come'] == True:
        #     I_cant_come = '✔'

        # # Заголовки таблицы
        # data = [serializer.data['name'],coming,spouse,I_cant_come, parser.parse(serializer.data['created_at']).strftime('%d-%m-%Y %H:%M:%S')]

        # worksheet.insert_row(data, last_row_number)

        # return Response(status=status.HTTP_201_CREATED)
  
