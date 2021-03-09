## PYTHON FLASK SERVER FOR INVESTMENT APP

### Python/Flask

`https://investment-app7.herokuapp.com/api/user_risk_profile`

To download locally

### `python3 -m venv venv`

### `. venv/bin/activate`

### `pip3 install -r requirements.txt`

### `export FLASK_APP=app.py`
### `export FLASK_ENV=development`

### `flask run`


### APIs:

## GET USER'S RISK PROFILE API (POST):
### `http://localhost:5000/api/user_risk_profile`

OR

### `https://investment-app7.herokuapp.com/api/user_risk_profile`

Examples of post data:
`
{
    "assets": [
    {
        "asset": "Treasury Bills",
        "amount": 650000
    }
]
}
`

`
{
    "assets": [
    {
        "asset": "Discovery Fund",
        "amount": 100000
    },
       {
        "asset": "Ethical Fund",
        "amount": 200000
    },
    {
        "asset": "Foreign Stocks",
        "amount": 350000
    },
       {
        "asset": "Local Stocks",
        "amount": 550000
    }
]
}
`

`
{
    "assets": [
    {
        "asset": "Fixed Income Fund",
        "amount": 150000
    },
       {
        "asset": "Money Market Fund",
        "amount": 100000
    },
       {
        "asset": "Easy Will",
        "amount": 40000
    }
]
}
`
Example of response:
`
{
    "profile": "Your risk rating is Low, and your investment type is Capital Preservation"
}
`

#### Function that return the user's weighted risk score
The function takes the input of the user's investment assets(and amounts) and a model the investments types and calculates the weighted scores of each investment assets.

`
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
`