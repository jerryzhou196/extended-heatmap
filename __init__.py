
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from anki.hooks import wrap

from aqt.qt import *

import aqt

from aqt import mw
from aqt.overview import Overview
from aqt.deckbrowser import DeckBrowser
from aqt.stats import DeckStats
from anki.stats import CollectionStats
from anki.hooks import addHook, remHook

from .activity import Activity
from anki.utils import json
import sys
from . import qrc_resources

from .config import hmd

from .links import initializeLinks





css = """ 
<style> 

    .jumbotron {
    padding-top: 30px;
    padding-bottom: 30px;
    margin-bottom: 30px;
    color: inherit;
    background-color: #eee;
    }

    .jumbotron h1 {
    font-size: 63px;
    }

    .container {
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
    }


    .jumbotron p {
    margin-bottom: 15px;
    font-size: 21px;
    font-weight: 200;
    }

    label {
    display: inline-block;
    max-width: 100%;
    margin-bottom: 5px;
    font-weight: 700;
    }   
    p {
    margin: 0 0 10px;
    }

    * {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    }

    .lead {
    margin-bottom: 20px;
    font-size: 16px;
    font-weight: 300;
    line-height: 1.4;
    }

    .jumbotron .container {
    max-width: 100%;
    }

    button, input, select, textarea {
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
    }
    button, select {
    text-transform: none;
}
button, input, optgroup, select, textarea {
    margin: 0;
    font: inherit;
    color: inherit;
}


    body {
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-size: 14px;
    line-height: 1.42857143;
    color: #333;
    background-color: #fff;
    }


    .jumbotron h1 {
    font-size: 63px;
}

.jumbotron .h1, .jumbotron h1 {
    color: inherit;
}
.h1, h1 {
    font-size: 36px;
}
.h1, .h2, .h3, h1, h2, h3 {
    margin-top: 20px;
    margin-bottom: 10px;
}
.h1, .h2, .h3, .h4, .h5, .h6, h1, h2, h3, h4, h5, h6 {
    font-family: inherit;
    font-weight: 500;
    line-height: 1.1;
    color: inherit;
}




</style>"""

html_heatmap = """


    <script>
    var pybridge = function(arg){{{{
        pycmd(arg);
    }}}};
    </script>   

   <script type="text/javascript" src="http://d3js.org/d3.v3.min.js"></script>   
   <script type="text/javascript" src="http://cdn.jsdelivr.net/cal-heatmap/3.3.10/cal-heatmap.min.js"></script>   
   <link rel="stylesheet" href="http://cdn.jsdelivr.net/cal-heatmap/3.3.10/cal-heatmap.css" />   
   <script type="text/javascript" src="qrc:/more_heatmap.js"></script>
   <script src="https://kit.fontawesome.com/881c8798ee.js" crossorigin="anonymous"></script>
   <link rel="stylesheet" href="qrc:/more_heatmap.css"/>

{css}
<body style = "text-align: center;">   

<div id = "container" style = "margin-top: 1em; zoom: 100%; text-align: center; display: flex; justify-content: center; align-items: center; ">
    <!-- Put this into Container to visualize border -> border-style: solid; border-color: red; border-inline-width: 5px; #999-->
    <div id="cal-heatmapzzzz" style = "margin-right: 3em; margin-top: 3em;"> 
         <div style = "margin-bottom: 20px;">    
            <button onclick="more_cal.previous();" style="margin-bottom: 5px;" class="btn-xs"><i class="fas fa-chevron-circle-left"></i></button>    
            <button onclick="more_cal.next();" style="margin-bottom: 5px;" class="btn-xs"><i class="fas fa-chevron-circle-right"></i></button>    
         </div>     
    </div>   
    <div class="jumbotron" style = " width: 450px; color: #999; background-color: #222222; border-radius: 10px;">
        <div class="container" style = "text-align: left;">
          <h1 class="display-4" style = 'margin-left: 20px;'>
            <label for="rated" > <span style = "color: white;"> Displaying </span><br> cards rated  </label><br>
            <div name = "selector" = "border-color:#2f2f31; ">
                <select name="rated" onchange = "testest()" id="rated" style = "outline: none; background-color: #2f2f31; border-radius: 10px;">
                <option {select_again} style = "outline: none;" value="Again">Again</option>
                <option {select_easy} style = "outline: none;" value="Easy">Easy</option>
                <option {select_hard} style = "outline: none;" value="Hard">Hard</option>
                <option {select_good} style = "outline: none;" value="Good">Good</option>
                </select>
            </div>
        </h1>
          <p class="lead" style = "margin-left: 20px;">From a month ago. </p>
        </div>
      </div>
</div>



</body>



<script type="text/javascript">
    more_cal = initMoreHeatmap({data},{legend},{offset});
</script>


"""



def checkIfSelected(name,type):
    if name != type:
        return ""
    else:
        return "Selected"


def deckbrowserRenderStats(self, _old):
    ret = _old(self)
    a = Activity(mw.col)
    selected = hmd.getReview_type()

    everything = a.getEverything(selected)



    formated_hm = html_heatmap.format(
        css = css,
        data = json.dumps(dict(everything['data'])),
        legend =json.dumps(everything['legend']),
        select_again= checkIfSelected(selected, 'Again'),
        select_easy= checkIfSelected(selected, 'Easy'),
        select_hard= checkIfSelected(selected, 'Hard'),
        select_good= checkIfSelected(selected, 'Good'),
        offset = everything['offset'],
     )
    return ret +  formated_hm


def initializeViews():
    DeckBrowser._renderStats = wrap(
        DeckBrowser._renderStats, deckbrowserRenderStats, "around")


initializeViews()
initializeLinks()

# < script
# type = "text/javascript" >
# var
# cal = new
# CalHeatMap();
# cal.init({
#     domain: "month",
#     subDomain: "day",
#     cellSize: 50,
#     itemName: ["service ticket", "service tickets"],
#     data: {
#         "1452019700": 40,
#         "1454688100": 50,
#         "1452710900": 5,
#         "1452883700": 15,
#         "1453142900": 15,
#         "1453488500": 30,
#         "1456239700": 80,
#         "1453662300": 20,
#         "1455130100": 60,
#         "1455562100": 70,
#         "1455131100": 10,
#         "1456166900": 30,
#         "1456399000": 12,
#         "1451674100": 90
#     },
#     subDomainTextFormat: "%d",
#     range: 1,
#     itemSelector: "#cal-heatmapzzzz",
#     start: new Date(2016, 01, 01),
#     displayLegend: false
# });
# < / script >