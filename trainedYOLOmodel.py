"""Download (if needed) and verify the YOLOv8 nano weights used by the app."""

from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")
    print(f"Model loaded successfully with {len(model.names)} known classes.")
