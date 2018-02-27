import os.path
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.httpserver
import json
import datetime
from tornado.options import define, options, parse_command_line

from paypalrestsdk import BillingPlan, BillingAgreement, configure
import paypal_config

define("port", default=5000, help="run on the given port", type=int)

configure({
    "mode": paypal_config.MODE,
    "client_id": paypal_config.CLIENT_ID,
    "client_secret": paypal_config.CLIENT_SECRET
})

base_dir = os.path.dirname(os.path.abspath(__file__))


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({'response': 'Hello Tornado PayPal !!'})

class CreateHandler(tornado.web.RequestHandler):
    def post(self):
        '''
            curl -v -X POST http://localhost:5000/create \
            -H "Content-Type:application/json" \
            -H "Authorization: Bearer Access-Token" \
            -d '{
              "name": "Plan with Regular and Trial Payment Definitions",
              "description": "Plan with regular and trial payment definitions.",
              "type": "fixed",
              "payment_definitions": [
              {
                "name": "Regular payment definition",
                "type": "REGULAR",
                "frequency": "MONTH",
                "frequency_interval": "2",
                "amount":
                {
                  "value": "100",
                  "currency": "USD"
                },
                "cycles": "12",
                "charge_models": [
                {
                  "type": "SHIPPING",
                  "amount":
                  {
                    "value": "10",
                    "currency": "USD"
                  }
                },
                {
                  "type": "TAX",
                  "amount":
                  {
                    "value": "12",
                    "currency": "USD"
                  }
                }]
              },
              {
                "name": "Trial payment definition",
                "type": "trial",
                "frequency": "week",
                "frequency_interval": "5",
                "amount":
                {
                  "value": "9.19",
                  "currency": "USD"
                },
                "cycles": "2",
                "charge_models": [
                {
                  "type": "SHIPPING",
                  "amount":
                  {
                    "value": "1",
                    "currency": "USD"
                  }
                },
                {
                  "type": "TAX",
                  "amount":
                  {
                    "value": "2",
                    "currency": "USD"
                  }
                }]
              }],
              "merchant_preferences":
              {
                "setup_fee":
                {
                  "value": "1",
                  "currency": "USD"
                },
                "return_url": "https://example.com/return",
                "cancel_url": "https://example.com/cancel",
                "auto_bill_amount": "YES",
                "initial_fail_amount_action": "CONTINUE",
                "max_fail_attempts": "0"
              }
            }'
        '''
        data = json.loads(self.request.body.decode('utf-8'))
        billing_plan_attributes = {
            "name": data['name'],
            "description": data['description'],
            "type": data['type'],
            "merchant_preferences": {
                "auto_bill_amount": "yes",
                "cancel_url": "https://example.com/cancel",
                "initial_fail_amount_action": "continue",
                "max_fail_attempts": "1",
                "return_url": 'https://example.com/success',
                "setup_fee": {
                    "currency": data['currency'],
                    "value": data['setup_fee']
                }
            },
            "payment_definitions": [
                {
                    "cycles": data['cycles'],
                    "frequency": data['frequency'],
                    "frequency_interval": data['frequency_interval'],
                    "name": data['payment_name'],
                    "type": data['payment_type'],
                    "amount": {
                        "currency": data['currency'],
                        "value": data['value']
                    },
                    "charge_models": [
                        {
                            "amount": {
                                "currency": data['currency'],
                                "value": data['shipping']
                            },
                            "type": "SHIPPING"
                        },
                        {
                            "amount": {
                                "currency": data['currency'],
                                "value": data['tax']
                            },
                            "type": "TAX"
                        }
                    ]
                }
            ]
        }
        billing_plan = BillingPlan(billing_plan_attributes)
        if billing_plan.create():
            msg = billing_plan.id
            print(
                "Billing Plan [%s] created successfully" % (msg))
        else:
            msg = billing_plan.error
            print(msg)

        self.write({"response": msg})

    def get(self):
        plans_created = []
        plans_active = []
        plans_created_query_dict = BillingPlan.all({"status": "CREATED",
                                                    "sort_order": "DESC"})
        plans_created = plans_created_query_dict.to_dict().get('plans')

        plans_active_query_dict = BillingPlan.all({"status": "ACTIVE",
                                                   "page_size": 5, "page": 0, "total_required": "yes"})
        plans_active = plans_active_query_dict.to_dict().get('plans')

        self.write({"response": {"plans_created": plans_created, "plans_active": plans_active}})


    def getMock(self):
        # Simulate Post Response Success
        response = {
          "id": "P-7DC96732KA7763723UOPKETA",
          "state": "CREATED",
          "name": "Plan with Regular and Trial Payment Definitions",
          "description": "Plan with regular and trial payment definitions.",
          "type": "FIXED",
          "payment_definitions": [
            {
              "id": "PD-0MF87809KK310750TUOPKETA",
              "name": "Regular payment definition",
              "type": "REGULAR",
              "frequency": "Month",
              "amount": {
                "currency": "USD",
                "value": "100"
              },
              "charge_models": [
                {
                  "id": "CHM-89H01708244053321UOPKETA",
                  "type": "SHIPPING",
                  "amount": {
                    "currency": "USD",
                    "value": "10"
                  }
                },
                {
                  "id": "CHM-1V202179WT9709019UOPKETA",
                  "type": "TAX",
                  "amount": {
                    "currency": "USD",
                    "value": "12"
                  }
                }
              ],
              "cycles": "12",
              "frequency_interval": "2"
            },
            {
              "id": "PD-03223056L66578712UOPKETA",
              "name": "Trial payment definition",
              "type": "TRIAL",
              "frequency": "Week",
              "amount": {
                "currency": "USD",
                "value": "9.19"
              },
              "charge_models": [
                {
                  "id": "CHM-7XN63093LF858372XUOPKETA",
                  "type": "SHIPPING",
                  "amount": {
                    "currency": "USD",
                    "value": "1"
                  }
                },
                {
                  "id": "CHM-6JY06508UT8026625UOPKETA",
                  "type": "TAX",
                  "amount": {
                    "currency": "USD",
                    "value": "2"
                  }
                }
              ],
              "cycles": "2",
              "frequency_interval": "5"
            }
          ],
          "merchant_preferences": {
            "setup_fee": {
              "currency": "USD",
              "value": "1"
            },
            "max_fail_attempts": "0",
            "return_url": "https://example.com/return",
            "cancel_url": "https://example.com/cancel",
            "auto_bill_amount": "YES",
            "initial_fail_amount_action": "CONTINUE"
          },
          "create_time": "2017-06-16T07:40:20.940Z",
          "update_time": "2017-06-16T07:40:20.940Z",
          "links": [
            {
              "href": "https://api.sandbox.paypal.com/v1/payments/billing-plans/P-7DC96732KA7763723UOPKETA",
              "rel": "self",
              "method": "GET"
            }
          ]
        }
        data = {}
        data['payment_definitions_id'] = response["id"]
        data['payment_definitions_url'] = "https://api.sandbox.paypal.com/v1/payments/billing-plans/{0}".format(data['payment_definitions_id'])

        self.write(data)


