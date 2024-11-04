This project was made by Wei-chen Huang for use in NSC 4353: Neuroscience Lab Methods at the University of Texas at Dallas as a tool for measuring locomotion of Daphnia as part of data recording in the student-led Daphnia Project.

note: works for most videos right now, can fail to generalize for a few, working a better-generalizing filter


!!INSTRUCTIONS!!

If you are using Google Colab (slow to upload video to Colab environment, computations are fast):
The link to the notebook is: https://colab.research.google.com/drive/1CxfRKlwDicCXAjHEFMJubC0Nk_wSpG-Y?usp=sharing
Make a copy in your own Google Drive
Then just click the run (play) button in each cell, and it will prompt you to upload a video (will take some time) and draw bounding boxes over the daphnia.

If you are running the code on your computer (faster because no need to upload anything, the computations are fast):
1.
if you do not have python installed, install python, any version of python 3 should work fine
download from here: https://www.python.org/downloads/
add python to path follow instructions here: https://realpython.com/add-python-to-path/

2.
open command prompt - can search and open (not preferred)
open file explorer where the program is located, clear the address bar, type cmd and press enter (preferred)
ensure python is installed and added to path: type python --version and hit enter, it shold display the version of python you have, this ensures that python is correctly installed 

3. 
install required packages
in the command prompt: type pip install opencv numpy and hit enter
both packages will install automatically

4. 
time to run the code!
type python dahpnia_cv.py and it will run
the program will open a file explorer menu and prompt you to select a file to open.
After a file is selected, 
This should print the total distance travelled by the daphnia in the video in pixels

TROUBLESHOOTING:
if it says no module found for cv2 or numpy, try:
python -m pip install opencv
and 
python -m pip install numpy

How it works:
We look at the video frame by frame, and we apply a filter that turn everything brighter than a certain threshold to pure white (255), and everything darker than a certain threshold to dark (0).
Next, we get the centroid of the largest dark contour, which we assume will be the daphnia in the image.
Between each frame, we calculate the euclidian distance that the centroid of the largest dark contour (daphnia) travelled, and add up the distances between each frame.
