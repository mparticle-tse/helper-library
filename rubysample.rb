# load the gem
require 'mparticle'
require 'date'
config = MParticle::Configuration.new
config.api_key = 'APP_KEY'
config.api_secret = 'APP_SECRET'
# config.debugging = true

api_instance = MParticle::EventsApi.new(config)

batch = MParticle::Batch.new
batch.timestamp_unixtime_ms = DateTime.now.strftime('%Q').to_i
batch.environment = 'development'

## user identities
user_identities = MParticle::UserIdentities.new
user_identities.customerid = 'rubyuser'
user_identities.email = 'rubyuser@example.com'
batch.user_identities = user_identities

batch.mpid = 600868121729048600
batch.mp_deviceid = "59780f39-d7a0-4ebe-9950-280f937c29e2"

## custom event
app_event = MParticle::AppEvent.new
app_event.event_name = 'Test event'
app_event.custom_event_type = 'navigation'
app_event.custom_attributes = { 'Test key' => 'Test value' }
app_event.custom_flags = {
  'answer': 42,
  'question': 'What is the answer to life, the universe, and everything?',
  'dolphins': [
      'So long',
      'Thanks for all the fish'
  ]
}

## screen view event
screen_view_event = MParticle::ScreenViewEvent.new
screen_view_event.custom_flags = {
  'answer': 42,
  'question': 'What is the answer to life, the universe, and everything?',
  'dolphins': [
      'So long',
      'Thanks for all the fish'
  ]
}

## commerce event
commerce_event = MParticle::CommerceEvent.new
commerce_event.custom_flags = {
  'answer': 42,
  'question': 'What is the answer to life, the universe, and everything?',
  'dolphins': [
      'So long',
      'Thanks for all the fish'
  ]
}

batch.events = [MParticle::SessionStartEvent.new, app_event, screen_view_event, commerce_event, MParticle::SessionEndEvent.new]

begin
  # send events
  thread = api_instance.upload_events(batch) { |data, status_code, headers|
    if status_code == 202
      puts "Upload complete"
    end
  }
  # wait for the thread, otherwise process may exit too early
  thread.join
rescue MParticle::ApiError => e
  puts "Exception when calling mParticle: #{e.response_body}"
end
