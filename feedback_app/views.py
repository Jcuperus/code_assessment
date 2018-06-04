from django.shortcuts import render, reverse
from django.http import HttpResponse

from .forms import CodeUploadForm
from .assessment.helpers import save_file, get_assessments

# Create your views here.
def index(request):

    if request.method == 'POST':
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            path = save_file(request.FILES['code_file'])
            assessments = get_assessments(path)

            return render(request, 'feedback/result.html', {'assessments': assessments})
    else:
        form = CodeUploadForm()

    return render(request, 'feedback/index.html', {'form': form})

def result(request):
    return render(request, 'feedback/result.html')