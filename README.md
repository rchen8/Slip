# Slip

### Installation

Make sure to use a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)  
```
pip install -r requirements.txt
brew install tesseract ffmpeg rabbitmq
```
Install [OpenCV 3.1.0](http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/)  
Install [RabbitMQ](http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html)

### To Run

```
sudo rabbitmq-server
celery -A lib.slide_match worker --loglevel=info
```

`python run.py` to start web server  
`python test.py` to temporarily test algorithm
