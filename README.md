# vxx_tracker
This is a Django-powered webapp that scrapes Instagram for posts and displayed them on a Leaflet map. It also allows for admins to add routes via .gpx files , which can be downloaded from Strava.

To update Day Routes:
- download the gpx file from Strava
- add lat and lng for rest days (find these on Google maps)
- add journals from Facebook embeded option. if it gives the option to "include all post" check the box. Most of of the time this is not an option.
- if adding more than one iframe, do not put line breaks between them, or it will cause a script error. Follow the ending </iframe> tag directly with the next <iframe> tag.