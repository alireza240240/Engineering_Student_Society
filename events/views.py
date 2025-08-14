from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsMemberOrAdmin
from .models import Event , EventParticipant
from .serializers import EventSeializer , RegisterEventSerializer



class EventListCreateView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly , IsMemberOrAdmin]

    def get(self,request):
        events = Event.objects.all()
        seializer = EventSeializer(events , many=True)
        return Response(seializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = EventSeializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class EventDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly , IsMemberOrAdmin]

    def get(self,request,pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSeializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSeializer(event,data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response({'message':'pak kardi 😆'},status=status.HTTP_204_NO_CONTENT)


class RegisterEventView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly ]# , IsMemberOrAdmin nmikhad dige normal ham mitone reg kone

    def post(self,request,pk):
        try :
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist :
            return Response({'error':'event does not exist ...❌'},status=status.HTTP_404_NOT_FOUND)

        if event.participants.count() >= event.capacity : # event.participant in mire to field event az model evpartc oj mid ba count() tedad mide
            return Response({'error':'The Event Capacity Is Compelete ...❌'},status=status.HTTP_400_BAD_REQUEST)
        
        if EventParticipant.objects.filter(event=event,user=request.user).exists():
            return Response({'error':'You Are Alredy Registered ... ❌'},status=status.HTTP_400_BAD_REQUEST)

        EventParticipant.objects.create(event=event,user=request.user)
        return Response({'message':'Succesfull Register Was Succesfull ...✅'},status=status.HTTP_201_CREATED)
        # inja dige estfd az srilzr lazem nist bra vght ke az karbar koli dade bgri to json alan bra skht EventParticipant ke chizi nmigrm hame ch lazm toye hamin view hast ham event hm user tnha vorodi lazm pk hst ke onam az url miad
        
