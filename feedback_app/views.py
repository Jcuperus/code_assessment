from django.shortcuts import render, reverse
from django.http import HttpResponse

from .forms import CodeUploadForm
from .assessment.utils import save_file, get_feedback

# Create your views here.
def index(request):

    if request.method == 'POST':
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            path = save_file(request.FILES['code_file'])
            feedback = get_feedback(path)

            return render(request, 'feedback/result.html', {'feedback': feedback})
    else:
        form = CodeUploadForm()

    return render(request, 'feedback/index.html', {'form': form})

def result(request):
    return render(request, 'feedback/result.html')