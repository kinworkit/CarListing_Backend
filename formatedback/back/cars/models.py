from decimal import Decimal

from django.db import models
import requests
from django.utils.crypto import get_random_string


class VehicleModelYear(models.Model):
    year = models.IntegerField()
    mark = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.mark} {self.model} {self.year}"

    class Meta:
        verbose_name = "car model and year"
        verbose_name_plural = "car models and years"


class Cars(models.Model):
    # search info
    mark = models.CharField(max_length=50, null=True, verbose_name='Марка')
    model = models.CharField(max_length=50, null=True, verbose_name='Модель')
    year = models.IntegerField(null=True)
    price = models.IntegerField(verbose_name='Цена', null=True)
    city = models.CharField(max_length=30, null=True, verbose_name='Город')
    mileage = models.IntegerField(verbose_name='Пробег', null=True)
    color = models.CharField(max_length=100, verbose_name='Цвет', default='Чёрный')

    # publication info
    public_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации', null=True, blank=True)
    public_num = models.CharField(max_length=70, verbose_name='Номер обьявления', unique=True, null=True, blank=True)
    user = models.ForeignKey('caccounts.CustomUser', on_delete=models.CASCADE, default='')
    description = models.TextField(max_length=12000, null=True, verbose_name='Описание', blank=True)

    # General information
    brand_country = models.CharField(max_length=100, null=True, verbose_name='Страна марки', blank=True)
    doors = models.IntegerField(null=True, verbose_name='Количество дверей', blank=True)
    car_class = models.CharField(max_length=1, null=True, verbose_name='Класс автомобиля', blank=True)

    # Transmission and control
    transmission_type = models.CharField(max_length=30, null=True, verbose_name='Тип КПП', blank=True)
    number_of_gears = models.IntegerField(null=True, verbose_name='Количество передач', blank=True)
    drive = models.CharField(max_length=100, null=True, verbose_name='Привод', blank=True)

    # Operational performance
    fuel_grade = models.CharField(max_length=20, null=True, verbose_name='Марка топлива', blank=True)
    max_speed = models.IntegerField(null=True, verbose_name='Максимальная скорость', blank=True)
    acceleration_to_100_kmh = models.CharField(max_length=20, null=True, verbose_name='Разгон до 100 км/ч', blank=True)
    fuel_tank_capacity = models.IntegerField(null=True, verbose_name='ОбЪём топливного бака', blank=True)
    ecological_standard = models.CharField(max_length=30, null=True, verbose_name='Экологический стандарт', blank=True)
    fuel_cons_city_100 = models.CharField(max_length=20, null=True, verbose_name='Расход топлива в городе на 100 км', blank=True)
    fuel_cons_highway_100 = models.CharField(max_length=20, null=True, verbose_name='Расход топлива на шоссе на 100 км', blank=True)
    fuel_cons_mixed_cycle_100 = models.CharField(max_length=20, null=True, verbose_name="Расход топлива в смешанном цикле на 100 км", blank=True)

    # Suspension and brakes
    front_suspension = models.CharField(max_length=60, null=True, verbose_name='Передняя подвеска', blank=True)
    rear_suspension = models.CharField(max_length=60, null=True, verbose_name='Задняя подвеска', blank=True)
    front_brakes = models.CharField(max_length=60, null=True, verbose_name='Передние тормоза', blank=True)
    rear_brakes = models.CharField(max_length=60, null=True, verbose_name='Задние тормоза', blank=True)

    # Body
    body_type = models.CharField(max_length=30, null=True, verbose_name='Тип кузова', blank=True)
    number_of_seats = models.IntegerField(null=True, verbose_name='Количество мест', blank=True)
    length = models.IntegerField(null=True, verbose_name='Длина', blank=True)
    width = models.IntegerField(null=True, verbose_name='Ширина', blank=True)
    height = models.IntegerField(null=True, verbose_name='Высота', blank=True)
    wheelbase = models.IntegerField(null=True, verbose_name='Колёсная база', blank=True)
    curb_weight = models.IntegerField(null=True, verbose_name='Снаряженная масса', blank=True)
    wheel_size = models.CharField(max_length=200, null=True, verbose_name='Размер колёс', blank=True)
    ground_clearance = models.IntegerField(null=True, verbose_name='Дорожный просвет', blank=True)
    trunk_volume_min = models.IntegerField(null=True, verbose_name='Обьём багажника минимальный', blank=True)
    gross_weight = models.IntegerField(null=True, verbose_name='Полная масса', blank=True)
    front_track_width = models.IntegerField(null=True, verbose_name='Ширина передней колеи', blank=True)
    rear_track_width = models.IntegerField(null=True, verbose_name='Ширина задней колеи', blank=True)

    # Engine
    engine_type = models.CharField(max_length=25, null=True, verbose_name='Тип двигателя', blank=True)
    volume = models.CharField(max_length=25, null=True, verbose_name='Обём', blank=True)
    power = models.IntegerField(null=True, verbose_name='Мощность', blank=True)
    max_power_rpm = models.IntegerField(null=True, verbose_name='Обороты максимальной мощности', blank=True)
    max_torque = models.IntegerField(null=True, verbose_name='Максимальный крутящий момент', blank=True)
    max_torque_rpm = models.IntegerField(null=True, verbose_name='Обороты максимального крутящего момента', blank=True)
    intake_type = models.CharField(max_length=250, null=True, verbose_name='Тип впуска', blank=True)
    cylinder_arrangement = models.CharField(max_length=50, null=True, verbose_name='Расположение цилиндров', blank=True)
    number_of_cylinders = models.IntegerField(null=True, verbose_name='Кол-во цилиндров', blank=True)
    number_vales_per_cylinder = models.IntegerField(null=True, verbose_name='Кол-во клапанов на цилиндр', blank=True)
    compression_ratio = models.CharField(max_length=30, null=True, verbose_name='Степень сжатия', blank=True)
    type_of_supercharger = models.CharField(max_length=60, null=True, verbose_name='Тип наддува', blank=True)
    cylinder_diameter = models.IntegerField(null=True, verbose_name='Диаметр цилиндра', blank=True)
    piston_stroke = models.CharField(max_length=30, null=True, verbose_name='Ход поршня', blank=True)
    engine_layout = models.CharField(max_length=60, null=True, verbose_name='Расположение двигателя', blank=True)
    max_power_kW = models.IntegerField(null=True, verbose_name='Максимальная мощность (кВт)', blank=True)

    #status
    status = models.CharField(max_length=30, null=True, blank=True, verbose_name='Состояние')
    reg_country = models.CharField(max_length=30, null=True, blank=True, verbose_name='Страна регистрации')

    # Photo
    image1 = models.ImageField(upload_to='cars/', verbose_name='Фотография', null=True, blank=True)
    image2 = models.ImageField(upload_to='cars/', verbose_name='Фотография', null=True, blank=True)
    image3 = models.ImageField(upload_to='cars/', verbose_name='Фотография', null=True, blank=True)
    image4 = models.ImageField(upload_to='cars/', verbose_name='Фотография', null=True, blank=True)

    #title
    title = models.CharField(max_length=255, editable=False, default='')

    vehicle_model_year = models.ForeignKey(VehicleModelYear, on_delete=models.CASCADE, related_name='cars', null=True)

    class Meta:
        verbose_name = "Автомобили"
        verbose_name_plural = "Автомобили"

    def save(self, *args, **kwargs):
        if not self.public_num:
            self.public_num = self.generate_unique_public_num()
        for field_name in ['image1', 'image2', 'image3', 'image4']:
            image_field = getattr(self, field_name)
            if image_field:
                headers = {
                    'Authorization': f'your id',  # Imgur Client ID
                }

                files = {
                    'image': (image_field.name, image_field.file.read(), image_field.file.content_type),
                }

                response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

                if response.status_code == 200:
                    imgur_data = response.json()
                    imgur_link = imgur_data['data']['link']

                    # Удаляем префикс "https://"
                    if imgur_link.startswith("https://"):
                        imgur_link = imgur_link.replace("https://", "", 1)

                    setattr(self, field_name, imgur_link)
                else:
                    print(f'Не удалось загрузить изображение {field_name} на Imgur')

        self.title = f"Продажа {self.mark} {self.model}, {self.year} в городе {self.city}"
        super().save(*args, **kwargs)

    def generate_unique_public_num(self):
        """
        Generate unique ad number.
        """
        max_length = 8
        public_num = get_random_string(max_length)
        while Cars.objects.filter(public_num=public_num).exists():
            public_num = get_random_string(max_length)
        return public_num

    def formatted_price(self):
        return "{:,.0f}".format(self.price).replace(',', ' ')

    def set_price_from_formatted(self, price):
        self.price = int(price.replace(',', ''))

    def formatted_price_admin(self):
        return self.formatted_price()

    formatted_price_admin.short_description = 'Цена'
    formatted_price_admin.admin_order_field = 'price'

    def price_as_string(self):
        return str(self.formatted_mileage())

    def formatted_mileage(self):
        return "{:,.0f}".format(self.mileage).replace(',', ' ')

    def set_mileage_from_formatted(self, mileage):
        self.mileage = int(mileage.replace(',', ''))

    def formatted_mileage_admin(self):
        return self.formatted_mileage()

    formatted_mileage_admin.short_description = 'Пробег'
    formatted_mileage_admin.admin_order_field = 'mileage'

    def mileage_as_string(self):
        return str(self.formatted_mileage())


