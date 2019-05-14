// json index order: id, date, caption, location text, lat, lng, pic url, thumburl

 json_length = json_stuff.length;



var mymap = L.map('mapid').setView([21.027763, 105.834160], 8);
bounds = L.latLngBounds(L.latLng(26.693407, 97.321159), L.latLng(4.648797, 121.418566));
mymap.setMaxBounds(bounds);
for (i = 0; i < json_length; i++) {

    popCont = '<img class="popupImage" src="' + json_stuff[i][6] + '"><br><p>' + json_stuff[i][1].slice(0,10) + '<br>' + json_stuff[i][3] + '<br>' + json_stuff[i][2] + '</p>';
    L.marker([json_stuff[i][4], json_stuff[i][5]], {
        icon:L.icon({
            iconUrl: json_stuff[i][7],
            iconSize: [50, ],
            popupAnchor: [0,0]})}).bindPopup(popCont).openPopup().addTo(mymap);

}
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: '',
    maxZoom: 20,
    minZoom: 6,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoidm9uZ3hleGFuaCIsImEiOiJjanY3YWF0eGQwZHV5M3lxcG5pYmw5YXNtIn0.v0B_dYRqfmTjJa-q4L3a1A'
}).addTo(mymap);

var mapgps;
    $("button").click(function(){
  $(this).css('border', '1px solid red');
  $.ajax({url: this.value,
      success: function(result){
    mapgps = result;
    if (mapgps.startsWith('<?xml version="1.0" encoding="UTF-8"?>')){

    new L.GPX(mapgps, {
        async: true,
        marker_options: {
            startIconUrl: "/static/leaflet/images/pin-icon-start.png",
            endIconUrl: "/static/leaflet/images/pin-icon-end.png",
            shadowUrl: "/static/leaflet/images/pin-shadow.png",
            className: 'map-pin',
        }
    }).on('loaded', function(e){
        mymap.fitBounds(e.target.getBounds());
    }).addTo(mymap);
    } else {
        mapgps = JSON.parse(mapgps);
        L.marker([mapgps[0], mapgps[1]], {
        icon:L.icon({
            iconUrl: '/static/rest.png',
            iconSize: [50, ],
            className: 'map-pin',
            popupAnchor: [0,0]})}).bindPopup(mapgps[2]).openPopup().addTo(mymap);
            mymap.panTo([mapgps[0], mapgps[1]],{animate: true});//pan to the rest day location
    }},
      error: function(){
      alert('Rest Day'); // instead of an alert, set it up so that a map popup displays
  }
  });
});



    // for (i = 0; i < json_length; i++) {
    //     window["postId"+json_stuff[i][0]] = json_stuff[i];
    //     }

    // displaying thumbnails
    // for (i = 0; i < json_length; i++) {
    //     var img = document.createElement('img');
    //     img.src = json_stuff[i][7];
    //     img.alt = 'test';
    //     img.width = 75;
    //     img.height = 75;
    //     document.body.appendChild(img);
    // }