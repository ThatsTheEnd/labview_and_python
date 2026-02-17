import cv2
import numpy as np
from collections import namedtuple
import logging

logger = logging.getLogger(__name__)


class BlobAnalysis:
    def __init__(self):
        """Initialize BlobAnalysis detector with configured parameters."""
        try:
            logger.debug("Initializing SimpleBlobDetector parameters")
            params = cv2.SimpleBlobDetector_Params()
            params.minThreshold = 110
            params.maxThreshold = 255
            params.filterByColor = True
            params.blobColor = 0
            params.filterByArea = True
            params.maxArea = 150000
            
            logger.debug("Creating SimpleBlobDetector")
            self.detector = cv2.SimpleBlobDetector_create(params)
            self.keypoints = []
            logger.info("BlobAnalysis initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing BlobAnalysis: {type(e).__name__}: {e}", exc_info=True)
            raise

    def analyse(self, image):
        """Detect blobs in the given image."""
        try:
            logger.debug(f"Analyzing image with shape: {image.shape}")
            self.keypoints = self.detector.detect(image)
            logger.info(f"Detected {len(self.keypoints)} blobs")
            
        except Exception as e:
            logger.error(f"Error during blob detection: {type(e).__name__}: {e}", exc_info=True)
            raise

    def overlay_image(self, image):
        """Draw detected keypoints on the image."""
        try:
            logger.debug(f"Drawing {len(self.keypoints)} keypoints on image")
            result = cv2.drawKeypoints(image, self.keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            logger.debug("Keypoints drawn successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error drawing keypoints: {type(e).__name__}: {e}", exc_info=True)
            raise

    def keypoint_tuples(self):
        """Convert keypoints to tuples of (x, y, diameter)."""
        try:
            logger.debug(f"Converting {len(self.keypoints)} keypoints to tuples")
            tuples = []

            Keypoint = namedtuple("Keypoint", "x y diameter")
            for i, keypoint in enumerate(self.keypoints):
                (x, y) = keypoint.pt
                diameter = keypoint.size
                tuple_kp = Keypoint(x, y, diameter)
                tuples.append(tuple_kp)
                logger.debug(f"Keypoint {i}: x={x:.2f}, y={y:.2f}, diameter={diameter:.2f}")

            logger.info(f"Converted {len(tuples)} keypoints to tuple format")
            return tuples
            
        except Exception as e:
            logger.error(f"Error converting keypoints to tuples: {type(e).__name__}: {e}", exc_info=True)
            raise

