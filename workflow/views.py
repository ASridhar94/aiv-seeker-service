from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from workflow.forms import WorkflowModelForm, SequenceFileModelForm
from workflow.models import SequenceFile, Workflow
from workflow.tasks import start_aiv_seeker


def index(request):
    return HttpResponse("Hello, world.")


def submit_workflow(request):
    if request.method == 'POST':
        form = WorkflowModelForm(request.POST)
        file_form = SequenceFileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            workflow = form.save(commit=False)
            workflow.save()
            for f in files:
                file_instance = SequenceFile(file=f, workflow=workflow)
                file_instance.save()
            task = start_aiv_seeker.apply_async(args=[workflow.id])
            workflow.task_id = task.id
            workflow.save()
        return HttpResponseRedirect(f'/workflows/submitted/{workflow.id}')
    else:
        form = WorkflowModelForm()
        file_form = SequenceFileModelForm()

    return render(request, 'submit_workflow.html', {'form': form, 'file_form': file_form})


def show_workflow(request, workflow_id):
    try:
        wf = Workflow.objects.get(id__exact=workflow_id)
    except MultipleObjectsReturned:
        return _show_error(request)
    except Workflow.DoesNotExist:
        return render(request, "workflow_not_found.html")
    except:
        return _show_error(request)

    return render(request, 'workflow_status.html', {"workflow_id": workflow_id, "status": wf.status, "output": ""})


def submitted(request, workflow_id):
    try:
        wf = Workflow.objects.get(id__exact=workflow_id)
    except MultipleObjectsReturned:
        return _show_error(request)
    except Workflow.DoesNotExist:
        return render(request, "workflow_not_found.html")
    except:
        return _show_error(request)

    return render(request, "thanks_for_submitting.html", {"workflow_id": workflow_id})


def _show_error(request):
    return render(request, "workflow_error.html")
