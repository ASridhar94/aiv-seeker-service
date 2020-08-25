from django.forms import ClearableFileInput, ModelForm

from workflow.models import Workflow, SequenceFile


class WorkflowModelForm(ModelForm):
    class Meta:
        model = Workflow
        fields = ['email', 'description']


class SequenceFileModelForm(ModelForm):
    class Meta:
        model = SequenceFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }
