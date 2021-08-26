// json_stuff index order: id, date, caption, location text, lat, lng, pic url, thumburl, uploader_name, uploader_profile_url

const json_length = json_stuff.length;
// setting up the Leaflet map
var mymap = L.map('mapid').setView([ 21.027763, 105.83416 ], 8);
bounds = L.latLngBounds(L.latLng(26.232144, 95.650739), L.latLng(4.034532, 119.481904));
mymap.setMaxBounds(bounds);
// setting the renderer, used for the gps route line later
var myRenderer = L.canvas({ padding: 0.2, tolerance: 20 });

// VXX journey dates
const vxx2016Start = new Date('10/11/2016');
const vxx2016End = new Date('11/28/2016');
const vxx2020Start = new Date('5/10/2020');
const vxx2020End = new Date('5/31/2020');

// creating the Instagram markers on the map
for (i = 0; i < json_length; i++) {
	if (json_stuff[i][2] == null) {
		json_stuff[i][2] = 'no caption';
	}
	// handling image vs video posts
	try {
		if (json_stuff[i][6].includes('.jpg')) {
			popCont =
				'<img class="popupImage" src="' +
				json_stuff[i][6] +
				'" alt="' +
				json_stuff[i][2] +
				'"><br/><p>' +
				new Date(json_stuff[i][1].slice(0, 10)).toDateString() +
				'<br/>' +
				json_stuff[i][3] +
				'<br/>' +
				json_stuff[i][2] +
				'<br/>Posted by <a href="' +
				json_stuff[i][9] +
				'">' +
				json_stuff[i][8] +
				'</a></p>';
		} else {
			popCont =
				'<video controls><source src="' +
				json_stuff[i][6] +
				'" type="video/mp4"><source src="' +
				json_stuff[i][6] +
				'" type="video/ogg">Your browser does not support the video tag.</video><br/><p>' +
				json_stuff[i][1].slice(0, 10) +
				'<br/>' +
				json_stuff[i][3] +
				'<br/>' +
				json_stuff[i][2] +
				'<br/>Posted by <a href="' +
				json_stuff[i][9] +
				'">' +
				json_stuff[i][8] +
				'</a></p>';
		}
	} catch (e) {
		console.log(e);
	}
	// Determine if post is from a specific VXX journey
	const postDate = new Date(json_stuff[i][1]);
	let dateClass = 'not-journey';
	if (postDate >= vxx2016Start && postDate <= vxx2016End) dateClass = 'journey-2016';
	if (postDate >= vxx2020Start && postDate <= vxx2020End) dateClass = 'journey-2020';

	// generating marker icons
	L.marker([ json_stuff[i][4], json_stuff[i][5] ], {
		icon: L.icon({
			iconUrl: json_stuff[i][7],
			iconSize: [ 50 ],
			popupAnchor: [ 0, 0 ],
			className: dateClass
		}),
		riseOnHover: true
	})
		.bindPopup(popCont)
		.openPopup()
		.addTo(mymap);
}

// Leaflet map texture
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
	attribution: '',
	maxZoom: 20,
	minZoom: 6,
	id: 'andrewtmarvin/cksqsezs4189q17qgpgzgbvjx',
	accessToken: 'pk.eyJ1IjoiYW5kcmV3dG1hcnZpbiIsImEiOiJja3NrcmhqZ3kwOXljMnduMHVzc3JkeW5jIn0.Rgc7MKhBWYuRRXuavqrDZA'
}).addTo(mymap);

