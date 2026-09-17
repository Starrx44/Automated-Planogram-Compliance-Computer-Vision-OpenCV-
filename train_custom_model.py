"""Fine-tune YOLOv8 on a custom product dataset exported from Roboflow.

Usage:
    python train_custom_model.py --data path/to/data.yaml
"""

import argparse
import logging
import sys

from ultralytics import YOLO

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data", required=True, help="Path to the data.yaml file exported from Roboflow"
    )
    parser.add_argument(
        "--base-model", default="yolov8n.pt", help="Pretrained checkpoint to fine-tune from (default: %(default)s)"
    )
    parser.add_argument("--epochs", type=int, default=100, help="Training epochs (default: %(default)s)")
    parser.add_argument("--imgsz", type=int, default=640, help="Training image size (default: %(default)s)")
    parser.add_argument("--batch", type=int, default=16, help="Batch size (default: %(default)s)")
    parser.add_argument(
        "--patience", type=int, default=20, help="Epochs with no improvement before early stopping (default: %(default)s)"
    )
    parser.add_argument("--name", default="shelf_custom", help="Run name under runs/detect/ (default: %(default)s)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    logger.info("Fine-tuning %s on %s for up to %d epochs", args.base_model, args.data, args.epochs)
    model = YOLO(args.base_model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        patience=args.patience,
        name=args.name,
    )

    metrics = model.val()
    logger.info("mAP@0.5: %.3f | mAP@0.5:0.95: %.3f", metrics.box.map50, metrics.box.map)
    logger.info("Best weights saved under runs/detect/%s/weights/best.pt", args.name)
    logger.info("Point the app at them with: python SmartRetailShelfMonitoringSystem.py --model runs/detect/%s/weights/best.pt", args.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
