# FaceOnLive — Face Recognition SDK for Linux

Server-side face detection and 1:1 / 1:N face matching for Linux, exposed through a Python interface over the native engine. Runs entirely on your own server.

> Part of the [FaceOnLive](https://faceonlive.com) on-premises biometric SDK suite.

> 📦 **Download the full SDK:** this repository contains the **source/demo code only**. The complete SDK — engine libraries and model files, with the full project structure — is attached to the [**Releases**](../../releases) page. Download the archive and extract it over this project.

## Features
- Face detection and biometric template extraction.
- Face similarity comparison for verification and identification.
- On-premises and offline; suitable for backend / batch pipelines.

## Requirements
| | |
|---|---|
| OS | Linux x86-64 |
| Runtime | Python 3.8+ |
| Engine | `libttvfaceengine` (included under `engine/`) |

## Setup
1. Get a license key — free trial at **https://faceonlive.com**.
2. Provide the key via the `LICENSE_KEY` environment variable, or place it in `license.txt` (replace the `<YOUR_LICENSE_KEY>` placeholder).
3. Install Python dependencies and run the provided demo.

## Quick start (Python)
```python
from engine.header import *   # exposes the bindings below

init_sdk()                                  # ttv_init
t1 = extract_template(image1)               # ttv_extract_feature
t2 = extract_template(image2)
score = calculate_similarity(t1, t2)        # ttv_compare_feature  (0.0 – 1.0)
```

## API reference (Python bindings → native)
| Binding | Native | Description |
|---|---|---|
| `get_version()` | `ttv_version` | SDK version. |
| `get_deviceid()` | `ttv_get_hwid` | Machine hardware ID (for offline licensing). |
| `init_sdk()` / `init_sdk_offline()` | `ttv_init` / `ttv_init_offline` | Initialize online or offline. |
| `extract_template(image)` | `ttv_extract_feature` | Extract a face template. |
| `calculate_similarity(t1, t2)` | `ttv_compare_feature` | Compare two templates (`0.0–1.0`). |

## License & support
Requires a valid license key — get one at **[faceonlive.com](https://faceonlive.com)**. Keep `license.txt` out of version control. Questions: contact@faceonlive.com
