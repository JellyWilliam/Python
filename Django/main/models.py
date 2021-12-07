import json

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField
# from django.core.serializers.json import DjangoJSONEncoder


class CustomUser(AbstractUser):
    def __str__(self):
        return self.email


class ManagingOrganization(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название управляющей организации')

    def __str__(self):
        return self.name

    @property
    def request(self):
        return json.dumps(Request.objects.filter(manage_org=self).values())

    class Meta:
        verbose_name = "Управляющая организация"
        verbose_name_plural = "Управляющие организации"


class AdressForTarif(models.Model):
    manage_org = models.ForeignKey(ManagingOrganization, on_delete=models.CASCADE,
                                   verbose_name='Управляющая организация', related_name='ManagingOrganization')
    sity = models.CharField(max_length=20, verbose_name='Город')
    locality = models.CharField(max_length=20, verbose_name='Населённый пункт', blank=True, null=True)
    street = models.CharField(max_length=30, verbose_name='Улица')
    house = models.CharField(max_length=5, verbose_name='Дом')

    def __str__(self):
        if self.locality is None:
            return str(self.manage_org) + ', г.' + str(self.sity) + ', ул.' + str(self.street) + ', д.' + str(
                self.house)
        else:
            return str(self.manage_org) + ', г.' + str(self.sity) + ', нп.' + str(self.locality) + ', ул.' + str(
                self.street) + ', д.' + str(self.house)


class Request(models.Model):
    # Операции/Управление МКД

    APPLICANT_CHOICES = (
        ('Оператор', 'Оператор'),
        ('Арендатор', 'Арендатор'),
        ('Госорганы', 'Госорганы'),
        ('Жилец', 'Жилец'),
        ('Наниматель', 'Наниматель'),
        ('Родственник собственника', 'Радственник собственника'),
        ('Собственник', 'Собственник'),
        ('Организация', 'Организация')
    )

    STATUS_CHOICES = (
        ('Аварийная', 'Аварийная'),
        ('Плановая', 'Плановая'),
        ('Платная', 'Платная'),
        ('Консультация', 'Консультация')
    )

    WORK_CHOICES = (
        ('Благоустройство', 'Благоустройство'),
        ('Вентиляция', 'Вентиляция'),
        ('Газовое оборудование', 'Газовое оборудование'),
        ('Утечка газа', 'Утечка газа'),
        ('Горячее водоснабжение', 'Горячее водоснабжение'),
        ('Запорная армаратура', 'Запорная армаратура'),
        ('Канализация', 'Канализация'),
        ('Квитанция', 'Квитанция'),
        ('Кровля', 'Кровля'),
        ('Лифт', 'Лифт'),
        ('Лифт(кабина)', 'Лифт(кабина)'),
        ('Мусоропровод', 'Мусоропровод'),
        ('Конструктив', 'Конструктив'),
        ('Отопление', 'Отопление'),
        ('Отчет собственникам', 'Отчет собственникам'),
        ('Провайдер', 'Провайдер'),
        ('Уборка подъезда', 'Уборка подъезда'),
        ('Придомовая уборка', 'Придомовая уборка'),
        ('Холодное водоснабжение', 'Холодное водоснабжение'),
        ('Электричество', 'Электричество')
    )

    sity = models.CharField(max_length=20, verbose_name='Город')
    street = models.CharField(max_length=30, verbose_name='Улица')
    house = models.CharField(max_length=5, verbose_name='Дом')
    entrance = models.CharField(max_length=3, verbose_name='Подъезд', blank=True, null=True)
    appartament = models.CharField(max_length=10, verbose_name='Квартира', blank=True, null=True)
    applicant = models.CharField(max_length=30, verbose_name='Проживающий', choices=APPLICANT_CHOICES, default='Жилец')
    status = models.CharField(max_length=20, verbose_name='Статус заявки', choices=STATUS_CHOICES,
                              default='Консультация')
    text = models.TextField(verbose_name='Текст заявки')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
    work = models.CharField(max_length=50, verbose_name='Работы/Услуги', choices=WORK_CHOICES,
                            default='Благоустройство')

    # Связанная информация

    observing = models.ForeignKey('Worker', null=True, verbose_name='Исполнитель', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True, verbose_name='Дата заявки')
    manage_org = models.ForeignKey(ManagingOrganization, on_delete=models.CASCADE,
                                   verbose_name='Управляющая организация', related_name='ManagingOrganizationRequest')
    home_phone = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Домашний телефон', blank=True,
                                     null=True)
    mobile_phone = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Мобильный телефон', blank=True,
                                       null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Заявка АДС"
        verbose_name_plural = "Заявки АДС"


