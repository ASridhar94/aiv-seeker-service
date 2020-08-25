import os
import shutil
import subprocess
import tempfile
from subprocess import CalledProcessError

from celery import shared_task
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned

from workflow.models import SequenceFile, Workflow


AIV_CONDA_PATH = '/root/anaconda3'
AIV_CONDA_EXEC = os.path.join(AIV_CONDA_PATH, 'bin/conda')
AIV_CONDA_ENV = 'aiv_seeker'
AIV_SEEKER_PATH = os.path.join("/AIV_seeker", 'AIV_Seeker.pl')
AIV_SEEKER_OUTPUT_PATH = os.path.join('/opt/static', 'output')
MEDIA_ROOT = settings.MEDIA_ROOT


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    return out, err


@shared_task(track_started=True)
def start_aiv_seeker(workflow_id):
    print(f"Starting task for workflow ID: {workflow_id}")
    try:
        workflow = Workflow.objects.get(id=workflow_id)
        workflow.status = "RUNNING"
        workflow.save()
    except MultipleObjectsReturned:
        print(f"Multiple workflows found for ID: {workflow_id}")
        return
    except Workflow.DoesNotExist:
        print(f"Workflow ID: {workflow_id} not found")
        return

    sequence_files = SequenceFile.objects.filter(workflow_id=workflow_id)
    results_dir = os.path.join(AIV_SEEKER_OUTPUT_PATH, str(workflow_id))
    with tempfile.TemporaryDirectory() as sequence_dir:
        print(f"Copying sequence files to {sequence_dir}")
        for f in sequence_files:
            print(f"Copying {f.file.name}")
            shutil.copy(os.path.join(MEDIA_ROOT, f.file.name), sequence_dir)

        # Run AIV_seeker in a subprocess.
        try:
            cmds = f"""
            {AIV_CONDA_EXEC} run -n {AIV_CONDA_ENV} perl {AIV_SEEKER_PATH} -i {sequence_dir} -o {results_dir}
            """
            out, err = subprocess_cmd(cmds)
            print(out)
            # TODO Save results to DB.
            workflow.status = "SUCCESSFUL"
            workflow.save()
        except CalledProcessError as e:
            workflow.status = "FAILED"
            workflow.save()
    # TODO Should we delete the sequence files since we are done?
