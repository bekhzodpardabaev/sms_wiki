# SEND SMS

```
pip install twilio
```

settings.py

```
# ESKIZ
ESKIZ_EMAIL = 'XXX'
ESKIZ_PASSWORD = 'XXX'
ESKIZ_API_TOKEN = 'XXX'

# TWILIO
TWILIO_ACCOUNT_SID = 'XXX'
TWILIO_AUTH_TOKEN = 'XXX'
TWILIO_PHONE_NUMBER = '+998991234567'

# PLAYMOBILE
PLAY_MOBILE_LOGIN = 'XXX'
PLAY_MOBILE_PASSWORD = 'XXX'

SMS_PROVIDER = 'eskiz'  # playmobile, twilio, eskiz
```

to use send_sms function

```
from apps.common.utils.sms import send_sms


try:
    
    send_sms(phone_number, message) # phone_number = "+998901234567", message = "Hello World"
    
except (requests.ConnectionError, requests.ConnectTimeout , requests.Timeout):
    
    raise serializers.ValidationError("request_connection_error")
```