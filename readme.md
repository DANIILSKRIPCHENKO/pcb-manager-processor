## Installation

This is an example of how to list things you need to use the software and how to install them.
* Create virtual environment
```sh
python -m venv venv
```

* Activate virtual environment
```sh
venv\Scripts\activate
```

* Clone yolo v5 repo
```sh
git clone https://github.com/ultralytics/yolov5  # clone
```

* Intsall packages for yolo v5
```sh
py -m pip install -r yolov5\requirements.txt
```

* Intsall other packages
```sh
py -m pip install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

* Run application, swagger documentation will be available in http://127.0.0.1:8000/docs
```sh
cd src
uvicorn main:app --reload
```