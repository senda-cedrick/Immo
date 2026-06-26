from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import AgenceForm, PersonnelForm
from .models import Agence, Personnel
from django.core.paginator import Paginator

class HomeView(TemplateView):
    template_name = 'index.html'

def home(request):
    return render(request, 'home.html')

class AgenceListView(ListView):
    model = Agence
    template_name = 'agences.html'
    context_object_name = 'pages'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Agence.objects.filter(nom__icontains=query).order_by('-id')
        return Agence.objects.all().order_by('-id')

class AgenceDetailView(DetailView):
    model = Agence
    template_name = 'agence_detail.html'
    context_object_name = 'agence'

def garanties(request):
    return render(request, 'garanties.html')

def appartements(request):
    return render(request, 'appartements.html')

def locataires(request):
    return render(request, 'locataires.html')

def personnels(request):
    return render(request, 'personnels.html')

def proprietaires(request):
    return render(request, 'proprietaires.html')


class AgenceCreateView(CreateView):
    model = Agence
    form_class = AgenceForm
    template_name = 'agence_form.html'
    success_url = reverse_lazy('agences')

    def form_valid(self, form):
        messages.success(self.request, "L'agence a été ajoutée avec succès !")
        return super().form_valid(form)

class AgenceUpdateView(UpdateView):
    model = Agence
    form_class = AgenceForm
    template_name = 'agence_form.html'
    success_url = reverse_lazy('agences')

    def form_valid(self, form):
        messages.success(self.request, "L'agence a été modifiée avec succès !")
        return super().form_valid(form)

class AgenceDeleteView(DeleteView):
    model = Agence
    template_name = 'agence_confirm_delete.html'
    success_url = reverse_lazy('agences')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "L'agence a été supprimée avec succès !")
        return super().delete(request, *args, **kwargs)


class PersonnelListView(ListView):
    model = Personnel
    template_name = 'personnels.html'
    context_object_name = 'pages'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Personnel.objects.filter(noms__icontains=query).order_by('-id')
        return Personnel.objects.all().order_by('-id')

class PersonnelDetailView(DetailView):
    model = Personnel
    template_name = 'personnel_detail.html'
    context_object_name = 'personnel'

class PersonnelCreateView(CreateView):
    model = Personnel
    form_class = PersonnelForm
    template_name = 'personnel_form.html'
    success_url = reverse_lazy('personnels')

    def form_valid(self, form):
        messages.success(self.request, "Le personnel a été ajouté avec succès !")
        return super().form_valid(form)

class PersonnelUpdateView(UpdateView):
    model = Personnel
    form_class = PersonnelForm
    template_name = 'personnel_form.html'
    success_url = reverse_lazy('personnels')

    def form_valid(self, form):
        messages.success(self.request, "Le personnel a été modifié avec succès !")
        return super().form_valid(form)

class PersonnelDeleteView(DeleteView):
    model = Personnel
    template_name = 'personnel_confirm_delete.html'
    success_url = reverse_lazy('personnels')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Le personnel a été supprimé avec succès !")
        return super().delete(request, *args, **kwargs)