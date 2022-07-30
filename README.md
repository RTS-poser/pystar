# pystar 
This is a python GUI app, and some supporting material, to assist with in-game geolocation and navigation.
 
Rather than using similar tools that rely on using an OM-# as a fiixed starting point, you can enter in 4+ distances to known quantum markers to get an approximate location.  Then you can manually enter in xyz coordiantes and plot a bearing and get an approximate distance.
 
The real intent of this tool is that if you get lost, or over shoot, or drift off course: you can stop, figure out where you are, and plot a new course.

## Credit where credit is due
The app relies heavily on a community generated [google doc spreadsheet](https://docs.google.com/spreadsheets/d/1VydKNxBHdljhO8ANSEcZRWogInCh-6tAdjI1HcwFlVE/edit#gid=1238406064) provided by player [justMurphy](https://robertsspaceindustries.com/citizens/justMurphy) and is inspired by various pre-existing tools already avaiable in the community.  This project is 50% personal learning, 50% customization for personal use in game, but if it helps others feel free to try it.

## Discalimers
This tool is a hobby of a hobby.  Real World > learning how to do new things > playing Star Citizen > building usable tools for Star Citizen.  If poor quality code, sub optimal user experience, or gramatical mistakes in documentation trigger you, please feel free to take these ideas and run with them! Just maybe share your results if you get somewhere with it?

## Setup/"Install"
This is a python script that has not been optimized for wide release.  A certain amount of python/anaconda knowledge is assumed, but I'll try and point you in the right direction:
- This has been tested on [Python 3.10](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), as distributed by [Anaconda/Miniconda](https://docs.anaconda.com/anaconda/install/)
- major dependent libraries include:
  - [pyqt (PyQt5)](https://anaconda.org/anaconda/pyqt)
  - [scipy](https://anaconda.org/anaconda/scipy) (should include [numpy](https://anaconda.org/anaconda/numpy))
  - Will technically run from spyder IDE, works best from console
- Download repository and extract to a local known folder.
- Note that this app relies on a community generated google doc spreadsheet, exported to a CSV file (included in repo) and will need to be updated with major patches periodically.

## To run:
- Set up an environment of python with known dependencies (scipy, numpy) and activate it
- download repository to local computer
- navigate to repository on local computer via commandline
- run: python trip_logger.py
- begin using as described below

## Workflow

In terms of practical usage, this is perhaps best for users with a spare laptop floating around.  Switching back and forth on a single gaming PC is likely not going to be a plesent experience.  This *should* work wherever python + pyqt can be installed but has only been tested on Windows 10 and macOS.
 
If you have a known planet-relative XYZ location (planet = xyz origin = 0,0,0)
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
   - If you make a data entry error you *should* be able to click "Clear Anchors" to remove the last entry, but only BEFORE hitting "Save Anchors" though this has not been well tested
- Once at least 4 Anchor points are added, click the "Save Anchors" button. This will update the "Survey Point" Origin/Destination on the "Calculate Bearing" tab, save your results, and clear out the text entry boxes.  Don't worry that the table is not updated, its fine, it will clear out later.

If you want to navigate somewhere and have already entered it as a Survey Point:
- Click the "Calculate Bearing" tab, note this will only work on a single planet/moon, so if you collect Survey Points from multiple reference frames, you need to keep track of that yourself.
- For both your "Origin" and your "Destination" you will need to:
  - Select if your origin/destination is a known "Quantum Marker" or a custom "Survey Point" from the appropriate drop down box
  - Once the first dropdown box is selected for either Origin/Destination, the second should be populated with available Quantum Markers
- Click the "Calculate Heading" to get the in game compass "Course/Bearing" and the estimated "Distance" to target
  - Note, distance estimate is not based on Great Circles but then there is no in-game odometer
  - If traveling from a land based quantum marker you shuold be able to turn around during your journey to monitor progress
  - Note that if traveling from an orbital location, the in game compass can act a little weird, try going to a lower altitude?
  - accuracy of the calcualtions depends on the accuracy of the inputs.  In game distances round to the nearest meter, 1/10 km, or km making the absolute accuracy of your Survey Point subject to a lack of precision  

## Bonus/Data Export
Every time the "Save Anchor" button on the "Survey Points" tab is used, a json file called "star_gui.json" is saved to the local code directory (example included in repo).  This can be further processed and converted into a CSV file or otherwise used as you see fit.  For example you can track the waypoints you use during a trip or record fixed points with identification for use in other projects.

## Known issues & Failure Modes
- preliminary accuracy estimates are guessed/assumed to be several hundred meters in game.  Probably accurate enough to find a ship or modest landmark, probably not accurate enough to see a delivery box easily/without searching
- Forms can be prone to user/data entry error, quantum marker distance text can be hard to read at times
- Distance calculations are estimates and distance traveled is not always easy to measure whil looking forward.  When on final approach, slow down, lose altitude, and consider doing addiiotanl Survey Point checks to confirm if you over-shoot your target.  During casual usage the biggest user error seems to be overshooting a target repeatedly (based on a sample size of 1 user so far...).
- App can crash if an unexpected usage pattern is encountered.  Error trapping and graceful failure modes have not been implemented.
- UI/UX could probably use some improvememnts too.

## Ideas for Future
- add user configuration and session-specific save options
- add tools to export to more common formats including CSV and geographic/shapefiles
- perhaps look into adding simple graphics/mini map?
- enhance UX based on common workflows (auto-indremeent IDs for survey points, loading data from past sessions?)

 
 
