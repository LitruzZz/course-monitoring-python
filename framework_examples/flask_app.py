from flask import Flask, abort, render_template
from .common import DEVICES, find_device

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("devices.html", devices=DEVICES)

@app.get("/devices/<int:device_id>")
def detail(device_id):
    device = find_device(device_id)
    if device is None:
        abort(404)
    return device
