// json_stuff index order: id, date, caption, location text, lat, lng, pic url, thumburl, uploader_name, uploader_profile_url

json_length = json_stuff.length;
// setting up the Leaflet map
var mymap = L.map('mapid').setView([21.027763, 105.834160], 8);
bounds = L.latLngBounds(L.latLng(26.693407, 97.321159), L.latLng(4.648797, 121.418566));
mymap.setMaxBounds(bounds);
// setting the renderer, used for the gps route line later
var myRenderer = L.canvas({padding: 0.2, tolerance: 20});

// creating the Instagram markers on the map
for (i = 0; i < json_length; i++) {
    if (json_stuff[i][2] == null) {
        json_stuff[i][2] = 'no caption'
    }
    // handling image vs video posts
    try {
        if (json_stuff[i][6].includes('.jpg')) {
            popCont = '<img class="popupImage" src="' + json_stuff[i][6] + '" alt="' + json_stuff[i][2] + '"><br><p>' + json_stuff[i][1].slice(0, 10) + '<br>' + json_stuff[i][3] + '<br>' + json_stuff[i][2] + '<br>Posted by <a href="' + json_stuff[i][9] + '">' + json_stuff[i][8] + '</a></p>';
        }
        else {
            popCont = '<video controls><source src="' + json_stuff[i][6] +'" type="video/mp4"><source src="' + json_stuff[i][6] +'" type="video/ogg">Your browser does not support the video tag.</video><br><p>' + json_stuff[i][1].slice(0, 10) + '<br>' + json_stuff[i][3] + '<br>' + json_stuff[i][2] + '<br>Posted by <a href="' + json_stuff[i][9] + '">' + json_stuff[i][8] + '</a></p>';
        }}
    catch(e) {
            console.log(e)
        }

    // generating marker icons
    L.marker([json_stuff[i][4], json_stuff[i][5]], {
        icon: L.icon({
            iconUrl: json_stuff[i][7],
            iconSize: [50,],
            popupAnchor: [0, 0]
        }),
        riseOnHover: true
    }).bindPopup(popCont).openPopup().addTo(mymap);
}

// Leaflet map texture
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: '',
    maxZoom: 20,
    minZoom: 6,
    id: 'mapbox.streets',
    accessToken: ''
}).addTo(mymap);

// Cycling route section
var mapgps;
$(".dropdown-item").click(function () {
    let s = this.name.substring(9).replace("/", "").replace("/", "");
    let day = this.innerHTML.slice(5);
    if ($(this).css('background-color') !== 'rgb(211, 211, 211)') {
        $(this).css('background-color', 'lightgray');
        $.ajax({
            url: this.name,
            success: function (result) {
                mapgps = result;
                if (mapgps.startsWith('<?xml version="1.0" encoding="UTF-8"?>')) {
                    new L.GPX(mapgps, {
                        async: true,
                        marker_options: {
                            startIconUrl: "/static/leaflet/images/start.svg",
                            endIconUrl: "/static/leaflet/images/finish-line2.svg",
                            shadowUrl: "/static/leaflet/images/pin-shadow.png",
                            className: 'map-pin',
                        },
                        polyline_options: {
                            color: 'green',
                            weight: 4,
                            renderer: myRenderer
                        }
                    })
                        // attaches popup to route so can be opened and closed by clicking on
                        .on('loaded', function (e) {
                        // console.log(e.target._info); //prints everything we can call from the gpx file
                        routePopCont = "<p class='route-title'>" + window["route" + e.target.get_start_time().getFullYear() + day]
                        + "</p><p class='route-details'>" + e.target.get_start_time().toLocaleString("en-US", {timeZone: "Asia/Ho_Chi_Minh"})
                        + " - " + e.target.get_end_time().toLocaleString("en-US", {timeZone: "Asia/Ho_Chi_Minh"}).slice(12)
                        + "<br>Moving time: " + e.target.get_duration_string(e.target.get_moving_time())
                        + "<br>Average speed: " + e.target.get_total_speed().toFixed(2)
                        + " km/h<br>Distance: " + (e.target.get_distance()/1000).toFixed(2)
                        + " km<br>Elevation gain: " + Math.round(e.target.get_elevation_gain()) + "m</p><details>"
                        + "<summary>Day " + day + " Journal</summary>" + window["route" + e.target.get_start_time().getFullYear() + day + "-text"] + "</details>";
                        e.target.bindPopup(routePopCont);
                        mymap.fitBounds(e.target.getBounds());
                        window["menuId" + s ] = e.target.getBounds();
                    })
                        // This attached a popup to the endpoint when the route line is drawn
                        .on('addpoint', function(e) {
                        if (e.point_type === 'end') {
                            routePopCont = "<p class='route-title'>" + window["route" + e.target.get_start_time().getFullYear() + day]
                        + "</p><p class='route-details'>" + e.target.get_start_time().toLocaleString("en-US", {timeZone: "Asia/Ho_Chi_Minh"})
                        + " - " + e.target.get_end_time().toLocaleString("en-US", {timeZone: "Asia/Ho_Chi_Minh"}).slice(12)
                        + "<br>Moving time: " + e.target.get_duration_string(e.target.get_moving_time())
                        + "<br>Average speed: " + e.target.get_total_speed().toFixed(2)
                        + " km/h<br>Distance: " + (e.target.get_distance()/1000).toFixed(2)
                        + " km<br>Elevation gain: " + Math.round(e.target.get_elevation_gain()) + "m</p><details>"
                        + "<summary>Day " + day + " Journal</summary>" + window["route" + e.target.get_start_time().getFullYear() + day + "-text"] + "</details>";
                            mymap.openPopup(routePopCont, e.point['_latlng'], {
                                direction: 'bottom',
                            });
                        }})
                        .addTo(mymap);
                } else {
                    // if the day is a rest day and doesn't have a gpx file, we create a marker label it a rest day
                    mapgps = JSON.parse(mapgps);
                    L.marker([mapgps[0], mapgps[1]], {
                        icon: L.icon({
                            iconUrl: '/static/coffee.gif',
                            iconSize: [80,],
                            className: 'map-pin rest-day',
                            popupAnchor: [0, 0],
                        })
                    })
                        .bindPopup("<p class='route-title'>" + mapgps[2] + "</p><details><summary>Day " + mapgps[4] + " Journal</summary>" + mapgps[3] + "</details>", {

                        }).openPopup()
                        .addTo(mymap).openPopup();

                    window["menuId" + s ] = [mapgps[0], mapgps[1]]; // keeps info in memory so clicking on the day again still re-centers map on marker without reloading gpx file
                    mymap.panTo([mapgps[0], mapgps[1]], {
                        animate: true
                    });//pan to the rest day location
                }
            },
            error: function () {
                alert('Server error'); // Displayed on frontend when loading a route if server doesn't respond
            }
        });
    }
    // This recenters the user on a previously loaded route if they click on the same route twice in the menu
    else {
        try {
            mymap.fitBounds(window["menuId" + s]);

        }
        catch(err) {
            mymap.panTo(window["menuId" + s]);
        }
    }
});