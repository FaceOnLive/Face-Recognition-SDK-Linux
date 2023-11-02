import sys
sys.path.append('.')

from flask import Flask, request, jsonify
from time import gmtime, strftime
import os
import base64
import json
import cv2
import numpy as np

from facewrapper.facewrapper import ttv_version
from facewrapper.facewrapper import ttv_get_hwid
from facewrapper.facewrapper import ttv_init
from facewrapper.facewrapper import ttv_init_offline
from facewrapper.facewrapper import ttv_extract_feature
from facewrapper.facewrapper import ttv_compare_feature

app = Flask(__name__) 

app.config['SITE'] = "http://0.0.0.0:8000/"
app.config['DEBUG'] = False

licenseKey = os.environ.get("LICENSE_KEY")
licensePath = "license.txt"
modelFolder = os.path.abspath(os.path.dirname(__file__)) + '/facewrapper/dict'

version = ttv_version()
print("version: ", version.decode('utf-8'))

ret = ttv_init(modelFolder.encode('utf-8'), licenseKey.encode('utf-8'))
if ret != 0:
    print(f"online init failed: {ret}");

    hwid = ttv_get_hwid()
    print("hwid: ", hwid.decode('utf-8'))

    ret = ttv_init_offline(modelFolder.encode('utf-8'), licensePath.encode('utf-8'))
    if ret != 0:
        print(f"offline init failed: {ret}")
        exit(-1)
    else:
        print(f"offline init ok")

else:
    print(f"online init ok")

@app.route('/api/compare_face', methods=['POST'])
def compare_face():
    file1 = request.files['image1']
    image1 = cv2.imdecode(np.fromstring(file1.read(), np.uint8), cv2.IMREAD_COLOR)
    if image1 is None:
        result = "image1: is null!"
        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    file2 = request.files['image2']
    image2 = cv2.imdecode(np.fromstring(file2.read(), np.uint8), cv2.IMREAD_COLOR)
    if image2 is None:
        result = "image2: is null!"
        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    
    faceRect1 = np.zeros([4], dtype=np.int32)
    feature1 = np.zeros([2048], dtype=np.uint8)
    featureSize1 = np.zeros([1], dtype=np.int32)

    ret = ttv_extract_feature(image1, image1.shape[1], image1.shape[0], faceRect1, feature1, featureSize1)
    if ret <= 0:
        if ret == -1:
            result = "license error!"
        elif ret == -2:
            result = "init error!"
        elif ret == 0:
            result = "image1: no face detected!"

        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    faceRect2 = np.zeros([4], dtype=np.int32)
    feature2 = np.zeros([2048], dtype=np.uint8)
    featureSize2 = np.zeros([1], dtype=np.int32)

    ret = ttv_extract_feature(image2, image2.shape[1], image2.shape[0], faceRect2, feature2, featureSize2)
    if ret <= 0:
        if ret == -1:
            result = "license error!"
        elif ret == -2:
            result = "init error!"
        elif ret == 0:
            result = "image2: no face detected!"

        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    similarity = ttv_compare_feature(feature1, feature2)
    if similarity > 0.7:
        result = "same"
    else:
        result = "different"
  
    status = "ok"
    response = jsonify(
    {
        "status": status, 
        "data": {
            "result": result, 
            "similarity": float(similarity), 
            "face1": {"x1": int(faceRect1[0]), "y1": int(faceRect1[1]), "x2": int(faceRect1[2]), "y2" : int(faceRect1[3])}, 
            "face2": {"x1": int(faceRect2[0]), "y1": int(faceRect2[1]), "x2": int(faceRect2[2]), "y2" : int(faceRect2[3])}, 
            }
    })

    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/api/compare_face_base64', methods=['POST'])
def coompare_face_base64():
    content = request.get_json()
    imageBase641 = content['image1']
    image1 = cv2.imdecode(np.frombuffer(base64.b64decode(imageBase641), dtype=np.uint8), cv2.IMREAD_COLOR)

    if image1 is None:
        result = "image1: is null!"
        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    imageBase642 = content['image2']
    image2 = cv2.imdecode(np.frombuffer(base64.b64decode(imageBase642), dtype=np.uint8), cv2.IMREAD_COLOR)

    if image2 is None:
        result = "image2: is null!"
        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    faceRect1 = np.zeros([4], dtype=np.int32)
    feature1 = np.zeros([2048], dtype=np.uint8)
    featureSize1 = np.zeros([1], dtype=np.int32)

    ret = ttv_extract_feature(image1, image1.shape[1], image1.shape[0], faceRect1, feature1, featureSize1)
    if ret <= 0:
        if ret == -1:
            result = "license error!"
        elif ret == -2:
            result = "init error!"
        elif ret == 0:
            result = "image1: no face detected!"

        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    faceRect2 = np.zeros([4], dtype=np.int32)
    feature2 = np.zeros([2048], dtype=np.uint8)
    featureSize2 = np.zeros([1], dtype=np.int32)

    ret = ttv_extract_feature(image2, image2.shape[1], image2.shape[0], faceRect2, feature2, featureSize2)
    if ret <= 0:
        if ret == -1:
            result = "license error!"
        elif ret == -2:
            result = "init error!"
        elif ret == 0:
            result = "image2: no face detected!"

        status = "ok"
        response = jsonify({"status": status, "data": {"result": result}})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    similarity = ttv_compare_feature(feature1, feature2)
    if similarity > 0.7:
        result = "same"
    else:
        result = "different"
  
    status = "ok"
    response = jsonify(
    {
        "status": status, 
        "data": {
            "result": result, 
            "similarity": float(similarity), 
            "face1": {"x1": int(faceRect1[0]), "y1": int(faceRect1[1]), "x2": int(faceRect1[2]), "y2" : int(faceRect1[3])}, 
            "face2": {"x1": int(faceRect2[0]), "y1": int(faceRect2[1]), "x2": int(faceRect2[2]), "y2" : int(faceRect2[3])}, 
            }
    })
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
