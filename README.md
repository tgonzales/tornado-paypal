# tornado-paypal
Integration tornado with paypal

## Configuration

Get your client credentials from https://developer.paypal.com/ and put them in a `paypal_config.py` file:

    $ cat paypal_config.py
    MODE = "sandbox"
    CLIENT_ID = "<client id from sandbox>"
    CLIENT_SECRET = "<client secret from sandbox>"

## Run the server

    python app.py
    // * Running on http://0.0.0.0:5000/
    // * server started ...5000

### Test Server in other tab terminal

    curl http://localhost:5000/hello
    // {"response": "Hello Tornado PayPal !!"}

### Get Subscriptions

    # active
    curl http://localhost:5000/subscriptions?status=ACTIVE
    // {"response": [{"update_time": "2018-02-23T16:58:16.968Z", "description": "desc subscription", "links": [{"href": "https://api.sandbox.paypal.com/v1/payments/billing-plans/P-1TB90350U70647744YOMURFA", "method": "GET", "rel": "self"}], "state": "ACTIVE", "create_time": "2018-02-23T16:57:38.196Z", "type": "FIXED", "id": "P-1TB90350U70647744YOMURFA", "name": "testSubscriptionService"}]}

    # inactive
    // {"response": null}


### Create Plan

    curl http://localhost:5000/plan \
    -H "Content-Type:application/json" \
    -H "Authorization: Bearer Access-Token" \
    -d '{
      "name": "Plan with Regular and Trial Payment Definitions",
      "description": "Plan with regular and trial payment definitions.",
      "type": "fixed",
      "currency": "BRL",
      "value": "120",
      "setup_fee": "1",
      "frequency": "MONTH",
      "frequency_interval": "2",
      "cycles": "12",
      "payment_name": "Regular payment definition",
      "payment_type": "REGULAR",
      "shipping": "9",
      "tax": "1"
    }'

    // {"response": "P-9SR04910L4554621F2K2LM6Q"}


### Get Plan Created and Active

    curl http://localhost:5000/plan
    // {"response": {"plans_active": [], "plans_created": [{"update_time": "2018-02-26T15:21:54.042Z", "description": "Plan with regular and trial payment definitions.", "links": [{"href": "https://api.sandbox.paypal.com/v1/payments/billing-plans/P-9SR04910L4554621F2K2LM6Q", "method": "GET", "rel": "self"}], "state": "CREATED", "create_time": "2018-02-26T15:21:54.042Z", "type": "FIXED", "id": "P-9SR04910L4554621F2K2LM6Q", "name": "Plan with Regular and Trial Payment Definitions"}]}}


### Activate Plan

    curl http://localhost:5000/activate/1 \
    -H "Content-Type:application/json" \
    -H "Authorization: Bearer Access-Token" \
    -d '{"id": "P-9SR04910L4554621F2K2LM6Q"}'
    //{"response": "Billing Plan activated successfully"}

### Deactivate

    curl http://localhost:5000/activate/0 \
    -H "Content-Type:application/json" \
    -H "Authorization: Bearer Access-Token" \
    -d '{"id": "P-9SR04910L4554621F2K2LM6Q"}'
    //{"response": "Billing Plan inactivated successfully"}


### Subscriptions

    curl http://localhost:5000/subscriptions?status=ACTIVE
    // {response: []}

### Subscribe
    
    curl http://localhost:5000/subscribe \
    -H "Content-Type:application/json" \
    -H "Authorization: Bearer Access-Token" \
    -d '{"id": "P-9SR04910L4554621F2K2LM6Q"}'

    // {"response": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=EC-9TG15785UX797991P"}

    # Execute
    curl http://localhost:5000/execute \
    -H "Content-Type:application/json" \
    -H "Authorization: Bearer Access-Token" \
    -d '{"token": "EC-9TG15785UX797991P"}'

    // {"response": "I-716N5KW43LES"}

### get Agreement

    curl http://localhost:5000/agreement?payment_token=I-716N5KW43LES
    // {"response": [{"update_time": "2018-02-23T16:58:16.968Z", "description": "desc do pos", "links": [{"href": "https://api.sandbox.paypal.com/v1/payments/billing-plans/P-1TB90350U70647744YOMURFA", "method": "GET", "rel": "self"}], "state": "ACTIVE", "create_time": "2018-02-23T16:57:38.196Z", "type": "FIXED", "id": "P-1TB90350U70647744YOMURFA", "name": "mwPOS"}, {"update_time": "2018-02-26T16:47:38.918Z", "description": "Plan with regular and trial payment definitions.", "links": [{"href": "https://api.sandbox.paypal.com/v1/payments/billing-plans/P-9SR04910L4554621F2K2LM6Q", "method": "GET", "rel": "self"}], "state": "ACTIVE", "create_time": "2018-02-26T15:21:54.042Z", "type": "FIXED", "id": "P-9SR04910L4554621F2K2LM6Q", "name": "Plan with Regular and Trial Payment Definitions"}]}