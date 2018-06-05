from django.shortcuts import render, reverse, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse

from .forms import CodeUploadForm
from .models import Assessment
from .assessment.helpers import save_file, get_assessments

# Create your views here.
def index(request):

    if request.method == 'POST':
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            path = save_file(request.FILES['code_file'])
            assessments = get_assessments(path)

            return redirect(reverse('feedback:assessments'))
    else:
        form = CodeUploadForm()

    return render(request, 'feedback/index.html', {'form': form})

def result(request):
    return render(request, 'feedback/result.html')

def assessments(request):
    assessments = get_list_or_404(Assessment)
    return render(request, 'assessments/index.html', {'assessments': assessments })

def assessment_detail(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    return render(request, 'assessments/detail.html', {'assessment': assessment})