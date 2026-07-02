import os
import sys
import numpy as np
import ctypes, ctypes.util
from enum import Enum
from ctypes import *
from numpy.ctypeslib import ndpointer

def print_log(fmt): print("[LOG] \033[98m{}\033[00m" .format(fmt))
def print_info(fmt): print("[INFO] \033[92m{}\033[00m" .format(fmt))
def print_error(fmt): print("[ERR] \033[91m{}\033[00m" .format(fmt)) 
def print_warning(fmt): print("[WARNING] \033[93m{}\033[00m" .format(fmt))

class ENGINE_CODE(Enum):
    E_NO_FACE = 0
    E_ACTIVATION_ERROR = -1
    E_ENGINE_INIT_ERROR = -2    

lib_path = os.path.abspath(os.path.dirname(__file__)) + '/librecognition_v6.so'
lib = cdll.LoadLibrary(lib_path)

get_version = lib.ttv_version
get_version.argtypes = []
get_version.restype = ctypes.c_char_p

get_deviceid = lib.ttv_get_hwid
get_deviceid.argtypes = []
get_deviceid.restype = ctypes.c_char_p

init_sdk = lib.ttv_init
init_sdk.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
init_sdk.restype = ctypes.c_int32

init_sdk_offline = lib.ttv_init_offline
init_sdk_offline.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
init_sdk_offline.restype = ctypes.c_int32

extract_template = lib.ttv_extract_feature
extract_template.argtypes = [ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ctypes.c_int32, ctypes.c_int32, ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_int32, flags='C_CONTIGUOUS')]
extract_template.restype = ctypes.c_int

calculate_similarity = lib.ttv_compare_feature
calculate_similarity.argtypes = [ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'), ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS')]
calculate_similarity.restype = ctypes.c_double

DEFAULT_THRESHOLD = 0.67
def compare_face(image_mat1, image_mat2, match_threshold=DEFAULT_THRESHOLD):
    result = ""
    if image_mat1 is None:
        result = "Failed to open image1"
        return result, None, None, None

    if image_mat2 is None:
        result = "Failed to open image2"
        return result, None, None, None
    
    face_bbox_1 = np.zeros([4], dtype=np.int32)
    template_1 = np.zeros([2048], dtype=np.uint8)
    template_len_1 = np.zeros([1], dtype=np.int32)
    width_1 = image_mat1.shape[1]
    height_1 = image_mat1.shape[0]

    ret = extract_template(image_mat1, width_1, height_1, face_bbox_1, template_1, template_len_1)
    if ret <= 0:
        if ret == ENGINE_CODE.E_ACTIVATION_ERROR.value:
            result = "ACTIVATION ERROR"
        elif ret == ENGINE_CODE.E_ENGINE_INIT_ERROR.value:
            result = "ENGINE INIT ERROR"
        elif ret == ENGINE_CODE.E_NO_FACE.value:
            result = "NO FACE in image1"
        return result, None, None, None
    

    face_bbox_2 = np.zeros([4], dtype=np.int32)
    template_2 = np.zeros([2048], dtype=np.uint8)
    template_len_2 = np.zeros([1], dtype=np.int32)
    width_2 = image_mat2.shape[1]
    height_2 = image_mat2.shape[0]

    ret = extract_template(image_mat2, width_2, height_2, face_bbox_2, template_2, template_len_2)
    if ret <= 0:
        if ret == ENGINE_CODE.E_ACTIVATION_ERROR.value:
            result = "ACTIVATION ERROR"
        elif ret == ENGINE_CODE.E_ENGINE_INIT_ERROR.value:
            result = "ENGINE INIT ERROR"
        elif ret == ENGINE_CODE.E_NO_FACE.value:
            result = "NO FACE in image2"
        return result, None, None, None

    match_score = calculate_similarity(template_1, template_2)
    if match_score > match_threshold:
        result = "SAME PERSON"
    else:
        result = "DIFFERENT PERSON"

    return result, match_score, [face_bbox_1, face_bbox_2], [template_1[:template_len_1[0]], template_2[:template_len_2[0]]]
