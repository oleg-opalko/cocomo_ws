from django import forms
from django.forms import inlineformset_factory

from .models import Project, ProjectScaleDriver, ProjectCostDriver, ScaleDriver, CostDriver

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'model_family', 'size_kloc']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'size_kloc': forms.NumberInput(attrs={'step': '0.1'})
        }

class ProjectScaleDriverForm(forms.ModelForm):
    class Meta:
        model = ProjectScaleDriver
        fields = ['scale_driver', 'rating']
        widgets = {
            'scale_driver': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scale_driver'].queryset = ScaleDriver.objects.all()
        self.fields['scale_driver'].widget.attrs['readonly'] = True

ProjectScaleDriverFormSet = inlineformset_factory(
    Project,
    ProjectScaleDriver,
    form=ProjectScaleDriverForm,
    extra=0,
    can_delete=False
)

class ProjectCostDriverForm(forms.ModelForm):
    class Meta:
        model = ProjectCostDriver
        fields = ['cost_driver', 'rating']
        widgets = {
            'cost_driver': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cost_driver'].queryset = CostDriver.objects.all()
        self.fields['cost_driver'].widget.attrs['readonly'] = True

ProjectCostDriverFormSet = inlineformset_factory(
    Project,
    ProjectCostDriver,
    form=ProjectCostDriverForm,
    extra=0,
    can_delete=False
)

class ScaleDriverForm(forms.ModelForm):
    class Meta:
        model = ScaleDriver
        fields = ['name', 'description', 'weight']

class CostDriverForm(forms.ModelForm):
    class Meta:
        model = CostDriver
        fields = ['name', 'description', 'category', 'effort_multiplier'] 