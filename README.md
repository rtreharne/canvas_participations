# Canvas Participations Report Generator

Version: 1.0
Author: Robert Treharne, University of Liverpool, 2024

## Overview

The `main.py` script will ask the user to input their `CANVAS_API_URL`, `CANVAS_API_TOKEN` and `course_id`.

A file called `output.csv` containing the course page views for each enrolled student, binned into hours, will be generated.

You can generate `CANVAS_API_TOKEN` at Account --> Settings on Canvas.

## Usage

### 1. Clone this repository

```{bash}
git clone https://github.com/rtreharne/canvas_participations.git
```

### 2. Create Virtual Environment and Install Python Modules

Windows:

```{base}
python -m virtualenv .venv
\.venv\Scripts\activate
pip install -r requirements.txt
```

Ubuntu/Mac OS
```{base}
python3 -m virtualenv .venv
/.venv/bin/activate
pip3 install -r requirements.txt
```

3. Run `main.py`

Windows:

```{bash}
python main.py
```

Ubuntu/Mac OS

```{bash}
python3 main.py
```