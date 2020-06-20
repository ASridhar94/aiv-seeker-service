from django.shortcuts import render

from django.http import HttpResponse

from workflow.forms import WorkflowModelForm, SequenceFileModelForm
from workflow.models import SequenceFile


def index(request):
    return HttpResponse("Hello, world.")


def submit_workflow(request):
    if request.method == 'POST':
        form = WorkflowModelForm(request.POST)
        file_form = SequenceFileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        print(f"{form}")
        print(f"{files}")
        if form.is_valid() and file_form.is_valid():
            workflow = form.save(commit=False)
            workflow.save()
            for f in files:
                file_instance = SequenceFile(file=f, workflow=workflow)
                file_instance.save()
    else:
        form = WorkflowModelForm()
        file_form = SequenceFileModelForm()

    return render(request, 'submit_workflow.html', {'form': form, 'file_form': file_form})


def show_workflow(request):
    pass