class Complect(models.Model):

    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='complects')

#Security system
    ABS = models.BooleanField(null=True, default=False, blank=True)
    ESP = models.BooleanField(null=True, default=False, blank=True)
    Anti_probuk = models.BooleanField(null=True, default=False, blank=True, verbose_name='Антипробуксовочная')
    Immobolaizer = models.BooleanField(null=True, default=False, blank=True, verbose_name='Иммоболайзер')
    Alarm = models.BooleanField(null=True, default=False, blank=True, verbose_name='Сигнализация')

#Poduszki
    pered = models.BooleanField(null=True, default=False, blank=True, verbose_name='Передние')
    bok = models.BooleanField(null=True, default=False, blank=True, verbose_name='Боковые')
    zadn = models.BooleanField(null=True, default=False, blank=True, verbose_name='Задние')

#Help system

    rain_scaner = models.BooleanField(null=True, default=False, blank=True, verbose_name='Датчик дождя')
    back_cam = models.BooleanField(null=True, default=False, blank=True, verbose_name='Камера заднего вида')
    parktr = models.BooleanField(null=True, default=False, blank=True, verbose_name='Парктроники')
    mirr_contr = models.BooleanField(null=True, default=False, blank=True, verbose_name='Контроль мертвых зон зеркал')

    def __str__(self):
        return f"Complect for {self.car.mark} {self.car.model}"