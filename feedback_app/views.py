from django.shortcuts import render, reverse, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse

from .forms import CodeUploadForm
from .models import Assessment
from .assessment.helpers import save_file, assess

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tmp_file_paths = []
            for code_file in request.FILES.getlist('code_files'):
                path = save_file(code_file)
                tmp_file_paths.append(path)

            assessment = assess(tmp_file_paths)
            # TODO: delete/store files
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