
# import necessary dependencies
from flask import Flask, request, jsonify, render_template, make_response
import pandas as pd
from itertools import zip_longest
from collections import defaultdict
from operator import itemgetter
from coredata import users
import os

# import os, subprocess, platform
from flask import Flask, render_template, url_for
from flask_weasyprint import HTML, render_pdf


app = Flask(__name__)


# https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb

# //buildpacks
# https://github.com/heroku/heroku-buildpack-apt
# https://github.com/chap/wkhtmltopdf-heroku-18-buildpack

# Function to include the risk rating in the user object
def addRatings(user, model):
    result = []
    for u in user:
        y = u["asset"]
        for items in model:
            ind = items["assets"]
            for i in ind:
                if i in y:
                    u["rating"] = items["rating"]
        result.append(u)
    return result

# Function to get the total sum of the user's investment(s)
def my_sum(obj):
    total = 0
    for val in obj:
        total += val["amount"]
    return total

# Function to group investments with the same risk rating
def groupRatings(obj):
    
    df = pd.DataFrame(obj)
    output = df.groupby('rating', as_index=False).sum().to_dict('records')
    
    return output

# Function that return the user's weighted risk score
def getCategory(user, model):
    data_with_ratings = addRatings(user, model)
    grouped_data = groupRatings(data_with_ratings)
    total = my_sum(grouped_data)
    new = []
    for item in grouped_data:
        avg = item["amount"] / total
        if item["rating"] == "Low-1":
            weight_score = avg * 2.5
        elif item["rating"] == "Low-2":
            weight_score = avg * 4.5
        elif item["rating"] == "Moderate":
            weight_score = avg * 6.5
        elif item["rating"] == "High":
            weight_score = avg * 8
        else:
            weight_score = avg * 9
        item["weighted_score"] = weight_score

    user_score = sorted(grouped_data, key=itemgetter('weighted_score'), reverse=True)
    if user_score[0]["rating"] == "Low-1":
        return "low"
    elif user_score[0]["rating"] == "Low-2":
        return "low-2"
    elif user_score[0]["rating"] == "Moderate":
        return "moderate"
    elif user_score[0]["rating"] == "High":
        return "high"
    else:
        return "very-high"

def getUsers():
    return users

def _get_pdfkit_config():
     """wkhtmltopdf lives and functions differently depending on Windows or Linux. We
      need to support both since we develop on windows but deploy on Heroku.

     Returns:
         A pdfkit configuration
     """
     if platform.system() == 'Windows':
         return pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
     else:
         WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
         return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

def get_account_statement():

    # Make a PDF straight from HTML in a string.
    html = render_template('statement.html')
    return render_pdf(HTML(string=html))

    # rendered = render_template('statement.html')
    # pdf = pdfkit.from_string(rendered, False, configuration=_get_pdfkit_config())
    #         # pdf = pdfkit.from_string(rendered, False, configuration=pdfkit_config)

    # response = make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=arm_engage_statement.pdf'

    # return response