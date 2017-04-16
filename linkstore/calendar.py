from datetime import datetime


class Calendar(object):
    DAY_MONTH_YEAR = '%d/%m/%Y'

    def date_of_today(self):
        return self._format_date(datetime.utcnow(), self.DAY_MONTH_YEAR)

    def _format_date(self, date, pattern):
        return date.strftime(pattern)
