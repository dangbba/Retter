from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.files import File
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
#from backend.retter.settings import MEDIA_URL
from card.models import Card
from card.synthesis import synthesis

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from card.serializers import CardSerializer, AudioSerializer, CardCreateSerializer

from retter.settings import MEDIA_ROOT, MEDIA_URL


from moviepy.editor import *
from datetime import timedelta, datetime
from card.serializers import CardSerializer, AudioSerializer
from card.task import card_delete
from retter.settings import MEDIA_ROOT

from . import models
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.http.request import QueryDict
from background_task.models import Task
from .task import card_delete

import os
import shutil


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def card_detail(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'DELETE':
        if card_id == str(card.card_id).replace('-', ''):
            shutil.rmtree(MEDIA_ROOT + '\\' + card_id)
            card.delete()
            data = {
                'delete': f'카드 {card_id}가 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        if os.path.isdir(MEDIA_ROOT + "\\" + str(card.card_id).replace('-', '')) == False:
            os.mkdir(MEDIA_ROOT + "\\" + str(card.card_id).replace('-', ''))
        serializer = CardSerializer(card, data=request.data)
        serializer.image = request.FILES['image']
        # serializer.myvoice = request.FILES['myvoice']
        if serializer.is_valid(raise_exception=True):
            serializer.save(video = 'media/' + str(card.card_id).replace('-', '') + '/' + card_id + '.mp4')

        if card.audio != None:
            audio_clip = AudioFileClip(MEDIA_ROOT + '\\' + str(card.card_id).replace('-', '') + '\\' + card.audio)
        elif card.myvoice != None:
            audio_clip = AudioFileClip(MEDIA_ROOT + '\\' + card.myvoice.name)

        image_clip = ImageClip(MEDIA_ROOT + '\\' + card.image.name)
        
        video_clip = image_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.write_videofile(MEDIA_ROOT + '\\' + str(card.card_id).replace('-', '') + '\\' + card_id + ".mp4",  codec='mpeg4', audio_codec="aac", fps=24)

        # response = HttpResponse(video, content_type="video/mp4")
        # response['Content-Disposition'] = 'attachment; filename=' + card_id + '.mp4'
        return Response(status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        file_path = card.video
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open('', 'rb'), content_type="video/mp4")
        response['Content-Disposition'] = f'attachment; filename={card.video[6:]}'
        return response


# card_id 생성되는 코드
@api_view(['POST'])
def test(request):
    serializer = CardSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def voice(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'GET':
        if card.audio == None:
            file_path = os.path.join(MEDIA_ROOT, card.myvoice.name)
        else:
            file_path = card.audio

        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open('', 'rb'), content_type = "audio/wav")
        response['Content-Disposition'] = f'attachment; filename={file_path}'
        
        return response
    elif request.method == 'POST':
        card


@api_view(['POST'])
def record(request):
    pass

@api_view(["POST"])
def create_card(request):
    serializer = CardCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    
    card_id = serializer.data['card_id']
    card_id = card_id.replace('-', '')
    text = serializer.data['text']
    voice_num = serializer.data['voice_num']
    synthesis(text, card_id, voice_num)

    audio = MEDIA_URL + card_id+ '/' + card_id + '.wav'
    card = get_object_or_404(Card, card_id = card_id)
    card.audio = audio
    card.save()
    serializer = CardCreateSerializer(card)
    return Response(serializer.data, status=status.HTTP_200_OK)

@parser_classes([MultiPartParser, FormParser])
def record(request, *args, **kwargs):

        audio_data = request.data.dict()

        #file_name = request.data["file_name"]

        audio_data['myvoice'] = request.data['file_name']

        audio_query_dict = QueryDict('', mutable=True)
        audio_query_dict.update(audio_data)

        audio_serializer = AudioSerializer(data = audio_query_dict)
        if audio_serializer.is_valid(raise_exception=True):
            audio_serializer.save()

            return Response(status = status.HTTP_201_CREATED)
        else:
            return Response(audio_serializer.errors, status = status.HTTP_400_BAD_REQUEST)  


<<<<<<< HEAD
        #documents = models.Card.objects.all()

# def card_delete(request):
#     cards = get_list_or_404(Card)
#     for card in cards:
#         if card.created_at.replace(tzinfo=None) + timedelta(minutes=1) <= datetime.now():
#             card.delete()
#             print(datetime.now())
=======
@api_view(['GET'])
def delete_check(request):
    card_delete(repeat=Task.DAILY)
    return Response(status=status.HTTP_204_NO_CONTENT)
>>>>>>> 49a0bf7f0449f66f474a8ea9c4b5a7fb0995348b
