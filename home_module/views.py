from django.shortcuts import render
from facerecognition_module.forms import FaceRecognitionForm

# Create your views here.
from facerecognition_module.models import FaceRecognition
from facerecognition_module.machinelearning import pipeline_model
from django.conf import settings


def home_view(request):
    face_recognition_form = FaceRecognitionForm()

    if request.method == 'POST':
        face_recognition_form = FaceRecognitionForm(request.POST or None, request.FILES or None)
        if face_recognition_form.is_valid():
            face_recognition_data = face_recognition_form.save(commit=True)
            # extract image from db
            primary_key = face_recognition_data.pk
            image_obj = FaceRecognition.objects.get(pk=primary_key)
            results = pipeline_model(image_obj.image.path)

            context = {
                'form': face_recognition_form,
                'upload': True,
                'results': results
            }
            return render(request, 'index.html', context)

    context = {
        'form': face_recognition_form,
        'upload': False
    }
    return render(request, 'index.html', context)
