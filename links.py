import re

import aqt
from anki.hooks import wrap
from aqt import mw
from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from aqt.qt import QWidget
from aqt.stats import DeckStats


from aqt.qt import QDialog

from .config import hmd


# hmd stands for heat map data


dict  = {'Again': False, 'Easy': False, 'Good': False, 'Hard': False}

def heatmapLinkHandler(self, url, _old=None):
    """Launches Browser when clicking on a graph subdomain"""

    if ":" in url:
        (cmd, arg) = url.split(":", 1)
    else:
        cmd, arg = url, ""  #this is needed because linkhandler handles any links pressed in the deck browser screen

    if not cmd or cmd not in ( #this is needed because linkhandler handles any links pressed in the deck browser screen
            "hm_modeswitch",
            "hm_browse"
    ):
        return None if not _old else _old(self, url)

    if cmd == "hm_modeswitch":
        hmd.changeReview_type(arg)
        mw.reset()
        _old(self, url)

    elif (cmd == "hm_browse"):
        invokeBrowser(arg)



def invokeBrowser(search):
    browser = aqt.dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(search)
    browser.onSearchActivated()


def findRevlogEntriesEasy(self, val):
    """Find cards by revlog timestamp range"""
    args = val[0]
    cutoff1, cutoff2 = [int(i) for i in args.split(":")]

    return "c.id in (select cid from revlog where (id between %d and %d AND (ease = '4')))" % (
        cutoff1,
        cutoff2,
    )


def findRevlogEntriesGood(self, val):
    """Find cards by revlog timestamp range"""
    args = val[0]
    cutoff1, cutoff2 = [int(i) for i in args.split(":")]

    return "c.id in (select cid from revlog where (id between %d and %d AND (ease = '3')))" % (
        cutoff1,
        cutoff2,
    )


def findRevlogEntriesHard(self, val):
    """Find cards by revlog timestamp range"""
    args = val[0]
    cutoff1, cutoff2 = [int(i) for i in args.split(":")]

    return "c.id in (select cid from revlog where (id between %d and %d AND (ease = '2')))" % (
        cutoff1,
        cutoff2,
    )

def findRevlogEntriesAgain(self, val):
    """Find cards by revlog timestamp range"""
    args = val[0]
    cutoff1, cutoff2 = [int(i) for i in args.split(":")]
    aqt.utils.showText(args)
    return "c.id in (select cid from revlog where (id between %d and %d AND (ease = '1')))" % (
        cutoff1,
        cutoff2,
    )


def addFinders(self, col):
    """Add custom finder to search dictionary"""
    self.search["rid_Easy"] = self.findRevlogEntriesEasy
    self.search["rid_Hard"] = self.findRevlogEntriesHard
    self.search["rid_Good"] = self.findRevlogEntriesGood
    self.search["rid_Again"] = self.findRevlogEntriesAgain




def _find_cards_reviewed_between(start_date: int, end_date: int, review_type):
    # select from cards instead of just selecting uniques from revlog
    # in order to exclude deleted cards
    return mw.col.db.list(  # type: ignore
        "SELECT id FROM cards where id in "
        "(SELECT cid FROM revlog where (id between ? and ?) AND ease = ?)",
        start_date,
        end_date,
        review_type,
    )

_re_rid = re.compile(r"^rid.+:([0-9]+):([0-9]+)$")

def find_rid(search: str, review_type):
    match = _re_rid.match(search)

    if not match:
        return False

    start_date = int(match[1])
    end_date = int(match[2])

    return _find_cards_reviewed_between(start_date, end_date, review_type)

def on_browser_will_search(search_context):
    search = search_context.search
    if search.startswith("rid_Easy"):
        found_ids = find_rid(search, '4')
    elif search.startswith("rid_Good"):
        found_ids = find_rid(search, '3')
    elif search.startswith("rid_Again"):
        found_ids = find_rid(search, '1')
    elif search.startswith("rid_Hard"):
        found_ids = find_rid(search, '2')
    else:
        return

    if found_ids is False:
        return

    search_context.card_ids = found_ids




def initializeLinks():
    Overview._linkHandler = wrap(Overview._linkHandler, heatmapLinkHandler, "around")
    DeckBrowser._linkHandler = wrap(
        DeckBrowser._linkHandler, heatmapLinkHandler, "around"
    )
    DeckStats._linkHandler = heatmapLinkHandler

    try:
        from aqt.gui_hooks import browser_will_search
        browser_will_search.append(on_browser_will_search)
    except (ImportError, ModuleNotFoundError):

        from anki.find import Finder

        Finder.findRevlogEntriesAgain = findRevlogEntriesAgain
        Finder.findRevlogEntriesGood = findRevlogEntriesGood
        Finder.findRevlogEntriesEasy = findRevlogEntriesEasy
        Finder.findRevlogEntriesHard = findRevlogEntriesHard
        Finder.__init__ = wrap(Finder.__init__, addFinders, "after")


