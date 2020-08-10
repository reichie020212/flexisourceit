# Test

### Install python3

	sudo apt install python3

### Install virtual environment

	sudo apt-get install python3-venv

### Create virtual environment

	python3 -m venv myvenv

### Activate virtual environment

	source myvenv/bin/activate

### Install Requirements

	python -m pip install --upgrade pip
	pip install -r requirements.txt

### Migrate

	python manage.py migrate

### Runserver

	python manage.py runserver

### Explanation
	Open Postman

	<domain> = localhost:8000 (depends on what port you will going to use)

	url: <domain>/registration/
	method: POST
	purpose: Creation of account
	sample data: {"username": "test_user", "password": "test2", "confirm_password": "test2", "first_name":"first1", "last_name":"last1"}
	output: "User has been created"

	url: <domain>/login/
	method: POST
	purpose: Account Login
	sample data: {"username": "test_user", "password": "test2"}
	output: {
	    "expiry": "2020-08-11T01:24:08.468679Z",
	    "token": "8d75a9ae3032355e687b533a747a0cd67543e727971d745ba805f1276aea61e2"
	}
	Take note of the "token", it will be use on other endpoint

	<token> = "8d75a9ae3032355e687b533a747a0cd67543e727971d745ba805f1276aea61e2"

	url: <domain>/stock/
	method: GET
	purpose: Show list of all stocks
	sample data: {}
	sample queryparameters: {}
	sample headers: Token <token>
	output: [
	    {
	        "id": 1,
	        "name": "stock4",
	        "price": 14.0
	    },
	    {
	        "id": 2,
	        "name": "stock2",
	        "price": 11.0
	    }
	]

	url: <domain>/stock/create/
	method: POST
	purpose: Create a new stock
	sample data: {"price": 14, "name": "stock3"}
	sample headers: Token <token>
	output: "Stock has been created"

	url: <domain>/stock/<id_of_stock>/
	method: POST
	purpose: Update a stock
	sample data: {"price": 19, "name": "stock3"}
	sample headers: Token <token>
	output: "Stock has been created"

	url: <domain>/stock/buy/
	method: POST
	purpose: Buy a stock
	sample data: {"quantity": 15, "name": "stock4"}
	sample headers: Token <token>
	output: {
	    "stock_id": 1,
	    "stock_name": "stock4",
	    "stock_quantity": 15
	}

	url: <domain>/stock/sell/
	method: POST
	purpose: Sell a stock
	sample data: {"quantity": 14, "name": "stock4"}
	sample headers: Token <token>
	output: {
	    "stock_id": 1,
	    "stock_name": "stock4",
	    "stock_quantity": 1
	}

	url: <domain>/stock/list/
	method: GET
	purpose: Show all stocks of your account
	sample data: {}
	sample queryparameters: {}
	sample headers: Token <token>
	output: [
	    {
	        "stock__name": "stock4",
	        "quantity": 1
	    }
	]

	url: <domain>/stock/total/?stock_name=<stock_name>
	method: GET
	purpose: Get total amount invested in a specific stock
	sample data: {}
	sample queryparameters: {'stock_name': stock4}
	sample headers: Token <token>
	output: {
	    "stock": "stock4",
	    "total": 14.0
	}