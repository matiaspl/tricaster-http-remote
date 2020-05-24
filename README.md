The app is designed to extend the 4 M/E buses available on TC-1 using presets for additional scenes and comps for zooms that usually would be available on a liveset. It comes handy if you use want to use more than 4 different shots.

Basic usage:
Set M/E 1 on pgm and M/E 2 on pvw. Currently there's no sanity check to make sure that only two 'utility' M/Es are used for switching between presets.
```
Load preset 2 on a M/E that is currently on main row A (a.k.a. "program"):
http://localhost:8080/?bus=program&preset=2

Load comp 2 on a M/E that is currently on main row B (a.k.a. "preview"):
http://localhost:8080/?bus=preview&comp=2

Load preset 3 with comp 1 applied on a M/E that is currently on main row B (a.k.a. "preview"):
http://localhost:8080/?bus=preview&preset=3&comp=2
```
This allows using e.g. Bitfocus Companion along with a Streamdeck to create an alternate controller for joint control of both main bus source M/E's and their contents. for a specially crafted livesets consisting of a grid/mosaic of scenes.

Have in mind that on Tricasters bus presets also include bus comps, 
