DatapointCreationTool

To create the XML document, please refer to 
https://github.com/tzutalin/labelImg

Dependencies (Tested under python2.7)
- pykeyboard
- pyscreenshot
- pandas?

Description
This tool aides in the capture and data collection of the Alfred Stream Bot project where an AI is to be trained in order to recognize in game stocks captured on any platform. The captured images are synthesized into individual images with varying resolutions and sizes all the while keeping the stock position intact.

How to run
Currently the development build of the data collection uses a dolphin emulator and maximizes the whole screen. 

1. Launch dolphin, start Melee, enter into any stage and pause.
2. Fullscreen the dolphin game window. (I just maximized it without fullscreening through options)
3. Take a screenshot and save the image.
4. Open labelImage.py and label the bounding areas sequentially with the name (boundingBox)
5. Label the stock icon areas sequentially cooresponding to the parent region boundingBox area. Name this sub region (falconBox)
6. Save the XML and launch the python collect_data.py by adding the arguments -x/--xml XML_FILE, -d/--directory DIRECTORY. 
* As soon as the script launches, the directory specified will either be WIPED OR CREATED, be cautious on what directory you select! *
* Also the script will automatically start recording data, so make sure you have your game playing as soon as you launch the script, remember its taking SCREEN SHOTS so anything on your screen will be captured. This doesn't mean though it will ruin where your stocks are, as long as its not overlapping. *

Few notes
The labelImage allows for many boxes to be added. The collect_data.py script will take this into account, meaning you should have n bounding boxes to n falcon boxes, thus you can have as many boxes you need. Therefore, for melee, you can have 20 stocks being recorded per data frame.

Validate.py is a recent addition whose arguments may be reduced to just -f.
This handy script checks the post text file created by the image capture and checks the file sequentially for out of bounds errors.

Later I'll be adding random time sleeps to vary out the data collection and pykeyboard will be used as a pause in between switching maps.
