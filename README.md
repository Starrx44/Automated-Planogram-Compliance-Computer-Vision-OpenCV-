<div align="center">

# 🛒 Smart Retail Shelf Monitoring with YOLOv8

**A real-time computer vision system that watches a retail shelf, counts products with YOLOv8, and flags low or out-of-stock items through a live desktop dashboard.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-Video%20Processing-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Demo](#-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Training a Custom Model](#-training-a-custom-model)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📌 About the Project

**Smart Retail Shelf Monitoring** is a computer vision prototype that turns an ordinary shelf-facing camera feed into a live inventory dashboard. It uses **YOLOv8** (Ultralytics' state-of-the-art object detection model) to detect and count items in each video frame, then renders the results in a simple, responsive **Tkinter GUI** that any store associate could glance at.

The goal of this project is to demonstrate an end-to-end computer vision pipeline — from raw video input, through real-time inference, to a human-readable stock report — using a lightweight, easy-to-run stack. It's built as a portfolio-friendly proof of concept for AI-powered retail automation, and is intentionally structured so the detection and alerting logic can be swapped for a custom-trained, product-specific model with minimal changes.

## ❗ Problem Statement

Manual shelf audits are one of the most repetitive and error-prone tasks in retail operations:

- 🕒 Store staff must physically walk the aisles to check stock levels, which is slow and easy to skip during busy hours.
- 🙈 Understocked or empty shelf spaces often go unnoticed until a customer complains or a sale is lost.
- 📋 Stock checks are usually logged manually (or not at all), leaving no real-time visibility into shelf health.
- 💸 Lost sales from stockouts and excess labor spent on manual counting both eat directly into retail margins.

## ✅ Solution

This project automates shelf monitoring with computer vision instead of manual counting:

- A camera (or, in this demo, a recorded video) continuously streams the shelf.
- **YOLOv8** analyzes every frame in real time and detects individual items.
- Detected items are **tallied per category** to build a live count.
- Counts are compared against a configurable **low-stock threshold**, and the dashboard instantly highlights items that need restocking — no manual walkthroughs required.

The result is a always-on, visual stock report that updates itself frame by frame.

## 🎬 Demo

<div align="center">

**Application Screenshot**

![App Screenshot Placeholder](docs/screenshot.png)

**Live Demo GIF**

![Demo GIF Placeholder](docs/demo.gif)

</div>

<details>
<summary>📸 How to add your own screenshots/GIF</summary>

1. Create a `docs/` folder in the project root.
2. Add a screenshot of the running app as `docs/screenshot.png`.
3. Record a short screen capture (e.g. with ScreenToGif, OBS, or LICEcap) and save it as `docs/demo.gif`.
4. The image links above will automatically render once the files exist.

</details>

## ✨ Features

| Feature | Description |
|---|---|
| 🎥 **Looped Video Playback** | Plays a retail shelf video on repeat, simulating a continuous live camera feed. |
| 🤖 **Real-Time YOLOv8 Detection** | Runs Ultralytics' YOLOv8n model on every frame to detect and label objects on the shelf. |
| 📊 **Live Stock Report** | A sidebar panel lists every detected product category along with its current on-screen count, refreshed continuously. |
| 🎨 **Color-Coded Stock Status** | Counts are color-coded — 🟢 green for healthy stock, 🟠 orange for low stock, 🔴 red for out-of-stock — for an at-a-glance read. |
| ⏯️ **Pause / Play Control** | Freeze the video feed at any moment to inspect a specific frame, then resume playback. |
| ❌ **Quit Button** | Cleanly releases the video capture and closes the application from within the GUI. |
| 🖼️ **Annotated Video Feed** | Bounding boxes and class labels from YOLOv8 are drawn directly onto the video stream in real time. |

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.8+ | Core application language |
| **Object Detection** | [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) (`yolov8n.pt`) | Real-time detection and classification of shelf items |
| **Video Processing** | OpenCV (`opencv-python`) | Reading, resizing, and looping video frames |
| **Image Handling** | Pillow (`PIL`) | Converting OpenCV frames into a Tkinter-displayable format |
| **GUI Framework** | Tkinter | Desktop dashboard: video panel, stock sidebar, and controls |
| **Model Weights** | `yolov8n.pt` (COCO-pretrained nano model) | Lightweight, fast inference suited for real-time use |

## ⚙️ How It Works

The application follows a straightforward, continuous processing loop:

```
 ┌─────────────┐   ┌───────────────┐   ┌────────────────┐   ┌───────────────┐   ┌────────────────┐
 │  Video Feed │ → │  YOLOv8 Model │ → │ Object Counting │ → │  Tkinter GUI  │ → │  Stock Alerts   │
 │ (frame read)│   │  (inference)  │   │ (per class tally)│  │ (video + list)│   │ (color coding)  │
 └─────────────┘   └───────────────┘   └────────────────┘   └───────────────┘   └────────────────┘
```

1. **Video Feed** — `cv2.VideoCapture` reads the shelf video frame-by-frame; when the video ends, it loops back to frame zero for continuous playback.
2. **YOLOv8 Inference** — Each frame is resized and passed to the YOLOv8n model, which returns bounding boxes, class labels, and confidence scores for every detected object.
3. **Detection Counting** — The detected class labels are tallied into a dictionary (`{product: count}`) for that frame, giving a live snapshot of what's currently visible on the shelf.
4. **GUI Rendering** — The annotated frame (with bounding boxes drawn on it) is converted to a Tkinter-compatible image and displayed on the left panel, refreshed roughly every 30 ms.
5. **Stock Alerts** — The sidebar text is rebuilt each cycle: every product/count pair is written out and color-tagged — green if the count is healthy, orange if it's at or below the low-stock threshold, red if the count is zero — giving an instant visual stock status.

## 📂 Project Structure

```text
Smart_Retail_Shelf_Monitoring_with_YOLOv8/
├── SmartRetailShelfMonitoringSystem.py   # Main application: ShelfMonitorApp class, video loop, YOLOv8 inference, Tkinter GUI
├── trainedYOLOmodel.py                   # Minimal script to download/verify the YOLOv8 model weights
├── train_custom_model.py                 # Fine-tunes YOLOv8 on a custom Roboflow-exported product dataset
├── sample_video.mp4                      # Sample retail shelf footage used for the demo
├── yolov8n.pt                            # Pretrained YOLOv8 nano weights (auto-downloaded if missing)
├── requirements.txt                      # Pinned Python dependencies
├── .gitattributes                        # Git line-ending normalization rules
├── .gitignore                            # Excludes venvs, caches, and editor files from version control
├── LICENSE                               # MIT License
└── README.md                             # Project documentation
```

## 🚀 Installation

Follow these steps to get the project running locally.

**1. Clone the repository**

```bash
git clone https://github.com/Sara12-2/Smart_Retail_Shelf_Monitoring_with_YOLOv8.git
cd Smart_Retail_Shelf_Monitoring_with_YOLOv8
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. Install the required dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up Tkinter**

Tkinter ships with most standard Python installations. If it's missing (common on some Linux distributions), install it manually:

```bash
sudo apt-get install python3-tk
```

**5. Verify the YOLOv8 model**

The `yolov8n.pt` weights file is already included in the repository. If it's ever missing, Ultralytics will automatically download it the first time the script runs, or you can fetch it manually:

```bash
python trainedYOLOmodel.py
```

## ▶️ Usage

**1. Provide a video source**

The app looks for `sample_video.mp4` in the project root by default. Drop your own shelf footage into the folder using that exact filename, or point `--video` at a different file (see below).

**2. Run the application**

```bash
python SmartRetailShelfMonitoringSystem.py
```

All settings are optional command-line flags — nothing needs to be edited in the source:

```bash
python SmartRetailShelfMonitoringSystem.py --video my_shelf.mp4 --model yolov8s.pt --threshold 5
```

**3. Interact with the GUI**

| Panel | What you'll see |
|---|---|
| **Left — Video Panel** | The live video feed with YOLOv8 bounding boxes and labels drawn on top of detected objects. |
| **Right — Stock Report** | A continuously updating, color-coded list of detected products and their current counts. |
| **Controls** | `Pause` / `Play` toggles playback; `Quit` safely closes the video stream and exits the app. |

**Stock status legend:**

| Color | Meaning |
|---|---|
| 🟢 Green | Normal stock level |
| 🟠 Orange | Low stock (at or below the threshold) |
| 🔴 Red | Out of stock (count is zero) |

## 🔧 Configuration

The app is configured entirely through command-line flags — no source edits required:

| Flag | Default | Description |
|---|---|---|
| `--video` | `sample_video.mp4` | Path to the video file used as the shelf feed. |
| `--model` | `yolov8n.pt` | Swap for a larger YOLOv8 variant (`yolov8s.pt`/`m`/`l`/`x`) or a custom-trained model for improved accuracy. |
| `--threshold` | `3` | Count at or below which an item is flagged as low stock. |

Run `python SmartRetailShelfMonitoringSystem.py --help` to see all options.

> **Note:** Out of the box, this project uses YOLOv8's general-purpose, COCO-pretrained weights — detected "products" correspond to COCO object classes rather than specific SKUs. For production retail use, the model should be fine-tuned on a labeled dataset of the actual products stocked on your shelves.

## 🎯 Training a Custom Model

Out of the box the app runs on YOLOv8's COCO-pretrained weights, which only recognize generic object classes. To detect real product SKUs instead:

1. **Collect images** — photograph each product category from multiple angles, lighting conditions, and backgrounds (see dataset guidelines in the project notes).
2. **Label in [Roboflow](https://roboflow.com/)** — create a project, upload the images, draw bounding boxes per product class, apply augmentation, and export in **YOLOv8** format. This produces a `data.yaml` plus `images/` and `labels/` folders.
3. **Fine-tune** with the included training script:

   ```bash
   python train_custom_model.py --data path/to/data.yaml
   ```

   Key flags: `--epochs`, `--batch`, `--imgsz`, `--base-model` (defaults are tuned for small custom datasets). Run `python train_custom_model.py --help` for the full list.

4. **Use the fine-tuned weights** — no code changes needed, just point the app at the new checkpoint:

   ```bash
   python SmartRetailShelfMonitoringSystem.py --model runs/detect/shelf_custom/weights/best.pt
   ```

## 📈 Future Improvements

- [ ] 📷 **Live camera / CCTV integration** — replace the sample video with a real-time RTSP or webcam stream.
- [ ] 🧠 **Custom-trained detection model** — fine-tune YOLOv8 on real product/SKU images for accurate, retail-specific recognition.
- [ ] 📤 **Exportable stock reports** — save shelf reports to CSV/Excel for record-keeping and trend analysis.
- [ ] 🔔 **Automated alerts** — trigger email/SMS notifications when items go out of stock.
- [ ] 🌐 **Web-based dashboard** — move from a Tkinter desktop app to a browser-based UI (e.g. Flask/Streamlit) for remote monitoring.
- [ ] 📦 **Multi-shelf / multi-camera support** — monitor several shelves or store zones simultaneously.
- [ ] 📈 **Historical analytics** — track stock trends over time to inform restocking schedules.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository.
2. **Create a branch** for your feature or fix: `git checkout -b feature/your-feature-name`.
3. **Commit your changes** with clear, descriptive messages.
4. **Push** to your fork: `git push origin feature/your-feature-name`.
5. **Open a Pull Request** describing what you changed and why.

Feel free to open an [issue](https://github.com/Sara12-2/Smart_Retail_Shelf_Monitoring_with_YOLOv8/issues) first to discuss any significant changes.

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software, provided the original copyright notice is retained. See the [LICENSE](LICENSE) file for full details.

## 👩‍💻 Author

**Sara Manzoor**

- 🐙 GitHub: [@Sara12-2](https://github.com/Sara12-2)
- 💼 LinkedIn: [Sara Manzoor](https://www.linkedin.com/in/sara-manzoor-3a8a56365/)
- 🌐 Portfolio: [my-personal-portfolio-five-zeta.vercel.app](https://my-personal-portfolio-five-zeta.vercel.app/)


---

<div align="center">

If you found this project useful, consider giving it a ⭐ on GitHub!

</div>
