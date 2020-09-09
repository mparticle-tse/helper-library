var mParticle = require('mparticle');

var api = new mParticle.EventsApi(new mParticle.Configuration(
    'APP_KEY',
    'APP_SECRET'));

var batch = new mParticle.Batch(mParticle.Batch.Environment.development);

// User Identities
batch.user_identities = new mParticle.UserIdentities();
batch.user_identities.customerid = 'nodeUser' // identify the user (required)
// User setAttributes
// arbitrary example allowing you to create a segment of users trial users
batch.user_attributes = {'hair color': 'brown'}

// Device Information
var device_info = new mParticle.DeviceInformation();
// set any IDs that you have for this user
device_info.ios_advertising_id = '07d2ebaa-e956-407e-a1e6-f05f871bf4e2';
device_info.android_advertising_id = 'a26f9736-c262-47ea-988b-0b0504cee874';
batch.device_info = device_info;

// Custom Event
var event = new mParticle.AppEvent(mParticle.AppEvent.CustomEventType.navigation,
  'Hello World');

batch.addEvent(event);

// // Commerce Event
var product = new mParticle.Product();
product.name = 'Example Product';
product.id = 'sample-sku';
product.price = 19.99;

var product_action = new mParticle.ProductAction('purchase');
product_action.products = [product];
product_action.tax_amount = 1.50;
product_action.total_amount = 21.49;

var commerce_event = new mParticle.CommerceEvent();
commerce_event.product_action = product_action;
commerce_event.timestamp_unixtime_ms = 1599681655000; //replace with time of transaction

batch.addEvent(commerce_event);

// Session EVENTS
var session_start = new mParticle.SessionStartEvent();
session_start.session_id = 12345678;
session_start.timestamp_unixtime_ms = 1599681655000;

session_end = new mParticle.SessionEndEvent();
session_end.session_id = session_start.session_id; // it's mandatory that these match
session_end.session_duration_ms = 1000;
session_end.timestamp_unixtime_ms = session_start.timestamp_unixtime_ms + session_end.session_duration_ms;

batch.addEvent(session_start);
batch.addEvent(session_end);
var body = [batch]; // {[Batch]} Up to 100 Batch objects

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};

api.bulkUploadEvents(body, callback);