class ActivateHandler(tornado.web.RequestHandler):
    def post(self, status="1"):
        data = json.loads(self.request.body.decode('utf-8'))
        billing_plan = BillingPlan.find(data['id'])

        if status == "1":
            if billing_plan.activate():
                msg = "Billing Plan activated successfully"
                print(msg)
            else:
                msg = billing_plan.error
                print(msg)
        else:
            billing_plan_update_attributes = [{
                "op": "replace",
                "path": "/",
                "value": {
                    "state": "INACTIVE"
                }
            }]
            if billing_plan.replace(billing_plan_update_attributes):
                msg = "Billing Plan inactivated successfully"
                print(msg)
            else:
                msg = billing_plan.error
                print(msg)
        self.write({'response': msg})


class SubscribeHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        billing_agreement = BillingAgreement({
            "name": "Organization plan name",
            "description": "Agreement for " + data['name'],
            "start_date": (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "plan": {
                "id": data['id']
            },
            "payer": {
                "payment_method": "paypal"
            },
            "shipping_address": {
                "line1": "StayBr111idge Suites",
                "line2": "Cro12ok Street",
                "city": "San Jose",
                "state": "CA",
                "postal_code": "95112",
                "country_code": "US"
            }
        })
        if billing_agreement.create():
            for link in billing_agreement.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    msg = approval_url
        else:
            msg = billing_agreement.error
            print(msg)

        self.write({'response': msg })


class ExecuteHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        payment_token = data['token']
        billing_agreement_response = BillingAgreement.execute(payment_token)
        self.write({'response': billing_agreement_response.id })


class AgreementHandler(tornado.web.RequestHandler):
    def get(self):
        payment_token = self.get_argument('payment_token')
        billing_agreement = BillingAgreement.find(payment_token)
        print('billing_agreement', billing_agreement)
        self.write({'response': 'billing_agreement' })

    def put(self):
        data = json.loads(self.request.body.decode('utf-8'))
        billing_agreement_id = data['billing_agreement_id']
        billing_agreement = BillingAgreement.find(billing_agreement_id)
        value = {
                    "description": "New Description",
                    "name": "New Name",
                    "shipping_address": {
                        "line1": "StayBr111idge Suites",
                        "line2": "Cro12ok Street",
                        "city": "San Jose",
                        "state": "CA",
                        "postal_code": "95112",
                        "country_code": "US"
                    }
        }
        billing_agreement_update_attributes = [
            {
                "op": "replace",
                "path": "/",
                "value": value
            }
        ]

        self.write({'response': billing_agreement })


class PaymentHistoryHandler(tornado.web.RequestHandler):
    def get(self):
        payment_token = self.get_argument('payment_token')
        start_date, end_date = self.get_argument('start_date'), self.get_argument('end_date')
        billing_agreement = BillingAgreement.find(payment_token)
        transactions = billing_agreement.search_transactions(start_date, end_date)
        self.write({'response': transactions })


class SubscriptionsHandler(tornado.web.RequestHandler):
    def get(self):
        status = self.get_argument('status') # ACTIVE INACTIVE
        plans = []
        plans_query_dict = BillingPlan.all({"status": status,
                                            "sort_order": "DESC"})

        if plans_query_dict:
            plans = plans_query_dict.to_dict().get('plans')

        self.write({'response': plans })


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/hello", HelloHandler),
            (r"/plan", CreateHandler),
            (r"/activate/(\d+)", ActivateHandler),
            (r"/payment-history", PaymentHistoryHandler),
            (r"/subscriptions", SubscriptionsHandler),
            (r"/subscribe", SubscribeHandler),
            (r"/execute", ExecuteHandler),
            
            (r"/agreement", AgreementHandler),
            (r"/admin", HelloHandler),
            (r"/login", HelloHandler),
            (r"/logout", HelloHandler),
        ]
        settings = dict(
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            debug=True,
            login_url="/login",
            logout_url="/logout",
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address='0.0.0.0')
    print('server started ...{0}'.format(options.port))
    tornado.ioloop.IOLoop.instance().start()
