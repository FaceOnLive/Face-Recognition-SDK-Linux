import gradio as gr
import requests
import json
from PIL import Image

def compare_face(frame1, frame2):
    url = "http://127.0.0.1:8000/api/compare_face"
    files = {'image1': open(frame1, 'rb'), 'image2': open(frame2, 'rb')}

    r = requests.post(url=url, files=files)
    faces = None

    try:
        image1 = Image.open(frame1)
        image2 = Image.open(frame2)

        face1 = None
        face2 = None
        data = r.json().get('data')
        if data.get('face1') is not None:
            face = data.get('face1')
            x1 = face.get('x1')
            y1 = face.get('y1')
            x2 = face.get('x2')
            y2 = face.get('y2')
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 >= image1.width:
                x2 = image1.width - 1
            if y2 >= image1.height:
                y2 = image1.height - 1

            face1 = image1.crop((x1, y1, x2, y2))
            face_image_ratio = face1.width / float(face1.height)
            resized_w = int(face_image_ratio * 150)
            resized_h = 150

            face1 = face1.resize((int(resized_w), int(resized_h)))

        if data.get('face2') is not None:
            face = data.get('face2')
            x1 = face.get('x1')
            y1 = face.get('y1')
            x2 = face.get('x2')
            y2 = face.get('y2')

            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 >= image2.width:
                x2 = image2.width - 1
            if y2 >= image2.height:
                y2 = image2.height - 1

            face2 = image2.crop((x1, y1, x2, y2))
            face_image_ratio = face2.width / float(face2.height)
            resized_w = int(face_image_ratio * 150)
            resized_h = 150

            face2 = face2.resize((int(resized_w), int(resized_h)))
        
        if face1 is not None and face2 is not None:
            new_image = Image.new('RGB',(face1.width + face2.width + 10, 150), (80,80,80))

            new_image.paste(face1,(0,0))
            new_image.paste(face2,(face1.width + 10, 0))
            faces = new_image.copy()
        elif face1 is not None and face2 is None:
            new_image = Image.new('RGB',(face1.width + face1.width + 10, 150), (80,80,80))

            new_image.paste(face1,(0,0))
            faces = new_image.copy()
        elif face1 is None and face2 is not None:
            new_image = Image.new('RGB',(face2.width + face2.width + 10, 150), (80,80,80))

            new_image.paste(face2,(face2.width + 10, 0))
            faces = new_image.copy()
    except:
        pass

    return [r.json(), faces]

with gr.Blocks() as demo:
    gr.Markdown(
        """
    # Face Recognition
    Get your own Face Recognition Server by duplicating this space.<br/>
        Or run on your own machine using docker.<br/>
    ```docker run -it -p 7860:7860 --platform=linux/amd64 \
	-e LICENSE_KEY="YOUR_VALUE_HERE" \
	registry.hf.space/faceonlive-face-recognition-sdk:latest ```<br/><br/>
    Contact us at https://faceonlive.com for issues and support.<br/>
    """
    )
    with gr.Row():
        with gr.Column():
            compare_face_input1 = gr.Image(type='filepath', height=480)
            gr.Examples(['gradio/examples/1.jpg', 'gradio/examples/2.jpg'], 
                        inputs=compare_face_input1)
            compare_face_button = gr.Button("Compare Face")
        with gr.Column():
            compare_face_input2 = gr.Image(type='filepath', height=480)
            gr.Examples(['gradio/examples/3.jpg', 'gradio/examples/4.jpg'], 
                        inputs=compare_face_input2)
        with gr.Column():
            compare_face_output = gr.Image(type="pil", height=150)
            compare_result_output = gr.JSON(label='Result')

    compare_face_button.click(compare_face, inputs=[compare_face_input1, compare_face_input2], outputs=[compare_result_output, compare_face_output])

demo.launch(server_name="0.0.0.0", server_port=7860)