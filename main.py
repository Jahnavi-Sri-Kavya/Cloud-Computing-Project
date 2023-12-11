import tensorflow
# from google.colab import auth
# auth.authenticate_user()
import os
from google.cloud import storage

from flask import Flask,render_template,request
from model import restore_model
from forms import Form
from model import restore_model
import numpy as np

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials\key-file.json"
# def download_file_from_gcs(bucket_name, file_name, destination_path):
#     """Download file from GCS."""
#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     blob.download_to_filename(destination_path)


# download_file_from_gcs('storage_buckets', 'diabetes.csv', 'data')
import subprocess
from google.cloud import storage

def download_dataset(bucket_path, destination_path):
    command = f"gsutil cp {bucket_path} {destination_path}"
    subprocess.run(command, shell=True)


bucket_path = "gs://csvstoragedata/diabetes.csv"
destination_path = "data"

download_dataset(bucket_path, destination_path)



app = Flask(__name__)
app.secret_key = 'development key'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect.html', methods=['GET', 'POST'])
def detect():
    form = Form(request.form)
    if request.method == 'POST' : #and form.validate():
        test_values = np.array([[form.pregnancies.data,form.glucose.data,form.bloodPressure.data,form.skinThickness.data,form.insulin.data,form.bmi.data,form.diabetesPedigreeFunction.data,form.age.data],], dtype=np.float32)
        result = restore_model(test_values)
        print("************")
        if(result):
            result = "Diabeties Postive,Time to go for sugar free"
        else:
            result = "Diabeties Negative,Time for dessert !"
    else:
        result = None
    iframe = 'details.html'

    return render_template('detect.html', form=form, result=result,iframe=iframe)

@app.route('/details.html')
def details():
    return render_template('details.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')



if __name__ == '__main__':
   app.run(debug = True)

  
