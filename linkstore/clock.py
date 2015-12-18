from datetime import datetime


class Clock(object):
    def date_of_today(self):
        return self._convert_date_to_string_with_pattern(
            self._get_current_utc_date(),
            '%d/%m/%Y'
        )

    def _get_current_utc_date(self):
        return datetime.utcnow()

    def _convert_date_to_string_with_pattern(self, date, pattern):
        return date.strftime(pattern)
