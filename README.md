# pystar 
 This is a python GUI app, and some supporting material, to assist with in-game geolocation and navigation.
 
 Rather than using similar tools that rely on using an OM-# as a fiixed starting point, you can enter in 4+ distances to know quantum markers to get an approximate location.  Then you can manually enter in xyz coordiantes and plot a bearing and get an approximate distance.
 
 The real intent of this tool is that if you get lost, or over shoot, or drift off course, you can stop, figure out where you are, and plot a new course.
 
 ##Workflow
 
 If you have a known planet-relative (planet = xyz origin = 0,0,0)
 - Click the "Manual Entry" tab
 - Enter a memorable "Target Name" for your location, it will be used in app and saved to export files for this point
 - Enter in the X, Y, Z text boxes the coresponding relative coordiantes in METERS
 - Click "Add Location" Button to view Decimal Degrees relative to OM-3 projected onto a sphere
 - "Target Name" will be available from "Survey Point" Origin/Destination on the "Calculate Bearing" tab
   - You will need to remember what planet a survey point is on as this is not stored for you.  Consider adding it to the Target name if moving around a lot.
 
 If you want to figure out where you are (if you found something to save or are taking a survey point):
 - Click the "Survey Points" tab
 - Enter a memorable "Target Name" same as above
 - You will need to collect Four "anchor points" to determine your location using [multilateration](https://en.wikipedia.org/wiki/Multilateration#/media/File:MLAT_TOT_2D_Algorithm.svg) so it helps to pick quantum markers nearby from different directions.  The accuracy of your point depends on the quality of your anchor selection.
   - From the "Planetary Body" drop down, select the location you are surveying
   - In a ship, enable quantum drive and orient towards a planet-bound quantum marker (OM-# will also work, major orbital stations should also work if in geostationary orbits)
   - Start typing the name of your selected "Quantum Marker" in the designated text box, allow autocomplete to assist you.  Spelling matters, it needs to be perfect based on the reference points used in the script.  Trust autocomplete!
   - Enter in the "Marker Distance" in the designated text box, be sue to select km/m (sticking with km and converting in your head is probably better)
   - Click "Add Anchor" button to save the anchor point and reset the entry fields, repeat up until at least 4 anchors are added, more can be supported though the impact on quality has not been tested (ideally more = better, in theory)
   - If you make a data entry error you *should* be able to click "Clear Anchors" to remove the last entry, but only BEFORE hitting "Save Anchors"
- Once at least 4 Anchor points are added click the "Save Anchors" button, this will update the "Survey Point" Origin/Destination on the "Calculate Bearing" tab, save your results, and clear out the text entry boxes.  Don't worry that the table is not updated, its fine, it will clear out later.
- 
 
 
 ## Discalimers
 This tool is a hobby of a hobby.  Real World > playing Star Citizen > building tools for Star Citizen.
