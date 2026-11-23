from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Calculation
from .forms import CalculationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import csv
from django.http import HttpResponse

class CalculationListView(LoginRequiredMixin, ListView):
    model = Calculation
    template_name = 'hydrolab/history.html'
    context_object_name = 'calculations'

    def get_queryset(self):
        # Разграничение ролей: если это суперпользователь (препод) - видит всё.
        # Если обычный юзер (студент) - только свои расчеты.
        if self.request.user.is_superuser:
            return Calculation.objects.all().order_by('-created_at')
        return Calculation.objects.filter(user=self.request.user).order_by('-created_at')

class CalculationCreateView(LoginRequiredMixin, CreateView):
    model = Calculation
    form_class = CalculationForm
    template_name = 'hydrolab/calc_form.html'
    success_url = reverse_lazy('history')

    def form_valid(self, form):
        # 1. Привязываем расчет к текущему пользователю
        form.instance.user = self.request.user
        
        # 2. Делаем расчет перед сохранением
        calc = form.save(commit=False)
        
        # Формула из ВКР 
        # ECD = density + (pressure_loss / (9.81 * depth))
        calc.pressure_loss = (calc.depth * calc.flow_rate * calc.density) / 1000000
        calc.ecd = calc.density + (calc.pressure_loss * 1000 / (9.81 * calc.depth)) if calc.depth > 0 else 0
        
        # Сохраняем в базу
        calc.save()
        return super().form_valid(form)

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # После регистрации отправляем на страницу входа

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CalculationUpdateView(LoginRequiredMixin, UpdateView):
    model = Calculation
    form_class = CalculationForm
    template_name = 'hydrolab/calc_form.html'
    success_url = reverse_lazy('history')
    def form_valid(self, form):
        calc = form.save(commit=False)
        
        # Пересчитываем ECD и потери давления
        calc.pressure_loss = (calc.depth * calc.flow_rate * calc.density) / 1000000
        calc.ecd = calc.density + (calc.pressure_loss * 1000 / (9.81 * calc.depth)) if calc.depth > 0 else 0
        
        calc.save()
        return super().form_valid(form)

class CalculationDeleteView(LoginRequiredMixin, DeleteView):
    model = Calculation
    template_name = 'hydrolab/calc_confirm_delete.html'
    success_url = reverse_lazy('history')

def chart_view(request):
    # Берем расчеты текущего пользователя (или все, если админ)
    if request.user.is_superuser:
        calcs = Calculation.objects.all().order_by('depth')
    else:
        calcs = Calculation.objects.filter(user=request.user).order_by('depth')
    
    # Готовим данные для графика: список глубин и список соответствующих ECD
    depths = [c.depth for c in calcs]
    ecds = [c.ecd for c in calcs]
    
    context = {
        'depths': depths,
        'ecds': ecds,
    }
    return render(request, 'hydrolab/chart.html', context)

def export_csv(request):
    # Создаем HTTP-ответ с типом файла CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig') # utf-8-sig нужен, чтобы Excel понял русские буквы
    
    # Указываем браузеру, что это файл для скачивания
    response['Content-Disposition'] = 'attachment; filename="hydrolab_report.csv"'
    
    # Создаем объект writer для записи CSV
    writer = csv.writer(response, delimiter=';') # Используем точку с запятой, так как Excel в русской локали ждет именно её
    
    # Пишем заголовки таблицы
    writer.writerow(['Скважина', 'Глубина (м)', 'Расход (л/с)', 'Плотность (кг/м³)', 'ECD (кг/м³)', 'Дата'])
    
    # Получаем данные (как и на странице истории: админ видит всё, юзер - только своё)
    if request.user.is_superuser:
        calculations = Calculation.objects.all().order_by('-created_at')
    else:
        calculations = Calculation.objects.filter(user=request.user).order_by('-created_at')
        
    # Записываем данные построчно
    for calc in calculations:
        writer.writerow([
            calc.well_name,
            calc.depth,
            calc.flow_rate,
            calc.density,
            round(calc.ecd, 2) if calc.ecd else '',
            calc.created_at.strftime('%d.%m.%Y %H:%M')
        ])
        
    return response