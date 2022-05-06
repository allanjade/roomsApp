from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
#serializer import
from .serializers import RoomSerializer


@api_view(['GET']) #decorator
def getRoutes(request):
    routes = ['GET /api',
            'GET /api/rooms',
             'GET /api/rooms/:id'
    ]
    return Response(routes)

#get all rooms
@api_view(['GET'])
def getRooms(request):
    roomslist = Room.objects.all()
    #serialize the model data
    serializer = RoomSerializer(roomslist, many=True)
    return Response(serializer.data)

#get data a specific room
@api_view(['GET'])
def getRoom(request, pk):
    roomslist = Room.objects.get(id=pk)
    #serialize the model data
    serializer = RoomSerializer(roomslist, many=False)
    return Response(serializer.data)
