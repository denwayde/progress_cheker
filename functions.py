from datetime import datetime, timedelta,date

def is_date_in_current_week(date_to_check):
    # Получаем текущую дату
    today = date.today()
    
    # Определяем первый день недели (понедельник)
    start_of_week = today - timedelta(days=today.weekday())
    
    # Определяем последний день недели (воскресенье)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Сравниваем даты
    return start_of_week <= date_to_check <= end_of_week




# date_to_check = datetime(2024,11, 6)  # Замените на нужную дату
# print(date_to_check)
# if is_date_in_current_week(date_to_check):
#     print(f"Дата {date_to_check.date()} входит в текущую неделю.")
# else:
#     print(f"Дата {date_to_check.date()} не входит в текущую неделю.")

# today = datetime.now()
# start_of_week = today - timedelta(days=today.weekday())

# strdate = date.today()
# print(datetime(strdate))
# print(date.fromisoformat(strdate)==date.today())