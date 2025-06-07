from flask import Flask, render_template, request, send_file, redirect, url_for, session
from Scraper.Scraper import google_maps_scraper
from Model.Model import find_similar_leads
import pandas as pd
import uuid
import os

"""this is the main runner file...."""

app = Flask(__name__)
app.secret_key = '123456789'
TEMP_FOLDER = 'temp'

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        industry = request.form['industry']
        location = request.form['location']
        
        temp_id = str(uuid.uuid4())
        session['temp_id'] = temp_id
        session['industry'] = industry
        session['location'] = location

        return redirect(url_for('loading'))

    return render_template('index.html')


@app.route('/loading')
def loading():
    return render_template('loading.html')  


@app.route('/processing')
def processing():
    temp_id = session.get('temp_id')
    industry = session.get('industry')
    location = session.get('location')

    if not all([temp_id, industry, location]):
        return redirect('/')

    raw_leads = google_maps_scraper(industry, location)

    similar_leads = find_similar_leads(raw_leads, industry)

    filename = f"{TEMP_FOLDER}/leads_{temp_id}.csv"
    similar_leads.to_csv(filename, index=False)

   
    session['result_file'] = filename

    return render_template('results.html',
                           leads=similar_leads.to_dict('records'),
                           industry=industry,
                           location=location,
                           filename=os.path.basename(filename))


@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(TEMP_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
