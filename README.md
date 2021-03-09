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

