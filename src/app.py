import os 
from os import environ
from time import sleep
from io import BytesIO
from flask import Flask, render_template, send_file
import pandas as pd 
import matplotlib.pyplot as plt
import jinja2
import s3fs
import boto3 as boto3
import io as io

app = Flask(__name__)

ACCESS_KEY = environ.get('AWS_ACCESS_KEY') 
SECRET_KEY = environ.get('AWS_SECRET_KEY') 
BUCKET = environ.get('Bucket_S3')
CSV1 = environ.get('S3_Bucket_First_CSV')
CSV2 = environ.get('S3_Bucket_Second_CSV')
print(' Here is the access key: ', ACCESS_KEY)
print(' Here is the access key: ', SECRET_KEY)
our_port = environ.get('port') 
s3 = boto3.resource('s3', aws_access_key_id = ACCESS_KEY , aws_secret_access_key = SECRET_KEY)

object1=s3.Object(BUCKET, CSV1)
object2=s3.Object(BUCKET, CSV2)
body = object1.get()['Body'].read().decode('utf-8')
body2 = object2.get()['Body'].read().decode('utf-8')
#print(body)
data = io.StringIO(body)
data2 = io.StringIO(body2)
first_data = pd.read_csv(data, sep = ",")
number2_data = pd.read_csv(data2, sep=",")
#print(first_data)
#print(second_data)
#print(first_data)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('/'),
])
app.jinja_loader = my_loader


def get_first_csv():
    #read data from my S3 Bucket
    #read environment variable
    '''
    s3_first = environ.get('S3_Bucket_First_CSV')
    if s3_first:
        print('Found environment variable! {s3_first}')
    else:
        print('No environment path variable found')
    print(s3_first)
    '''
    #first_data = pd.read_csv(s3_first)
    #print(first_data)
    #CODE DOES NOT CHANGED
    #first_data = pd.read_csv('first.csv')
    #print(first_data)
    fig, ax = plt.subplots()
    fig.set_size_inches(len(first_data['sepal.length']) *  0.1, len(first_data['sepal.width'] ) * 0.1)
    # scatter the data and color by variety type.
    #Setosa = red / Versicolor = Yellow / Virgincia = Blue
    colors = {'Setosa':'r', 'Versicolor':'y', 'Virginica':'b'}
    for i in range(len(first_data['sepal.length'])):
        ax.scatter(first_data['sepal.length'][i], first_data['sepal.width'][i], c=colors[first_data['variety'][i]]) 
        ax.scatter(first_data['petal.length'][i], first_data['petal.width'][i], c=colors[first_data['variety'][i]])
    # set a title and labels
    ax.set_title('First Dataset')
    ax.set_xlabel('length')
    ax.set_ylabel('width')
    #save to image.
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    #return send_file(img, mimitype='image/png')
    #encoded_img = base64.encodebytes(img.getvalue()).decode('ascii')
    return img

def get_second_csv():

    '''
    s3_second = environ.get('S3_Bucket_Second_CSV')
    if s3_second:
        print('Found environment variable! {s3_second}')
    else:
        print('No environment path variable found')
    print(s3_second)
    second_data = pd.read_csv(s3_second)
    '''
    second_data = number2_data
    #print(second_data)
    second_data = second_data.drop(['Unnamed: 0'], axis=1).drop(['variety'], axis=1)
    second_data.plot.line(title='Second Dataset')
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/second.png', methods= ['GET'])
def second_csv():
    img = get_second_csv()
    return send_file(img, mimetype='image/png', cache_timeout=0)
    
@app.route('/first.png')
def first_csv():
    img = get_first_csv()
    return send_file(img, mimetype='image/png', cache_timeout=0)

def check_for_secret():    
    s = environ.get('AWS_ACCESS_KEY')   
    s2 =  environ.get('AWS_SECRET_KEY')  
    if s:        
        print('We have a secret! ',s , s2)    
    else:        
        print('No secrets for us')
def check_for_env_var():    
    v = environ.get('MY_VAR')    
    v2 = environ.get('MY_VAR2')
    if v:        
        print('We have an environment variable! ', v, v2)    
    else:        
        print('No environment variables for us')

def hello():
    while True:
            print('Hello!')
            check_for_secret()
            check_for_env_var()
            print()
            print(s3)
            sleep(5)

def access_check():
    v3 = environ.get('S3_Bucket_First_CSV')
    print('path to bucket: ', v3)
    v3 = v3 + "13"
    print(v3)
    #read_check = pd.read_csv('s3://cse427-ahvo/lab1/number1.csv')
    #print(read_check)

if __name__ == '__main__':

    #access_check()
    #print(s3)
    #hello()
    #print("hello")
    #print(second_data)
    app.run(host='0.0.0.0', port=our_port)          