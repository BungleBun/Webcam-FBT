# Webcam-FBT (Name in progress)

This project is a work in progress, not a full working project.

Welcome to my project, Webcam-FBT (name in progress). I am creating this project to make fullbody tracking in VR more accessible.

# What does this project do/plan to do?

Webcam-FBT takes the user's webcam feed using opencv and uses mediapipe to map the user's body out with a skeletal rig. Using an advanced google machine learning model it uses pose estimation to smoothly translate the 2 dimensional camera movements into 3d fully tracked body movements. It then uses the tracked position of the mapped skeletal rig and maps it to your in-game virtual reality character.

Using the VRChat OSC it will translate your fullbody movements smoothly onto any avatar. There is also a plan to use OpenVR drivers to make this project compatible with any SteamVR game with FBT features as well.

Thus far I am only working on making it run on PCVR but I hope to eventually find ways to make it run smoothly on any setup, whether that be PCVR and webcam, standalone and mobile camera, PCVR and mobile camera, or standalone and webcam. 

# Fancy tech lingo:

Languages:
    -Python

Libraries:
    -OpenCV
    -Mediapipe
    -Numpy
    -Time
    -Python-OSC
    -TBD

Frameworks:
    -TBD

# How to run:

TBD (All the project does in this stage is turn on your webcam and display it in a small window, it doesn't even turn it off when you try to exit out of the window (from my experience). I fail to see why you would WANT to run it thus far.)

# Update log:

* 7/2/2026: Added Google's ML model and Mediapipe to track the coordinates of 33 different points on the user's body. Currently prints the coordinates, with plans to instead feed them into a game's OSC/Driver. Also added better documentation inside of the code.

* 7/1/2026: This is my first real git contribution so I am just trying to get it out there with hopes of updating in the future.