class Worker(models.Model):
    TYPE_CHOICES = (
        ('Работник', 'Работник'),
        ('Оператор', 'Оператор'),
        ('Администратор', 'Администратор')
    )

    observing = models.CharField(max_length=30, verbose_name='Работник')
    type = models.CharField(max_length=30, verbose_name='Должность', choices=TYPE_CHOICES)

    def __str__(self):
        return "{} {}".format(self.observing, self.type)

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"


class TarifPay(models.Model):
    location = models.CharField(max_length=50, verbose_name='Город/район')
    # 1.Текущий ремонт общего имущества
    deductions_for_maintenance_of_structural_elements_of_buildings_base_rate = models.DecimalField(
        db_column='deductions_for_maintenance',
        verbose_name='1.1.Отчисления на текущий ремонт конструктивных элементов зданий - базовая ставка', max_digits=7,
        decimal_places=5)
    # 1.2.Отчисления на текущий ремонт общего имущества, не находящегося на гарантийном обслуживании:
    G_out_sewerage_out_cold_water_and_out_hot_water = models.DecimalField(
        db_column='G_out_sewerage_out_cold_water_and_out_hot_water',
        verbose_name='1.2.Отчисления на текущий ремонт общего имущества, не находящегося на гарантийном обслуживании: \n 1.2.1. - общедомовых инженерных сетей в домах без канализации, без холодного водоснабжения и без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    G_out_sewerage_w_cold_water_and_out_hot_water = models.DecimalField(
        db_column='G_out_sewerage_w_cold_water_and_out_hot_water',
        verbose_name='1.2.2. - общедомовых инженерных сетей в домах без канализации, без горячего водоснабжения, с холодным водоснабжением',
        max_digits=7, decimal_places=5)
    G_w_sewerage_out_cold_water_and_out_hot_water = models.DecimalField(
        db_column='G_w_sewerage_out_cold_water_and_out_hot_water',
        verbose_name='1.2.3. - общедомовых инженерных сетей в домах с канализацией, с холодным водоснабжением, без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    G_w_sewerage_w_cold_water_and_w_hot_water = models.DecimalField(
        db_column='G_w_sewerage_w_cold_water_and_w_hot_water',
        verbose_name='1.2.4. - общедомовых инженерных сетей в домах с канализацией, с холодным и горячим водоснабжением',
        max_digits=7, decimal_places=5)
    G_indoor_hot_water_recirculation_pumps = models.DecimalField(
        verbose_name='1.2.5. - внутридомовых рециркуляционных насосов горячего водоснабжения', max_digits=7,
        decimal_places=5)
    G_over_10_floors = models.DecimalField(
        db_column='G_over_10_floors',
        verbose_name='1.2.6. - внутридомовых пожарных и пожарно-охранных сигнализаций в домах свыше 10 этажей',
        max_digits=7, decimal_places=5)
    G_in_house_automated_systems_for_commercial = models.DecimalField(
        db_column='G_in_house_automated_systems_for_commercial',
        verbose_name='1.2.7. - внутридомовых автоматизированных систем коммерческого учета электроэнергии и (или) теплоснабжения и (или) горячего водоснабжения и (или) холодного водоснабжения',
        max_digits=7, decimal_places=5)
    G_up_to_5000_sq_m = models.DecimalField(
        db_column='G_up_to_5000_sq_m',
        verbose_name='1.2.8. - узлов учета и (или) систем автоматического регулирования в домах площадью до 5000 кв. м',
        max_digits=7, decimal_places=5)
    G_metering_stations_and_or_automatic_control_systems_in_houses_with_an_area_of_over_5000_sq_m = models.DecimalField(
        db_column='G_over_5000_sq_m',
        verbose_name='1.2.9. - узлов учета и (или) систем автоматического регулирования в домах площадью свыше 5000 кв. м',
        max_digits=7, decimal_places=5)
    G_metering_units_and_or_automatic_control_systems_in_houses_with_an_area_of_over_8000_sq_m = models.DecimalField(
        db_column='G_over_8000_sq_m',
        verbose_name='1.2.10. - узлов учета и (или) систем автоматического регулирования в домах площадью свыше 8000 кв. м',
        max_digits=7, decimal_places=5)
    # 2.Содержание общего имущества
    # 2.1.Техническое обслуживание:
    TO_common_building_engineering_networks_in_houses_without_sewerage_without_cold_water_supply_and_without_hot_water_supply = models.DecimalField(
        db_column='TO_out_sewerage_out_cold_water_supply_and_out_hot_water_supply',
        verbose_name='2. Содержание общего имущества \n 2.1.	Техническое обслуживание: \n 2.1.1.	- общедомовых инженерных сетей в домах без канализации, без холодного водоснабжения и без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    TO_common_building_engineering_networks_in_houses_without_sewerage_without_hot_water_supply_with_cold_water_supply = models.DecimalField(
        db_column='TO_out_sewerage_w_cold_water_supply_and_out_hot_water_supply',
        verbose_name='2.1.2. - общедомовых инженерных сетей в домах без канализации, без горячего водоснабжения, с холодным водоснабжением',
        max_digits=7, decimal_places=5)
    TO_common_building_engineering_networks_in_houses_with_sewerage_system_with_cold_water_supply_without_hot_water_supply = models.DecimalField(
        db_column='TO_w_sewerage_w_cold_water_supply_and_out_hot_water_supply',
        verbose_name='2.1.3. - общедомовых инженерных сетей в домах с канализацией, с холодным водоснабжением, без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    TO_common_building_engineering_networks_in_houses_with_sewerage_with_cold_and_hot_water_supply = models.DecimalField(
        db_column='TO_w_sewerage_w_cold_water_supply_and_w_hot_water_supply',
        verbose_name='2.1.4. - общедомовых инженерных сетей в домах с канализацией, с холодным и горячим водоснабжением',
        max_digits=7, decimal_places=5)
    TO_roofs_attics_basements = models.DecimalField(verbose_name='2.1.5. - кровли, чердаков, подвалов', max_digits=7,
                                                    decimal_places=5)
    TO_indoor_gas_equipment = models.DecimalField(verbose_name='2.1.6. - внутридомового газового оборудования',
                                                  max_digits=7, decimal_places=5)
    TO_in_house_garbage_chutes = models.DecimalField(verbose_name='2.1.7. - внутридомовых мусоропроводов', max_digits=7,
                                                     decimal_places=5)
    TO_indoor_boilers = models.DecimalField(verbose_name='2.1.8. - внутридомовых бойлеров', max_digits=7,
                                            decimal_places=5)
    TO_indoor_hot_water_recirculation_pumps = models.DecimalField(
        verbose_name='2.1.9. - внутридомовых рециркуляционных насосов горячего водоснабжения', max_digits=7,
        decimal_places=5)
    TO_in_house_firefighters_and_fire_and_security_alarms_in_houses_over_10_floors = models.DecimalField(
        db_column='TO_over_10_floors',
        verbose_name='2.1.10. - внутридомовых пожарных и пожарно-охранных сигнализаций в домах свыше 10 этажей',
        max_digits=7, decimal_places=5)
    TO_in_house_automated_systems_for_commercial_metering_of_electricity_and_or_heat_supply_and_or_hot_water_supply_and_or_cold_water_supply = models.DecimalField(
        db_column='TO_in_house_automated_systems_for_commercial',
        verbose_name='2.1.11. - внутридомовых автоматизированных систем коммерческого учета электроэнергии и (или) теплоснабжения и (или) горячего водоснабжения и (или) холодного водоснабжения',
        max_digits=7, decimal_places=5)
    TO_metering_stations_and_or_automatic_control_systems_in_houses_with_an_area_of_up_to_5000_sq_m = models.DecimalField(
        db_column='TO_up_to_5000_sq_m',
        verbose_name='2.1.12.	- узлов учета и (или) систем автоматического регулирования в домах площадью до 5000 кв. м',
        max_digits=7, decimal_places=5)
    TO_metering_stations_and_or_automatic_control_systems_in_houses_with_an_area_of_over_5000_sq_m = models.DecimalField(
        db_column='TO_over_5000_sq_m',
        verbose_name='2.1.13. - узлов учета и (или) систем автоматического регулирования в домах площадью свыше 5000 кв. м',
        max_digits=7, decimal_places=5)
    TO_metering_units_and_or_automatic_control_systems_in_houses_with_an_area_of_over_8000_sq_m = models.DecimalField(
        db_column='TO_over_8000_sq_m',
        verbose_name='2.1.14.	- узлов учета и (или) систем автоматического регулирования в домах площадью свыше 8000 кв. м',
        max_digits=7, decimal_places=5)
    TO_technical_diagnostics_of_in_house_gas_equipment_VDGO_which_has_fulfilled_the_standard_operating_life = models.DecimalField(
        db_column='TO_VDGO',
        verbose_name='2.1.15.	- техническое диагностирование внутридомового газового оборудования (ВДГО), отработавшего нормативные сроки эксплуатации',
        max_digits=7, decimal_places=5)
    # 2.2. Технический осмотр:
    TS_common_building_engineering_networks_in_houses_without_sewerage_without_cold_water_supply_and_without_hot_water_supply = models.DecimalField(
        db_column='TS_out_sewerage_out_cold_water_supply_and_out_hot_water_supply',
        verbose_name='2.2. Технический осмотр: \n 2.2.1. - общедомовых инженерных сетей в домах без канализации, без холодного водоснабжения и без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    TS_common_building_engineering_networks_in_houses_without_sewerage_without_hot_water_supply_with_cold_water_supply = models.DecimalField(
        db_column='TS_out_sewerage_w_cold_water_supply_and_out_hot_water_supply',
        verbose_name='2.2.2. - общедомовых инженерных сетей в домах без канализации, без горячего водоснабжения, с холодным водоснабжением',
        max_digits=7, decimal_places=5)
    TS_common_building_engineering_networks_in_houses_with_sewerage_system_with_cold_water_supply_without_hot_water_supply = models.DecimalField(
        db_column='TS_w_sewerage_w_cold_water_supply_and_out_hot_water_supply',
        verbose_name='2.2.3. - общедомовых инженерных сетей в домах с канализацией, с холодным водоснабжением, без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    TS_common_building_engineering_networks_in_houses_with_sewerage_with_cold_and_hot_water_supply = models.DecimalField(
        db_column='TS_w_sewerage_w_cold_water_supply_and_w_hot_water_supply',
        verbose_name='2.2.4. - общедомовых инженерных сетей в домах с канализацией, с холодным и горячим водоснабжением',
        max_digits=7, decimal_places=5)
    TS_roofs_attics_basements = models.DecimalField(verbose_name='2.2.5. - кровли, чердаков, подвалов', max_digits=7,
                                                    decimal_places=5)
    TS_indoor_gas_equipment = models.DecimalField(verbose_name='2.2.6. - внутридомового газового оборудования',
                                                  max_digits=7, decimal_places=5)
    TS_indoor_hot_water_recirculation_pumps = models.DecimalField(
        verbose_name='2.2.7. - внутридомовых рециркуляционных насосов горячего водоснабжения', max_digits=7,
        decimal_places=5)
    TS_in_house_automated_systems_for_commercial_metering_of_electricity_and_or_heat_supply_and_or_hot_water_supply_and_or_cold_water_supply = models.DecimalField(
        db_column='automated_systems',
        verbose_name='2.2.8.	- внутридомовых автоматизированных систем коммерческого учета электроэнергии и (или) теплоснабжения и (или) горячего водоснабжения и (или) холодного водоснабжения',
        max_digits=7, decimal_places=5)
    # 2.3. Аварийное обслуживание:
    A_common_building_engineering_networks_in_houses_without_sewerage_without_cold_water_supply_and_without_hot_water_supply = models.DecimalField(
        db_column='A_out_s_out_cold_water_and_out_hot_water',
        verbose_name='2.3. Аварийное обслуживание: \n 2.3.1.	- общедомовых инженерных сетей в домах без канализации, без холодного водоснабжения и без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    A_common_building_engineering_networks_in_houses_without_sewerage_without_hot_water_supply_with_cold_water_supply = models.DecimalField(
        db_column='A_out_s_out_w_water_and_out_hot_water',
        verbose_name='2.3.2. - общедомовых инженерных сетей в домах без канализации, без горячего водоснабжения, с холодным водоснабжением',
        max_digits=7, decimal_places=5)
    A_common_building_engineering_networks_in_houses_with_sewerage_system_with_cold_water_supply_without_hot_water_supply = models.DecimalField(
        db_column='A_w_s_out_w_water_and_out_hot_water',
        verbose_name='2.3.3. - общедомовых инженерных сетей в домах с канализацией, с холодным водоснабжением, без горячего водоснабжения',
        max_digits=7, decimal_places=5)
    A_common_building_engineering_networks_in_houses_with_sewerage_with_cold_and_hot_water_supply = models.DecimalField(
        db_column='A_w_s_out_w_water_and_w_hot_water',
        verbose_name='2.3.4. - общедомовых инженерных сетей в домах с канализацией, с холодным и горячим водоснабжением',
        max_digits=7, decimal_places=5)
    A_roofs_attics_basements = models.DecimalField(verbose_name='2.3.5. - кровли, чердаков, подвалов', max_digits=7,
                                                   decimal_places=5)
    A_indoor_gas_equipment = models.DecimalField(verbose_name='2.3.6. - внутридомового газового оборудования',
                                                 max_digits=7, decimal_places=5)
    A_indoor_hot_water_recirculation_pumps = models.DecimalField(
        verbose_name='2.3.7. - внутридомовых рециркуляционных насосов горячего водоснабжения', max_digits=7,
        decimal_places=5)
    A_in_house_firefighters_and_fire_and_security_alarms_in_houses_over_10_floors = models.DecimalField(
        db_column='A_fire',
        verbose_name='2.3.8. - внутридомовых пожарных и пожарно-охранных сигнализаций в домах свыше 10 этажей',
        max_digits=7, decimal_places=5)
    A_in_house_automated_systems_for_commercial_metering_of_electricity_and_or_heat_supply_and_or_hot_water_supply_and_or_cold_water_supply = models.DecimalField(
        db_column='A_automated_systems',
        verbose_name='2.3.9. - внутридомовых автоматизированных систем коммерческого учета электроэнергии и (или) теплоснабжения и (или) горячего водоснабжения и (или) холодного водоснабжения',
        max_digits=7, decimal_places=5)
    # 2.4. Санитарное содержание и благоустройство:
    cleaning_of_the_local_area = models.DecimalField(
        verbose_name='2.4.	Санитарное содержание и благоустройство: \n 2.4.1. - уборка придомовой территории',
        max_digits=7, decimal_places=5)
    cleaning_of_yard_sanitary_installations = models.DecimalField(
        verbose_name='2.4.2. - уборка дворовых санитарных установок', max_digits=7, decimal_places=5)
    cleaning_staircases = models.DecimalField(verbose_name='2.4.3. - уборка лестничных клеток', max_digits=7,
                                              decimal_places=5)
    cleaning_of_elevators = models.DecimalField(verbose_name='2.4.4. - уборка лифтов', max_digits=7, decimal_places=5)
    pest_control_and_disinfestation = models.DecimalField(verbose_name='2.4.5. - дератизация и дезинсекция',
                                                          max_digits=7, decimal_places=5)
    improvement_of_the_local_area_including_the_demolition_of_emergency_trees = models.DecimalField(
        db_column='improvement_of_the_local_area',
        verbose_name='2.4.6. - благоустройство придомовой территории, включая снос аварийных деревьев', max_digits=7,
        decimal_places=5)
    maintenance_of_playgrounds_and_sports_grounds = models.DecimalField(
        verbose_name='2.4.7. - содержание детских и спортивных площадок', max_digits=7, decimal_places=5)
    sand_replacement_in_sandboxes = models.DecimalField(verbose_name='2.4.8. - замена песка в песочницах', max_digits=7,
                                                        decimal_places=5)
    removal_of_ice_and_icicles_from_roofs = models.DecimalField(
        verbose_name='2.4.9. - удаление наледей и сосулек с крыш', max_digits=7, decimal_places=5)
    # 2.5. Сбор и вывоз бытовых отходов:
    organization_and_maintenance_of_places_sites_for_the_accumulation_of_solid_municipal_waste_including_maintenance_and_cleaning = models.DecimalField(
        db_column='organization_and_maintenance',
        verbose_name='2.5.	Сбор и вывоз бытовых отходов: \n 2.5.1. - организация и содержание мест (площадок) накопления твердых коммунальных отходов, включая обслуживание и очист',
        max_digits=7, decimal_places=5)
    removal_of_liquid_household_waste = models.DecimalField(verbose_name='2.5.4. - вывоз жидких бытовых отходов',
                                                            max_digits=7, decimal_places=5)
    # 2.6. Содержание локальных котельных:
    maintenance_of_local_boiler_houses = models.DecimalField(
        verbose_name='2.6.	Содержание локальных котельных: \n 2.6.1. - техническое обслуживание локальных котельных',
        max_digits=7, decimal_places=5)
    current_repair_of_local_boiler_houses = models.DecimalField(
        verbose_name='2.6.2. - текущий ремонт локальных котельных', max_digits=7, decimal_places=5)
    # 2.7. Содержание лифтового хозяйства в домах, где все подъезды оборудованы лифтами:
    maintenance_and_repair_of_elevators = models.DecimalField(
        verbose_name='2.7. Содержание лифтового хозяйства в домах, где все подъезды оборудованы лифтами: \n 2.7.1. - техническое обслуживание и ремонт лифтов',
        max_digits=7, decimal_places=5)
    maintenance_and_repair_of_dispatching_facilities = models.DecimalField(
        verbose_name='2.7.2. - техническое обслуживание и ремонт средств диспетчеризации', max_digits=7,
        decimal_places=5)
    maintenance_and_repair_of_fire_and_or_security_alarm_systems_for_elevators = models.DecimalField(
        db_column='maintenance_and_repair',
        verbose_name='2.7.3. - техническое обслуживание и ремонт пожарной и (или) охранной сигнализации лифтов',
        max_digits=7, decimal_places=5)
    periodic_technical_inspection_of_elevators_with_electrical_measurements = models.DecimalField(
        db_column='periodic_technical',
        verbose_name='2.7.4. - периодическое техническое освидетельствование лифтов с проведением электроизмерений',
        max_digits=7, decimal_places=5)
    expert_examination_survey_of_elevators_that_have_worked_out_the_standard_assigned_service_life = models.DecimalField(
        db_column='expert_examination_survey',
        verbose_name='2.7.5. - экспертное обследование (освидетельствование) лифтов, отработавших нормативный (назначенный) срок службы',
        max_digits=7, decimal_places=5)
    # 3. Плата за управление многоквартирным домом:
    houses_without_centralized_drainage = models.DecimalField(
        verbose_name='3. Плата за управление многоквартирным домом: \n 3.1. - дома без централизованного водоотведения',
        max_digits=7, decimal_places=5)
    houses_with_centralized_drainage_without_centralized_hot_water_supply = models.DecimalField(
        db_column='with_centralized_drainage',
        verbose_name='3.2. - дома с централизованным водоотведением, без централизованного горячего водоснабжения',
        max_digits=7, decimal_places=5)
    houses_with_centralized_sewerage_and_hot_water_supply = models.DecimalField(db_column='with_centralized_sewerage',
                                                                                verbose_name='3.3. - дома с централизованным водоотведением и горячим водоснабжением',
                                                                                max_digits=7,
                                                                                decimal_places=5)
    houses_without_elevators_equipped_with_garbage_chutes = models.DecimalField(
        db_column='out_elevators_equipped_w_garbage_chutes',
        verbose_name='3.4. - дома без лифтов, оборудованные мусоропроводами', max_digits=7, decimal_places=5)
    houses_without_elevators_equipped_with_local_boiler_houses = models.DecimalField(
        db_column='out_elevators_equipped_w_local_boiler',
        verbose_name='3.5.	- дома без лифтов, оборудованные локальными котельными', max_digits=7, decimal_places=5)
    houses_without_garbage_chutes_equipped_with_lifts = models.DecimalField(
        db_column='out_garbage_chutes_equipped_w_lifts',
        verbose_name='3.6. - дома без мусоропроводов, оборудованные лифтами', max_digits=7, decimal_places=5)
    houses_equipped_with_garbage_chutes_and_elevators = models.DecimalField(
        db_column='equipped_w_garbage_chutes_and_elevators',
        verbose_name='3.7. - дома, оборудованные мусоропроводами и лифтами', max_digits=7, decimal_places=5)
    houses_equipped_with_garbage_chutes_elevators_and_local_boiler_houses = models.DecimalField(
        db_column='equipped_w_garbage_chutes_elevators_and_local_boiler',
        verbose_name='3.8. - дома, оборудованные мусоропроводами, лифтами и локальными котельными', max_digits=7,
        decimal_places=5)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "Тарифы"
        verbose_name_plural = "Тарифы"


