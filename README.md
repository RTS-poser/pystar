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
 
 
 ## Discalimers
 This tool is a hobby of a hobby.  Real World > playing Star Citizen > building tools for Star Citizen.
