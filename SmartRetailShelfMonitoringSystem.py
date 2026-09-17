"""Real-time shelf stock monitoring using YOLOv8, with a Tkinter dashboard."""

import argparse
import logging
import sys
import tkinter as tk
from pathlib import Path

import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

FRAME_SIZE = (640, 480)
UPDATE_INTERVAL_MS = 30


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--video", default="sample_video.mp4", help="Path to the shelf video file (default: %(default)s)"
    )
    parser.add_argument(
        "--model", default="yolov8n.pt", help="Path to the YOLOv8 model weights (default: %(default)s)"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Item count at or below which stock is flagged as low (default: %(default)s)",
    )
    return parser.parse_args()


class ShelfMonitorApp:
    """Tkinter dashboard that overlays live YOLOv8 detections on a looping video feed."""

    def __init__(self, video_path: str, model_path: str, low_stock_threshold: int):
        self.low_stock_threshold = low_stock_threshold
        self.paused = False

        logger.info("Loading YOLOv8 model from %s", model_path)
        self.model = YOLO(model_path)

        logger.info("Opening video source %s", video_path)
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Could not open video source: {video_path}")

        self._build_ui()

    def _build_ui(self) -> None:
        self.root = tk.Tk()
        self.root.title("Smart Retail Shelf Monitoring")
        self.root.geometry("1000x600")
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.video_label = tk.Label(self.root)
        self.video_label.pack(side="left")

        sidebar = tk.Frame(self.root, width=300)
        sidebar.pack(side="right", fill="y")

        tk.Label(sidebar, text="Shelf Stock Report", font=("Arial", 16, "bold")).pack(pady=10)
        self.product_text = tk.Text(sidebar, width=40, height=35, font=("Arial", 12))
        self.product_text.pack()

        self.pause_btn = tk.Button(sidebar, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(pady=5)
        tk.Button(sidebar, text="Quit", command=self.quit_app).pack(pady=5)

    def toggle_pause(self) -> None:
        self.paused = not self.paused
        self.pause_btn.config(text="Play" if self.paused else "Pause")

    def quit_app(self) -> None:
        self.cap.release()
        self.root.destroy()

    def _count_products(self, results) -> dict:
        counts: dict[str, int] = {}
        for cls in results[0].boxes.cls:
            label = self.model.names[int(cls)]
            counts[label] = counts.get(label, 0) + 1
        return counts

    def _render_stock_report(self, product_counts: dict) -> None:
        self.product_text.delete("1.0", tk.END)
        for product, count in product_counts.items():
            color = "red" if count == 0 else "orange" if count <= self.low_stock_threshold else "green"
            self.product_text.insert(tk.END, f"{product}: {count}\n")

            safe_tag = "".join(c if c.isalnum() else "_" for c in product)
            line_start = f"{self.product_text.index('end')} linestart -1l"
            line_end = f"{self.product_text.index('end')} lineend -1c"
            self.product_text.tag_add(safe_tag, line_start, line_end)
            self.product_text.tag_config(safe_tag, foreground=color)

    def _render_frame(self, frame) -> None:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
        self.video_label.imgtk = imgtk  # keep a reference so it isn't garbage-collected
        self.video_label.configure(image=imgtk)

    def update_frame(self) -> None:
        if not self.paused:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, FRAME_SIZE)
                results = self.model(frame, verbose=False)
                self._render_stock_report(self._count_products(results))
                self._render_frame(results[0].plot())
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop video

        self.video_label.after(UPDATE_INTERVAL_MS, self.update_frame)

    def run(self) -> None:
        self.update_frame()
        self.root.mainloop()


def main() -> int:
    args = parse_args()

    if not Path(args.video).exists():
        logger.error("Video file not found: %s", args.video)
        return 1

    try:
        app = ShelfMonitorApp(args.video, args.model, args.threshold)
    except Exception:
        logger.exception("Failed to start the shelf monitor")
        return 1

    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
