import sqlite3
from datetime import datetime, timedelta


def get_booked_intervals(db_path, table_path, days):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем занятые интервалы
    cursor.execute(f"SELECT time_start, duration FROM {table_path} WHERE day = ?", (days,))
    booked_intervals = cursor.fetchall()

    conn.close()

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








