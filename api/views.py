from datetime import date, timedelta
from rest_framework.response import Response
from .serializers import MeetingSerializer, RoomSerializer
from .models import Meeting, Room
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET', 'POST'])
def meeting_list(request, id):

    if request.method == 'GET':

        current_date = date.today()
        end_date = current_date + timedelta(days=60)
        start_date = current_date - timedelta(days=30)

        if id == 0:

            meetings = Meeting.objects.all()
            serializer = MeetingSerializer(meetings, many = True)
            return Response(serializer.data)

        try:    
            meetings =  Meeting.objects.filter(room_id__id = id, date__range=[start_date, end_date])
        except Meeting.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = MeetingSerializer(meetings, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MeetingSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def meeting_detail(request, id):

    try:    
       meeting =  Meeting.objects.get(pk=id)
    except Meeting.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MeetingSerializer(meeting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def room_list(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    return Response(serializer.data)