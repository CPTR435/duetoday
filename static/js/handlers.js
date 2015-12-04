// handlers.js

var main = $("#main-content");

var handlers = [
	["/calendar.*", calendarHandler],
	["/EditItem/.*", editHandler],
	["/NewItem", editHandler],
	["/EditFeed/.*", feedHandler],
	["/NewFeed", feedHandler],
	["/.*", pageHandler],
	[".*", indexHandler]
];

function hasher() {
	var title = window.location.hash.substr(1).replace(/\//g," | ").replace(/_/g," ").replace(/\./g," ").capitalize();
	document.title = config.title + title;

	var hash = window.location.hash.substr(1);
	for (var h in handlers) {
		var path = handlers[h][0].replace(/\//g,"\\\/");
		var r = new RegExp(path);
		var m = hash.match(path);
		if (m && m[0] === hash) {
			m = path.split("\\\/");
			hash = hash.split("/").filter(function(i) { return m.indexOf(i) < 0; });
			handlers[h][1].apply(this, hash);
			return true;
		}
	}
}

function indexHandler() {
  loader(main, "static/html/main.html", function() {
		// put after loading scripts here
	});
  if (window.location.hash.length > 1) {
    window.location.hash = "";
  }
}

function pageHandler(path1, path2) {
  var path = path1+(path2 ? "/"+path2 : "")+".html";
  loader(main, "static/html/"+path, function(xhr) {
    if (xhr.status > 400)
      window.location.href = "#";
  });
}

var getCalendarPath;

function calendarHandler(path1, path2) {
  loader(main, "static/html/calendar.html", function(xhr) {
    if (xhr.status > 400)
      window.location.href = "#";
  });

    // Format:
    //   #/calendar/2015-12-25 -- Particular day
    //   #/calendar/2015-12    -- December
    //   #/calendar/2015-W45   -- week 48
    function getCalendarPathLocal() {
        // Get the path from a global variable created in handler.js
        var view = 'month';
        var gotoDate = moment();

        if (path2 != undefined) {
            var path = path2.split('-');

            if (path.length == 2) {
                if (path[1].substring(0,1) == 'W') {
                    gotoDate = moment().week(path[1].substring(1))
                    view = 'week';
                } else {
                    gotoDate = moment(path[1]+'/01/'+path[0])
                    view = 'month';
                }
            } else if (path.length == 3) {
                gotoDate = moment(path[1]+'/'+path[2]+'/'+path[0])
                view = 'day';
            }
        }

        return [view, gotoDate.format('MM/DD/YYYY')];
    }

    // Allow us access to this function outside of calendarHandler()
    getCalendarPath=getCalendarPathLocal;
}

var getIdent;
function editHandler(id){
	loader(main, "static/html/NewItem.html", function() {
	});
	function getID(){
		var ident = id;
		return ident;
	}
	getIdent = getID;
}

var feedId;
function feedHandler(id) {
	loader(main, "static/html/NewFeed.html", function() {});
	function getID() {
		return id;
	}
	feedId = getID;
}
