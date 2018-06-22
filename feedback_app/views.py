from django.shortcuts import render, reverse, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.uploadhandler import TemporaryFileUploadHandler

from .forms import CodeUploadForm
from .models import Assessment
from .assessment.helpers import assess, get_tmp_file_paths

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tmp_file_paths = get_tmp_file_paths(request.FILES.getlist('code_files'))
            assessment = assess(tmp_file_paths)
            return HttpResponseRedirect(reverse('feedback:assessment_detail', kwargs={'assessment_id': assessment.id}))
    else:
        form = CodeUploadForm()

    return render(request, 'feedback/index.html', {'form': form})

def result(request):
    return render(request, 'feedback/result.html')

def assessments(request):
    assessments = get_list_or_404(Assessment)
    return render(request, 'assessments/index.html', {'assessments': assessments})

def assessment_detail(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    return render(request, 'assessments/detail.html', {'assessment': assessment})