class AddSteamShop(models.Model):
    name_steam_shop = models.CharField(max_length=50, verbose_name='Наименование котельной')
    street = models.CharField(max_length=50, verbose_name='Улица')
    locality = models.CharField(max_length=50, verbose_name='Населенный пункт')
    district = models.CharField(max_length=50, verbose_name='Район')
    region = models.CharField(max_length=50, verbose_name='Область')
    code = models.CharField(max_length=50, verbose_name='Код')
    attachment = models.CharField(max_length=50, verbose_name='Принадлежность')

    def __str__(self):
        return str(self.id) + ' ' + self.name_steam_shop

    class Meta:
        verbose_name = "Паспорт котельной"
        verbose_name_plural = "Паспорта котельных"


class AddBuilding(models.Model):
    name_building = models.CharField(max_length=50, verbose_name='Наименование')
    year_build = models.DateField(max_length=50, verbose_name='Год постройки')
    number_of_storeys = models.DecimalField(verbose_name='Этажность', max_digits=7, decimal_places=2)
    total_area = models.DecimalField(verbose_name='Общая площадь', max_digits=7, decimal_places=2)
    construction_volume = models.DecimalField(verbose_name='Строительный объём', max_digits=7, decimal_places=2)
    commissioning_year = models.DateField(max_length=50, verbose_name='Год ввода в эксплуатацию')
    date_of_last_examination = models.CharField(max_length=50, verbose_name='Дата последней экспертизы')
    conclusion = models.CharField(max_length=50, verbose_name='Заключение')
    wear_percentage = models.DecimalField(verbose_name='Процент износа', max_digits=7, decimal_places=2)
    building_structure_type = models.CharField(max_length=50, verbose_name='Тип конструкции здания')

    def __str__(self):
        return str(self.id) + ' ' + self.name_building + ' ' + str(self.year_build)

    class Meta:
        verbose_name = "Паспорт здания"
        verbose_name_plural = "Паспорта зданий"


class TarifBuild(models.Model):
    manage_org = models.CharField(max_length=30, verbose_name='Управляющая организация')
    adress = models.CharField(max_length=100, verbose_name='Адрес')
    tarif = ArrayField(JSONField(), verbose_name='Тариф')
    sum = models.DecimalField(verbose_name='Сумма', max_digits=30, decimal_places=20)
    tarifGen = models.DecimalField(verbose_name='Тариф за 1 кв.м', max_digits=5, decimal_places=2)
    square = models.DecimalField(verbose_name='Площадь', max_digits=10, decimal_places=2)
    date = models.CharField(verbose_name='Дата', max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.manage_org) + ', ' + self.adress

    class Meta:
        verbose_name = "Тарифы зданий"
        verbose_name_plural = "Тарифы зданий"


class News(models.Model):
    slug = models.SlugField(verbose_name='Метка')
    title = models.CharField(verbose_name='Заголовок', max_length=50)
    description = models.CharField(verbose_name='Описание', max_length=250)
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(verbose_name='Фотография', null=True, blank=True)
    url = models.URLField(verbose_name='Ссылка на статью', null=True, blank=True)
    author = models.CharField(verbose_name='Автор', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = "Новости"
