from flask import Flask, render_template, redirect, request, flash, url_for, session
import os
from werkzeug.utils import secure_filename
import spacy
from spacy import displacy
import re
from flaskext.markdown import Markdown
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app=Flask(__name__)
Markdown(app)
app.secret_key='dhfq34y3ur'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION PERMANENT']=False
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method=="POST":
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(url_for('home'))
        file = request.files['file']
        if file.filename == '':
            flash('Empty file')
            return redirect(url_for('home'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session['filename']=filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if request.form['Model']=="Model 1(inaccurate but with more labels)":
                return redirect(url_for('generate1'))
            elif request.form['Model']=="Model 2(relatively accurate)":
                return redirect(url_for('generate2'))
@app.route('/generateM1')
def generate1():
    ner=spacy.load(r'C:\Users\Lenovo\Desktop\CV new model\output\model-best')
    filename='uploads/'+session['filename']
    file=open(filename,'r',encoding='utf-8')
    file=file.read()
    file=re.sub('\n','',file)
    doc=ner(file)
    html=displacy.render(doc,style='ent')
    return render_template('generate.html',result=html)
@app.route('/generateM2')
def generate2():
    ner=spacy.load('en_core_web_sm')
    filename = 'uploads/' + session['filename']
    file = open(filename, 'r', encoding='utf-8')
    file = file.read()
    file = re.sub('\n', '', file)
    doc = ner(file)
    html=displacy.render(doc,style='ent')
    return render_template('generate.html', result=html)
if __name__=="__main__":
    app.run(debug=True)