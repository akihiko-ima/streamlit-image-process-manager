# import cv2
# import numpy as np
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision


# class ObjectDetection:
#     def __init__(self, model_path: str, score_threshold: float = 0.5):
#         self.model_path = model_path
#         self.score_threshold = score_threshold
#         self.MARGIN = 20
#         self.ROW_SIZE = 10
#         self.FONT_SIZE = 1
#         self.FONT_THICKNESS = 2
#         self.TEXT_COLOR = (208, 22, 122)

#         # Initialize the detector
#         base_options = python.BaseOptions(model_asset_path=self.model_path)
#         options = vision.ObjectDetectorOptions(
#             base_options=base_options, score_threshold=self.score_threshold
#         )
#         self.detector = vision.ObjectDetector.create_from_options(options)

#     def __visualize(self, image: np.ndarray, detection_result) -> np.ndarray:
#         """Private method to draw bounding boxes and labels on the input image."""
#         for detection in detection_result.detections:
#             # Draw bounding box
#             bbox = detection.bounding_box
#             start_point = bbox.origin_x, bbox.origin_y
#             end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
#             cv2.rectangle(image, start_point, end_point, self.TEXT_COLOR, 3)

#             # Draw label and score
#             category = detection.categories[0]
#             category_name = category.category_name
#             probability = round(category.score, 2)
#             result_text = f"{category_name} ({int(probability * 100)}%)"
#             text_location = (
#                 self.MARGIN + bbox.origin_x,
#                 self.MARGIN + self.ROW_SIZE + bbox.origin_y,
#             )

#             # Draw the main text
#             cv2.putText(
#                 image,
#                 result_text,
#                 text_location,
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 self.FONT_SIZE,
#                 self.TEXT_COLOR,
#                 self.FONT_THICKNESS,
#             )

#         return image

#     def process_image(self, image_file: str) -> np.ndarray:
#         """Process the image, detect objects, and return the annotated image in RGB format."""
#         image = mp.Image.create_from_file(image_file)
#         detection_result = self.detector.detect(image)
#         image_copy = np.copy(image.numpy_view())
#         annotated_image = self.__visualize(image_copy, detection_result)

#         return annotated_image
