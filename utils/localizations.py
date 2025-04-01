CURRENT_LANGUAGE = 'en'

TRANSLATIONS = {
    'en': {
        'Sunday': 'Sun', 'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed',
        'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat',
        'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
        'May': 'May', 'June': 'Jun', 'July': 'Jul', 'August': 'Aug',
        'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec',
        'Holiday': 'Holiday'
    },
    'ko': {
        'Sunday': '일', 'Monday': '월', 'Tuesday': '화', 'Wednesday': '수',
        'Thursday': '목', 'Friday': '금', 'Saturday': '토',
        'January': '1월', 'February': '2월', 'March': '3월', 'April': '4월',
        'May': '5월', 'June': '6월', 'July': '7월', 'August': '8월',
        'September': '9월', 'October': '10월', 'November': '11월', 'December': '12월',
        'Holiday': '휴일'
    }
}

def _(key: str) -> str:
    return TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(key, key)

DAYS_OF_WEEK = [_(day) for day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']]
MONTHS_OF_YEAR = [_(month) for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']]