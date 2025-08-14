from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer



class RegisterView(APIView):

    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role=data.get('role','normal'),
            )

            print(f'data : {data} \n user : {user}') # just for test

            return Response({'message':'user register was succesfull ...🍏'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    





# ---------------- bray RegisterView -----------------


    # user = User.objects.create_user khoby create_user ine pass hash mikne
    
    # def post(self,request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save
    #         return Response({'message':'user register was succesfull .'},status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



    # def post(self,request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save
    #         return Response(serializer.validated_data,status=status.HTTP_201_CREATED)