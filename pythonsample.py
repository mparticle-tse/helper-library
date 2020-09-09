import mparticle
from mparticle import AppEvent, SessionStartEvent, SessionEndEvent, Batch

configuration = mparticle.Configuration()
configuration.api_key = 'APP_KEY'
configuration.api_secret = 'APP_SECRET'

batch = Batch()
## environment
batch.environment = 'development'

## user identities
identities = mparticle.UserIdentities()
identities.customerid = 'python'
identities.email = 'pythonuser@example.com'
batch.user_identities = identities

# arbitrary example allowing you to create a segment of users trial users
batch.user_attributes = {'Account type': 'trial', 'TrialEndDate':'2016-12-01'}

## device info
device_info = mparticle.DeviceInformation()
# set any IDs that you have for this user
device_info.ios_advertising_id = '07d2ebaa-e956-407e-a1e6-f05f871bf4e2'
device_info.android_advertising_id = 'a26f9736-c262-47ea-988b-0b0504cee874'
batch.device_info = device_info

## custom event
app_event = AppEvent('Hello Python', 'navigation')

## commerce event
product = mparticle.Product()
product.name = 'Example Product'
product.id = 'sample-sku'
product.price = 19.99

product_action = mparticle.ProductAction('purchase')
product_action.products = [product]
product_action.tax_amount = 1.50
product_action.total_amount = 21.49

commerce_event = mparticle.CommerceEvent(product_action)
commerce_event.timestamp_unixtime_ms = 1599682691000

## session events
session_start = mparticle.SessionStartEvent()
session_start.session_id = 12345678
session_start.timestamp_unixtime_ms = 1599682691000

session_end = mparticle.SessionEndEvent()
session_end.session_id = session_start.session_id # its mandatory that these match
session_end.session_duration_ms = 1000
session_end.timestamp_unixtime_ms = 1599682691000 + session_end.session_duration_ms


batch.events = [SessionStartEvent(), app_event, commerce_event, SessionEndEvent()]

# Raise the connection pool size if necessary (defaults to 1)
# configuration.connection_pool_size = 50

api_instance = mparticle.EventsApi(configuration)

# synchronous
try:
    api_instance.upload_events(batch)
    # or api_instance.bulk_upload_events([batch_1, batch_2])
    # both upload and bulk_upload also have _with_http_info signatures,
    # which will return the HTTP status info and headers, along with the body
except mparticle.rest.ApiException as e:
    print("Exception while calling mParticle: %s\n" % e)


# asynchronous, specifying your callback function
def my_callback(response):
    if type(response) is mparticle.rest.ApiException:
        print('An error occured: ' + str(response))
    else:
        #successful uploads will yield an HTTP 202 response and no body
        print("API called successfully.")

thread = api_instance.upload_events(batch, callback=my_callback)
