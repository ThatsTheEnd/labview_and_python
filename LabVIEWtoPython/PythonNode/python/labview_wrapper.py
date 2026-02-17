import analysis
import cv2
from collections import namedtuple

# Define Keypoint namedtuple for LabVIEW compatibility
Keypoint = namedtuple("Keypoint", "x y diameter")

def create_analyser():
    return analysis.BlobAnalysis()

def analyse_image(analyser: analysis.BlobAnalysis, image):
    analyser.analyse(image)
    keypoints = analyser.keypoint_tuples()
    # Convert float values to integers in namedtuples for LabVIEW compatibility
    return [Keypoint(int(kp.x), int(kp.y), int(kp.diameter)) for kp in keypoints]

