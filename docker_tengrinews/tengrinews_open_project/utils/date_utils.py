import datetime


def parse_russian_date(date_str):
    if ':' not in date_str:
        date_str = f'{date_str} 00:00'
    # Russian month names mapping to their numeric values
    months = {
        'января': 1, 'февраля': 2, 'марта': 3,
        'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9,
        'октября': 10, 'ноября': 11, 'декабря': 12
    }
    
    # Current date
    today = datetime.datetime.now()
    
    # Handling relative dates
    if 'Сегодня' in date_str:
        date = today
        time_part = date_str.split()[1]
    elif 'Вчера' in date_str:
        date = today - datetime.timedelta(days=1)
        time_part = date_str.split()[1]
    else:
        # Splitting the date string by space
        day, month, year, time_part = date_str.split()
        day = int(day)
        year = int(year)
        month = months[month]
        date = datetime.datetime(year, month, day)
    
    # Parsing the time
    hour, minute = map(int, time_part.split(':'))
    
    # Combining date and time
    return datetime.datetime(date.year, date.month, date.day, hour, minute)
