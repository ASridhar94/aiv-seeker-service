import os
import shutil
import subprocess
import tempfile
from subprocess import CalledProcessError

from celery import shared_task
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned

from workflow.models import SequenceFile, Workflow


AIV_SEEKER_PATH = "/Users/aishwaryasridhar/Documents/UBC docs/AIV/AIV_seeker/"
MEDIA_ROOT = settings.MEDIA_ROOT


@shared_task(track_started=True)
def start_aiv_seeker(workflow_id):
    try:
        workflow = Workflow.objects.get(id__exact=workflow_id)
        workflow.status = "RUNNING"
        workflow.save()
    except MultipleObjectsReturned:
        print(f"Multiple workflows found for ID: {workflow_id}")
        return
    except Workflow.DoesNotExist:
        print(f"Workflow ID: {workflow_id} not found")
        return

    sequence_files = SequenceFile.objects.filter(workflow_id=workflow_id)
    with tempfile.TemporaryDirectory() as sequence_dir, tempfile.TemporaryDirectory() as results_dir:
        print(f"Copying sequence files to {sequence_dir}")
        for f in sequence_files:
            print(f"Copying {f.name}")
            shutil.copy(os.path.join(MEDIA_ROOT, f.name), sequence_dir)

        # Run AIV_seeker in a subprocess.
        try:
            cmd = [os.path.join(AIV_SEEKER_PATH, 'AIV_Seeker.pl'), '-i', sequence_dir, '-o', results_dir]
            print(f"Running {' '.join(cmd)}")
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            print(output)
            # TODO Save results to DB.
            workflow.status = "SUCCESSFUL"
            workflow.save()
        except CalledProcessError as e:
            workflow.status = "FAILED"
            workflow.save()
    # TODO Should we delete the sequence files since we are done?
