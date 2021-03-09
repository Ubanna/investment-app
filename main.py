# import necessary dependencies
from flask import Flask, request, jsonify
import pandas as pd
from itertools import zip_longest
from collections import defaultdict
from operator import itemgetter

app = Flask(__name__)

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
        return "Your risk rating is Low, and your investment type is Capital Preservation"
    elif user_score[0]["rating"] == "Low-2":
        return "Your risk rating is Low, and your investment type is Income"
    elif user_score[0]["rating"] == "Moderate":
        return "Your risk rating is Moderate, and your investment type is Income & Growth"
    elif user_score[0]["rating"] == "High":
        return "Your risk rating is High, and your investment type is Growth"
    else:
        return "Your risk rating is Very High, and your investment type is Aggressive Growth"