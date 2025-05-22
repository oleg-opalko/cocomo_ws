# from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.forms import inlineformset_factory

from .models import Project, ScaleDriver, CostDriver, ProjectScaleDriver, ProjectCostDriver
from .forms import ProjectForm, ProjectScaleDriverForm, ProjectCostDriverForm, ScaleDriverForm, CostDriverForm

def get_scale_driver_formset(*args, **kwargs):
    extra = kwargs.pop('extra', 0)
    can_delete = kwargs.pop('can_delete', False)
    return inlineformset_factory(
        Project,
        ProjectScaleDriver,
        form=ProjectScaleDriverForm,
        extra=extra,
        can_delete=can_delete
    )(*args, **kwargs)

def get_cost_driver_formset(*args, **kwargs):
    extra = kwargs.pop('extra', 0)
    can_delete = kwargs.pop('can_delete', False)
    return inlineformset_factory(
        Project,
        ProjectCostDriver,
        form=ProjectCostDriverForm,
        extra=extra,
        can_delete=can_delete
    )(*args, **kwargs)

class ProjectListView(ListView):
    model = Project
    template_name = 'main/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'main/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['results'] = project.get_calculation_results()
        context['scale_drivers'] = project.projectscaledriver_set.all()
        context['cost_drivers'] = project.projectcostdriver_set.all()
        return context

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'main/project_form.html'
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['scale_driver_formset'] = get_scale_driver_formset(self.request.POST, extra=ScaleDriver.objects.count())
            context['cost_driver_formset'] = get_cost_driver_formset(self.request.POST, extra=CostDriver.objects.count())
        else:
            initial_data = [{'scale_driver': sd.id, 'rating': 3} for sd in ScaleDriver.objects.all()]
            context['scale_driver_formset'] = get_scale_driver_formset(initial=initial_data, extra=ScaleDriver.objects.count())
            initial_data = [{'cost_driver': cd.id, 'rating': 3} for cd in CostDriver.objects.all()]
            context['cost_driver_formset'] = get_cost_driver_formset(initial=initial_data, extra=CostDriver.objects.count())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        scale_driver_formset = context['scale_driver_formset']
        cost_driver_formset = context['cost_driver_formset']

        if scale_driver_formset.is_valid() and cost_driver_formset.is_valid():
            self.object = form.save()
            scale_driver_formset.instance = self.object
            cost_driver_formset.instance = self.object
            scale_driver_formset.save()
            cost_driver_formset.save()
            messages.success(self.request, 'Project created successfully!')
            return redirect('project-detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'main/project_form.html'
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['scale_driver_formset'] = get_scale_driver_formset(self.request.POST, instance=self.object, extra=1, can_delete=True)
            context['cost_driver_formset'] = get_cost_driver_formset(self.request.POST, instance=self.object, extra=1, can_delete=True)
        else:
            existing_scale_drivers = set(self.object.projectscaledriver_set.values_list('scale_driver_id', flat=True))
            initial_scale = [
                {'scale_driver': sd.id, 'rating': 3}
                for sd in ScaleDriver.objects.exclude(id__in=existing_scale_drivers)
            ]
            context['scale_driver_formset'] = get_scale_driver_formset(
                instance=self.object,
                initial=initial_scale,
                extra=1,
                can_delete=True
            )

            existing_cost_drivers = set(self.object.projectcostdriver_set.values_list('cost_driver_id', flat=True))
            initial_cost = [
                {'cost_driver': cd.id, 'rating': 3}
                for cd in CostDriver.objects.exclude(id__in=existing_cost_drivers)
            ]
            context['cost_driver_formset'] = get_cost_driver_formset(
                instance=self.object,
                initial=initial_cost,
                extra=1,
                can_delete=True
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        scale_driver_formset = context['scale_driver_formset']
        cost_driver_formset = context['cost_driver_formset']

        if scale_driver_formset.is_valid() and cost_driver_formset.is_valid():
            self.object = form.save()
            scale_driver_formset.instance = self.object
            cost_driver_formset.instance = self.object
            scale_driver_formset.save()
            cost_driver_formset.save()
            messages.success(self.request, 'Project updated successfully!')
            return redirect('project-detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'main/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')

class ScaleDriverCreateView(CreateView):
    model = ScaleDriver
    form_class = ScaleDriverForm
    template_name = 'main/scale_driver_form.html'
    success_url = reverse_lazy('project-create')

class CostDriverCreateView(CreateView):
    model = CostDriver
    form_class = CostDriverForm
    template_name = 'main/cost_driver_form.html'
    success_url = reverse_lazy('project-create')

class ScaleDriverUpdateView(UpdateView):
    model = ScaleDriver
    form_class = ScaleDriverForm
    template_name = 'main/scale_driver_form.html'
    def get_success_url(self):
        return reverse('project-create')

class ScaleDriverDeleteView(DeleteView):
    model = ScaleDriver
    template_name = 'main/scale_driver_confirm_delete.html'
    def get_success_url(self):
        return reverse('project-create')

class CostDriverUpdateView(UpdateView):
    model = CostDriver
    form_class = CostDriverForm
    template_name = 'main/cost_driver_form.html'
    def get_success_url(self):
        return reverse('project-create')

class CostDriverDeleteView(DeleteView):
    model = CostDriver
    template_name = 'main/cost_driver_confirm_delete.html'
    def get_success_url(self):
        return reverse('project-create')

def index(request):
    return render(request, 'index.html')