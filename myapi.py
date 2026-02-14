from flask import Flask, render_template, request
from keras.models import load_model
from keras.models import Model
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
import keras
from tensorflow.python.platform import gfile
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import os

app = Flask(__name__)

p = {}
labels=['ACA (Adenocarcinoma)','N (Normal)','SCC (Squamous Cell Carcinoma)']
corrlist=[]

# functions

def getmyarray(list1):
  for sublist in list1:
    for i in sublist:
      corrlist.append(i)
  return corrlist

def getpredres(arr): 
  max=arr[0]
  ct=0
  for x in arr:
    if(x>max):
      max=x
  for a in arr:
    ct+=1
    if(a==max):
      break   
  return labels[ct-1]


@app.route('/', methods=['GET', 'POST'])
def main():
    
    return render_template('new.html')

@app.route('/user_manual', methods=['GET', 'POST'])
def user_manual():
    if request.method == 'POST':
        
        return redirect(url_for('/'))

    return render_template('new2.html')


@app.route('/submit', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = 'static/' + img.filename
        img.save(img_path)

    img = image.load_img(img_path, target_size = (150, 150))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)

    tflite_model_file = 'static/model/model.tflite'
    with open(tflite_model_file, 'rb') as fid:
      tflite_model = fid.read()
    interpreter = tf.lite.Interpreter(model_content=tflite_model)
    interpreter.allocate_tensors()
    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]
    prediction = []
    interpreter.set_tensor(input_index, img)
    interpreter.invoke()
    prediction.append(interpreter.get_tensor(output_index))
    predicted_label = np.argmax(prediction)
    
    return render_template('new.html', prediction = labels[predicted_label], img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)