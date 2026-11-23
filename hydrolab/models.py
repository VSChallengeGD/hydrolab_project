from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Calculation(models.Model):
    # Поля из ВКР
    well_name = models.CharField(max_length=100, verbose_name="Название скважины")
    depth = models.FloatField(
        validators=[MinValueValidator(0.1)], 
        verbose_name="Глубина по стволу (м)"
    )
    flow_rate = models.FloatField(
        validators=[MinValueValidator(0.1)], 
        verbose_name="Расход раствора (л/с)"
    )
    density = models.FloatField(
        validators=[MinValueValidator(0.1)], 
        verbose_name="Плотность раствора (кг/м³)"
    )
    
    # Поля для реологии (модель Гершеля-Балкли)
    tau0 = models.FloatField(verbose_name="Предельное напряжение сдвига (Па)", default=2.0)
    k_cons = models.FloatField(verbose_name="Коэффициент консистенции (Па·сⁿ)", default=1.5)
    n_index = models.FloatField(verbose_name="Индекс течения", default=0.8)

    # Результаты расчета (заполняются автоматически в views.py)
    pressure_loss = models.FloatField(verbose_name="Потери давления (МПа)", null=True, blank=True)
    ecd = models.FloatField(verbose_name="Эквивалентная плотность ECD (кг/м³)", null=True, blank=True)
    
    # Системные поля
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата расчета")

    def __str__(self):
        return f"{self.well_name} - {self.created_at.strftime('%Y-%m-%d')}"

class MudProperty(models.Model):
    # Справочник растворов 
    name = models.CharField(max_length=100, verbose_name="Название раствора")
    description = models.TextField(blank=True, verbose_name="Описание")
    density = models.FloatField(verbose_name="Базовая плотность (кг/м³)")

    def __str__(self):
        return self.name