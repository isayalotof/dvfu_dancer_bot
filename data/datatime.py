from data.data_base import c
from datetime import datetime, timedelta


def get_booked_intervals(table_path, days):
    # Подключаемся к базе данных
    cursor = c

    # Получаем занятые интервалы
    cursor.execute(f"SELECT time_start, duration FROM {table_path} WHERE day = ?", (days,))
    booked_intervals = cursor.fetchall()

    # Преобразуем в список временных интервалов
    busy_times = []
    for start_time, duration in booked_intervals:
        start = datetime.strptime(start_time, '%H:%M')
        end = start + timedelta(hours=duration)
        busy_times.append((start, end))

    return busy_times


def create_time_slots(start_time, end_time):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time)
        current_time += timedelta(minutes=30)
    return slots


def get_available_slots(booked_intervals):
    start_time = datetime.strptime("10:00", "%H:%M")
    end_time = datetime.strptime("22:00", "%H:%M")

    # Генерируем временные слоты
    time_slots = create_time_slots(start_time, end_time)

    available_slots = []

    for slot in time_slots:
        slot_end = slot + timedelta(minutes=30)

        # Проверяем, свободен ли слот
        is_busy = False
        for start, end in booked_intervals:
            if slot < end and slot_end > start:
                is_busy = True
                break

        if not is_busy:
            available_slots.append(slot)

    return available_slots


def calculate_available_durations(start_time_user, booked_intervals):
    max_duration = timedelta(hours=3)
    end_time_user = start_time_user + max_duration

    # Найти ближайшее занятое время после начала записи
    for booked_start, booked_end in booked_intervals:
        if booked_start >= start_time_user:
            if booked_start < end_time_user:
                max_duration = booked_start - start_time_user
            break

    # Определяем доступные длительности (каждые 30 минут)
    available_durations = []
    current_duration = timedelta(minutes=30)
    while current_duration <= max_duration:
        available_durations.append(current_duration)
        current_duration += timedelta(minutes=30)

    return available_durations


def get_remaining_days_of_week():
    # Получаем текущую дату
    today = datetime.now()
    # Получаем текущий день недели (0 - понедельник, 6 - воскресенье)
    current_weekday = today.weekday()

    # Список дней недели
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    # Получаем список оставшихся дней включая сегодняшний
    remaining_days = days_of_week[current_weekday:]

    return remaining_days


def get_date_of_weekday(weekday_name):
    # Словарь для сопоставления названий дней недели с их номерами
    weekdays = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    # Получаем текущую дату
    today = datetime.now()
    current_weekday = today.weekday()  # 0 - понедельник, 6 - воскресенье

    target_weekday = weekdays[weekday_name]

    # Вычисляем разницу между текущим днем и целевым днем
    days_difference = target_weekday - current_weekday

    target_date = today + timedelta(days=days_difference)

    return target_date.date().strftime("%d/%m/%Y")


def get_russia_day(weekday_name):
    weekdays = {
        ('Monday',): "Понедельник",
        ('Tuesday',): "Вторник",
        ('Wednesday',): "Среду",
        ('Thursday',): "Четверг",
        ('Friday',): "Пятницу",
        ('Saturday',): "Субботу",
        ('Sunday',): "Воскресенье"
    }

    return weekdays[weekday_name]


def get_my_records(user_name):
    places = ['Place1', 'Place2', 'Place3', 'Place4']
    days = []
    cursor = c
    for place in places:
        dai = cursor.execute(f"""SELECT day 
        FROM {place} 
        WHERE username = {user_name}""").fetchall()
        k = dai
        if len(k) > 0:
            days.append([f'{get_russia_day(k[0])}', f'{place}'])
    if len(days) > 0:
        return days
    else:
        days.append('У вас нет ни одной записи')
        return days
