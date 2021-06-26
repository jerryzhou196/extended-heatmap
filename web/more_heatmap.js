function tzOffsetByTimestamp(timestamp) {
    date = new Date(timestamp * 1000);
    return date.getTimezoneOffset() * 60;
}

function applyDateOffset(date) {
    return new Date(date.getTime() + date.getTimezoneOffset() * 60 * 1000);
}

function getLastMonth() {

     var x = new Date();
     x.setDate(0); // 0 will result in the last day of the previous month
     x.setDate(1);
     return x;
    //We just need to get a date a month and sometime before that for the minimum month to be on the month before
}



class SelectedRating {
    constructor(default_option){
        this.rating = default_option;
    }
    changeRating(rating){
        this.rating = rating;
    }
    getRating() {
        return this.rating;
    }
}

var rating = new SelectedRating('Again');


function onChangedSelector(){
   var x = document.getElementById("rated").value;
   pybridge('hm_modeswitch:' + x);
}


//function encodeSelectedRating(x){
//    switch(x) {
//        case 'Again':
//            return '1';
//        case 'Hard':
//            return '2';
//        case 'Good':
//            return '3';
//        case 'Easy':
//            return '4';
//        }
//
//}


function initMoreHeatmap(data,legend,offset,stringCellSize) {
    var more_cal = new CalHeatMap();
    var calTodayDate = applyDateOffset(new Date());
    var lastMonth = getLastMonth();

    var cellSize = parseInt(stringCellSize,10);


     more_cal.init({
               domain: "month",
               subDomain: "day",
               cellSize: cellSize,
               itemName: ["cards", "cards"],
               data: data,
               minDate: lastMonth,
               maxDate: new Date(),
               subDomainTextFormat: "%d",
               range: 1,
               legend: legend,
               tooltip: true,
               itemSelector: "#cal-heatmapzzzz",
               displayLegend: false,
               afterLoadData: function afterLoadData(timestamps) {
                    var results = {};
                    for (var timestamp in timestamps) {
                        var value = timestamps[timestamp];
                        timestamp = parseInt(timestamp, 10);
                        results[timestamp + tzOffsetByTimestamp(timestamp)] = value;
                       };
                    return results;
                },

                onClick: function (date, nb) {
                    cmd = ""

                    if (nb === null || nb == 0) {
                        // No cards for that day. Preserve highlight and return.
                        more_cal.highlight(new Date()); return;
                    }
                    today = new Date(calTodayDate);
                    today.setHours(0, 0, 0);  // just a precaution against
                                              // calTodayDate not being zeroed
                    diffSecs = Math.abs(today.getTime() - date.getTime()) / 1000;
                    diffDays = Math.round(diffSecs / 86400);
                    diffDayMinusOne = diffDays - 1

                    cutoff1 = date.getTime() + offset * 3600 * 1000;
                    cutoff2 = cutoff1 + 86400 * 1000;
                    cmd += "rid_" + document.getElementById("rated").value + ':' + cutoff1 + ":" + cutoff2;

//                    FLAWED SEARCH
//                    cmd += ( "(rated:" + diffDays + ':' + encodeSelectedRating(selectedRating) + ')' );
//                    if (diffDays > 1) {
//                        cmd += ( "(rated:" + diffDays + ':' + encodeSelectedRating(selectedRating) + ') - ' + "(rated:" + diffDayMinusOne + ':' + encodeSelectedRating(selectedRating) + ')' );
//                    } else {
//                        cmd += ( "(rated:" + diffDays + ':' + encodeSelectedRating(selectedRating) + ')' );
//                    }

                    // Invoke browse
                    pybridge("hm_browse:" + cmd);

                    // Update date highlight to include clicked on date AND today
                   more_cal.highlight([new Date(), date]);
                },
             });

           return more_cal;
}

// FAILED ATTEMPTS :(


//function onMoreHmNavigate(event, button, direction) {
//    if (direction === "next") {
//        more_cal.next();
//    }
//    else {
//        more_cal.previous();
//     }
//}

//    cal.init({
//        domain: "month",
//        subDomain: "day",
//        cellSize: 50,
//        itemName: ["card", "cards"],
//        displayLegend: false,
//        itemSelector: "#cal-heatmapzzzz",
//        tooltip: true,
//        data: data,
//        });

// var cal = new CalHeatMap();
//           cal.init({
//               domain: "month",
//               subDomain: "day",
//               cellSize: 50,
//               itemName: ["service ticket", "service tickets"],
//               data: {
//                   "1452019700": 40,
//                   "1454688100": 50,
//                   "1452710900": 5,
//                   "1452883700": 15,
//                   "1453142900": 15,
//                   "1453488500": 30,
//                   "1456239700": 80,
//                   "1453662300": 20,
//                   "1455130100": 60,
//                   "1455562100": 70,
//                   "1455131100": 10,
//                   "1456166900": 30,
//                   "1456399000": 12,
//                   "1451674100": 90
//               },
//               subDomainTextFormat: "%d",
//               range: 1,
//               itemSelector: "#cal-heatmapzzzz",
//               start: new Date(2016, 01, 01),
//               displayLegend: false
//           });