// Cycling route section
var mapgps;
document.querySelectorAll('.route-menu-item').forEach((element) => {
	element.addEventListener('click', (e) => {
		e.preventDefault();
		const link = e.target;
		let s = link.name.substring(9).replace('/', '').replace('/', '');
		let day = link.dataset.day;
		if (link.style.backgroundColor !== 'rgb(211, 211, 211)') {
			link.style.backgroundColor = 'rgb(211, 211, 211)';
			fetch(link.name)
				.then((response) => response.text())
				.then((text) => {
					mapgps = text;
					if (mapgps.startsWith('<?xml version="1.0" encoding="UTF-8"?>')) {
						let polyLineColor = 'black';
						s.slice(0, 4) == '2016' ? (polyLineColor = 'goldenrod') : (polyLineColor = '#56b947');
						new L.GPX(mapgps, {
							async: true,
							marker_options: {
								startIconUrl: '/static/leaflet/images/start.svg',
								endIconUrl: '/static/leaflet/images/finish-line2.svg',
								shadowUrl: '/static/leaflet/images/pin-shadow.png',
								className: 'map-pin'
							},
							polyline_options: {
								color: polyLineColor,
								weight: 4,
								renderer: myRenderer
							},
							routePopCont: ''
						})
							// attaches popup to route so can be opened and closed by clicking on
							.on('loaded', function (e) {
								e.target.bindPopup(this.options.routePopCont);
								mymap.fitBounds(e.target.getBounds());
								window['menuId' + s] = e.target.getBounds();
							})
							// This attached a popup to the endpoint when the route line is drawn
							.on('addpoint', function (e) {
								if (e.point_type === 'end') {
									// console.log(e.target._info); //prints everything we can call from the gpx file
									this.options.routePopCont =
										"<p class='route-title'>" +
										window['route' + e.target.get_start_time().getFullYear() + day] +
										"</p><p class='route-details'>" +
										new Date(
											e.target
												.get_start_time()
												.toLocaleString('en-US', { timeZone: 'Asia/Ho_Chi_Minh' })
												.split(',')[0]
										).toDateString() +
										'<br/>' +
										e.target
											.get_start_time()
											.toLocaleString('en-US', { timeZone: 'Asia/Ho_Chi_Minh' })
											.split(',')[1] +
										' &rarr; ' +
										e.target
											.get_end_time()
											.toLocaleString('en-US', { timeZone: 'Asia/Ho_Chi_Minh' })
											.split(',')[1] +
										'<br/>Moving time: ' +
										e.target.get_duration_string(e.target.get_moving_time()) +
										'<br/>Average speed: ' +
										e.target.get_total_speed().toFixed(2) +
										' km/h<br/>Distance: ' +
										(e.target.get_distance() / 1000).toFixed(2) +
										' km<br/>Elevation gain: ' +
										Math.round(e.target.get_elevation_gain()) +
										'm</p><details>' +
										'<summary>Day ' +
										day +
										' Journal</summary>' +
										window['route' + e.target.get_start_time().getFullYear() + day + '-text'] +
										'</details>';
									mymap.openPopup(this.options.routePopCont, e.point['_latlng'], {
										direction: 'bottom'
									});
								}
							})
							.addTo(mymap);
					} else {
						// if the day is a rest day and doesn't have a gpx file, we create a marker label it a rest day
						mapgps = JSON.parse(mapgps);
						L.marker([ mapgps[0], mapgps[1] ], {
							icon: L.icon({
								iconUrl: '/static/coffee.gif',
								iconSize: [ 80 ],
								className: 'map-pin rest-day',
								popupAnchor: [ 0, 0 ]
							})
						})
							.bindPopup(
								"<p class='route-title'>" +
									mapgps[2] +
									'</p><details><summary>Day ' +
									mapgps[4] +
									' Journal</summary>' +
									mapgps[3] +
									'</details>',
								{}
							)
							.openPopup()
							.addTo(mymap)
							.openPopup();

						window['menuId' + s] = [ mapgps[0], mapgps[1] ]; // keeps info in memory so clicking on the day again still re-centers map on marker without reloading gpx file
						mymap.panTo([ mapgps[0], mapgps[1] ], {
							animate: true
						}); //pan to the rest day location
					}
				})
				.catch((err) => {
					alert('Server error');
				}); // Displayed on frontend when loading a route if server doesn't respond});
		} else {
			// This recenters the user on a previously loaded route if they click on the same route twice in the menu
			try {
				mymap.fitBounds(window['menuId' + s]);
			} catch (err) {
				//
			}
		}
	});
});

// Route Menu Section
const routeYearLinks = document.querySelectorAll('.route-year-link');
const routeYearMenus = document.querySelectorAll('.route-year-menu');
routeYearLinks.forEach((yearLink) => {
	yearLink.addEventListener('click', (e) => {
		e.preventDefault();
		routeYearLinks.forEach((link) => link.classList.remove('route-year-link-active'));
		e.target.classList.add('route-year-link-active');
		routeYearMenus.forEach((menu) => menu.classList.remove('route-year-menu-visible'));
		e.target.nextElementSibling.classList.add('route-year-menu-visible');
	});
});

// Show Posts By VXX Journey Section
const notJourney = document.querySelectorAll('.not-journey');
const Journey2016 = document.querySelectorAll('.journey-2016');
const Journey2020 = document.querySelectorAll('.journey-2020');
const checkbox2016 = document.querySelector('#checkbox-2016');
const checkbox2020 = document.querySelector('#checkbox-2020');
const checkboxOthers = document.querySelector('#checkbox-others');
const displayPostsByYear = () => {
	const hide = (posts) => {
		for (post of posts) {
			post.classList.add('hidden-post');
		}
	};
	const show = (posts) => {
		for (post of posts) {
			post.classList.remove('hidden-post');
		}
	};
	if (!checkbox2016.checked && !checkbox2020.checked && !checkboxOthers.checked) {
		show(notJourney);
		show(Journey2016);
		show(Journey2020);
	} else {
		checkbox2016.checked ? show(Journey2016) : hide(Journey2016);
		checkbox2020.checked ? show(Journey2020) : hide(Journey2020);
		checkboxOthers.checked ? show(notJourney) : hide(notJourney);
	}
};
document
	.querySelectorAll('.checkbox-group input')
	.forEach((input) => input.addEventListener('click', displayPostsByYear));
