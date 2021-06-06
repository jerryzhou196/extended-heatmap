
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import aqt

import datetime

from .platform import ANKI21
from aqt import mw


#all codes includes repeated presses AND learn/relearns

legend_factors = (0.125, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 4)

class Activity(object):
    def __init__(self, col):
        self.col = col
        self.offset = self._getColOffset()
        self.legend_factors = legend_factors

    def getEverything(self, review_type):
        everything = self._getDataAndLegendAndOffset(review_type)
        return everything

#----------------------------------------------

    def _getDataAndLegendAndOffset(self,review_type):
        raw_data = self._fetchRawDataFromDatabase(review_type)
        data_legend = self._setDynamicLegend(self._getAverage(raw_data))

        return {
            'data': raw_data,
            'legend': data_legend,
            'offset': self.offset,
             }

    def _fetchRawDataFromDatabase(self, review_type):
        offset = self.offset * 3600
        intial_cmd = "SELECT CAST(STRFTIME('%s', id/1000 - {}, 'unixepoch', 'localtime', 'start of day') as int) AS day, COUNT() FROM revlog WHERE (ease = '{}') GROUP BY DAY"

        reviewCode = {
            'Again': 1,
            'Hard': 2,
            'Good': 3,
            'Easy': 4
        }

        cmd = intial_cmd.format(offset, reviewCode[review_type])

        #Edit 2
        #Turns out that https://github.com/ankidroid/Anki-Android/wiki/Database-Structure is too old. They added a hard rating for new cards too so the ease values are way simplier. :(

        #Edit 1
        #https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
        #See Database-Structure for explanation

        # if (review_type == 'Hard'):
        #     hard_request = "ease = '2'"
        #     # "(ease = '2' AND type = '1') OR (ease = '2' AND type = '0') "
        #     cmd = intial_cmd.format(offset, hard_request)
        # elif (review_type == 'Easy'):
        #     easy_request = "ease = '4'"
        #     # (ease = '3' AND (type = '0' OR type = '2')) OR(ease='4' AND type = '1')
        #     cmd = intial_cmd.format(offset, easy_request)
        # elif (review_type == 'Good'):
        #     good_request = "ease = '3'"
        #     # "(ease = '3' AND (type = '1')) OR (ease = '2' AND (type = '0' OR type = '2'))"
        #     cmd = intial_cmd.format(offset, good_request)
        # else:
        #     again_request = "ease = '1'"
        #     cmd =  intial_cmd.format(offset, again_request)

        raw_data = self.col.db.all(cmd)
        return raw_data

    def _setDynamicLegend(self,average):
        avg = max(20, average)
        return [coefficient * avg for coefficient in self.legend_factors]

    def _getAverage(self, raw_data):
        total = 0
        days_learned = 1
        for idx, item in enumerate(raw_data):
            total += item[1]
            days_learned += 1
        avg = int(round(total / days_learned, 1))
        return avg

    def _getColOffset(self):
        """
        Return daily scheduling cutoff time in hours
        """

        if ANKI21 and self.col.schedVer() == 2:
            # aqt.utils.showText(str(self.col.conf.get("rollover", 4)))
            # aqt.utils.showText("ballsack")
            return self.col.conf.get("rollover", 4)
        start_date = datetime.datetime.fromtimestamp(self.col.crt)
        # aqt.utils.showText(str(datetime.datetime.fromtimestamp(self.col.crt).hour))
        # aqt.utils.showText("ballsack1")
        return start_date.hour













