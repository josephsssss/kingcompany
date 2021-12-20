from django.urls import register_converter


class YearConverter:
    regex = r"20\d{2}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


class MonthConverter(YearConverter):
    regex = r"20\d{1,2}"  #


class DayConverter(YearConverter):
    regex = r"[0123]\d"


register_converter(YearConverter, 'year')
