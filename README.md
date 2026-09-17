<div align="center">

# 🛒 Automated Planogram Compliance & Shelf Monitoring

**A real-time computer vision pipeline utilizing OpenCV and YOLOv8 to automate retail shelf audits, detect out-of-stock items, and ensure planogram compliance.**

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
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage & Configuration](#-usage--configuration)
- [Training a Custom Model](#-training-a-custom-model)
- [License](#-license)

---

## 📌 About the Project

**Automated Planogram Compliance** is a computer vision pipeline that turns an ordinary shelf-facing camera feed into a live inventory and compliance dashboard. It uses **OpenCV** for robust image preprocessing and **YOLOv8** (Ultralytics' state-of-the-art object detection model) to detect, classify, and count items in each video frame. 

The goal of this project is to demonstrate an end-to-end computer vision architecture — from raw video input and real-time deep learning inference to a human-readable stock report. It is structured so the detection logic can be easily swapped for a custom-trained, SKU-specific model to suit hyper-local delivery or large-scale retail operations.

## ❗ Problem Statement

Manual shelf audits and planogram checks are some of the most expensive and error-prone tasks in supply chain and retail operations:
- 🕒 Store staff must physically walk the aisles to check stock levels, which is highly inefficient.
- 🙈 Understocked or empty shelf spaces often go unnoticed, leading directly to lost revenue.
- 📋 Stock checks are usually logged manually, leaving centralized operations teams without real-time visibility into shelf health.

## ✅ Solution

This project automates shelf monitoring using deep learning:
- A camera continuously streams the retail shelf.
- **OpenCV** handles frame extraction and resizing.
- **YOLOv8** analyzes every frame in real-time to detect individual items and bounding boxes.
- Detected items are tallied against a configurable **low-stock threshold**, instantly flagging items that need restocking via a dynamic Tkinter GUI.

## ✨ Features

| Feature | Description |
|---|---|
| 🎥 **Looped Video Processing** | Ingests a retail shelf video feed, simulating a continuous live camera stream. |
| 🤖 **Real-Time YOLOv8 Detection** | Runs Ultralytics' YOLOv8n model on every frame to detect and label objects. |
| 📊 **Live Stock Report** | A sidebar panel lists every detected product category along with its current on-screen count. |
| 🎨 **Color-Coded Status** | Counts are color-coded — 🟢 healthy, 🟠 low stock, 🔴 out-of-stock — for an at-a-glance read. |
| 🖼️ **Annotated Video Feed** | Bounding boxes and class labels are drawn directly onto the video stream in real-time. |

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.8+ | Core application language |
| **Object Detection** | [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) | Real-time detection and classification |
| **Image Processing** | OpenCV (`opencv-python`) | Reading, resizing, bounding box rendering, and frame manipulation |
| **GUI Framework** | Tkinter & Pillow (`PIL`) | Desktop dashboard rendering |

## ⚙️ How It Works

The application follows a continuous processing loop:

```text
 ┌─────────────┐   ┌───────────────┐   ┌────────────────┐   ┌───────────────┐   ┌────────────────┐
 │  Video Feed │ → │  YOLOv8 Model │ → │ Object Counting │ → │  Tkinter GUI  │ → │  Stock Alerts   │
 │ (OpenCV cv2)│   │  (inference)  │   │ (per class tally)│ │ (video + list)│   │ (color coding)  │
 └─────────────┘   └───────────────┘   └────────────────┘   └───────────────┘   └────────────────┘
