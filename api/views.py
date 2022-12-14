from datetime import date, timedelta
from rest_framework.response import Response
from .serializers import MeetingSerializer, RoomSerializer, TargetMail
from .models import Meeting, Room
from rest_framework.decorators import api_view
from rest_framework import status
from random import randint
from django.db.models import Q
from django.http import FileResponse
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .xlsxGenerator.tableGenerator import TableGenerator
from .xlsxGenerator.cleaner import clearAll 
import hashlib




@api_view(['GET'])
def downloadFile(request, id):
    
    if request.method=='GET':

        if id == 0:
            meetings = Meeting.objects.all()
            serializer = MeetingSerializer(meetings, many = True)
            return Response(serializer.data)

        try:    
            meetings =  Meeting.objects.filter(Q(room__id = id) & Q(type__exact = ('class')))
            
        except Meeting.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = MeetingSerializer(meetings, many = True)
        
        table=TableGenerator(data=serializer.data, title=id)
        clearAll(dirPath=table.getDir())
        table.setData()
        file=open(table.getFile(),'rb')
        response=FileResponse(file)

        return response    


@api_view(['GET', 'POST'])
def meeting_list(request, id):

    if request.method == 'GET':

        current_date = date.today()
        end_date = current_date + timedelta(days=90)
        start_date = current_date - timedelta(days=60)

        if id == 0:

            meetings = Meeting.objects.all()
            serializer = MeetingSerializer(meetings, many = True)
            return Response(serializer.data)

        try:    
            meetings =  Meeting.objects.filter(Q(room__id = id,status__exact = ('accepted')) & (Q(date__range=[start_date, end_date]) | Q(type__exact = ('class'))))
        except Meeting.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = MeetingSerializer(meetings, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MeetingSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            room = Room.objects.get(pk = id)

            message = Mail(
            from_email='ilkhom.c@outlook.com',
            to_emails="eku.ulanov@gmail.com",
            subject='A new event is creteated !',
            html_content=f'Recieved a new event request for {room}, go to https://ilkhom19.pythonanywhere.com/admin/ to "ACCEPT" or "DECLINE" the event')
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                sg.send(message)
            except Exception as e:
                return Response("Couldn't send email!", status=status.HTTP_408_REQUEST_TIMEOUT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

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

@api_view(['POST'])
def sendMail(request):
    targetMail=TargetMail(data=request.data)

    if targetMail.is_valid():
        address=targetMail.data['email']
        password=f'{randint(1000,9999)}'
        salt = os.environ.get('SALT')
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        message = Mail(
            from_email='ilkhom.c@outlook.com',
            to_emails=address,
            subject='Email Verification for RRS',
            html_content=f'Your Secret code is: {password}')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            return Response("Couldn't send email!", status=status.HTTP_408_REQUEST_TIMEOUT)
        return Response([address,hashed_password], status=status.HTTP_200_OK)
    else: return Response(targetMail.errors)
