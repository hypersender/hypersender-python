<p align="center"><img width="307" height="63" src="https://raw.githubusercontent.com/hypersender/hypersender-python/main/art/hy.svg" alt="Hypersender Logo"></p>

<p align="center">
<a href="https://pypi.org/project/hypersender/"><img src="https://img.shields.io/pypi/v/hypersender" alt="PyPI version"></a>
<a href="https://pypi.org/project/hypersender/"><img src="https://img.shields.io/pypi/pyversions/hypersender" alt="Python versions"></a>
<a href="https://github.com/hypersender/hypersender-python/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" alt="License"></a>
</p>

# Hypersender Python SDK

The official Python SDK for the [Hypersender](https://hypersender.com) **WhatsApp API**, **SMS API**, and **OTP API**. Send WhatsApp messages, build a WhatsApp bot in Python, send SMS from your own Android phone, and verify users with one-time codes, in a few lines of code.

- Plain methods with keyword arguments that return plain dictionaries
- One dependency ([httpx](https://www.python-httpx.org/)), fully typed, Python 3.9+
- Works with Django, Flask, FastAPI, or a simple script

## Installation

```bash
pip install hypersender
```

Get your API keys and instance IDs from the [Hypersender dashboard](https://app.hypersender.com), then set them as environment variables:

```bash
HYPERSENDER_WHATSAPP_API_KEY=
HYPERSENDER_WHATSAPP_INSTANCE_ID=
HYPERSENDER_SMS_API_KEY=
HYPERSENDER_SMS_INSTANCE_ID=
HYPERSENDER_OTP_API_KEY=
HYPERSENDER_OTP_INSTANCE_ID=
HYPERSENDER_ENTERPRISE_API_KEY=   # Enterprise accounts only
```

Set only the ones for the products you use. You can also pass them to the client: `Hypersender(whatsapp_api_key="...", whatsapp_instance_id="...")`.

## Send a WhatsApp message with Python

```python
from hypersender import Hypersender

hs = Hypersender()

hs.whatsapp.send_text("201234567890@c.us", "Hello from Python!")
```

A `chat_id` is the phone number with country code followed by `@c.us`. See [What is chatId?](https://docs.hypersender.com/v2/api-reference/whatsapp/what-is-chatid)

Send images, files, video, and voice notes from a URL or a local file:

```python
hs.whatsapp.send_image("201234567890@c.us", url="https://example.com/menu.png", caption="Today's menu")
hs.whatsapp.send_file("201234567890@c.us", file="invoice.pdf", caption="Your invoice")
```

Polls, locations, contact cards, reactions, typing indicators, and more:

```python
hs.whatsapp.send_poll("201234567890@c.us", "Lunch?", ["Pizza", "Sushi"])
hs.whatsapp.send_location("201234567890@c.us", 30.0444, 31.2357, title="Cairo office")
hs.whatsapp.start_typing("201234567890@c.us")
```

### Check if a number has WhatsApp

```python
result = hs.whatsapp.contacts.check_contact_exists("201234567890")
if result["numberExists"]:
    hs.whatsapp.send_text(result["chatId"], "Welcome!")
```

## Build a WhatsApp bot in Python

Hypersender sends incoming messages to your webhook URL. Reply with the SDK and you have a WhatsApp bot. Here is a complete echo bot with Flask:

```python
import hmac
import os

from flask import Flask, abort, request
from hypersender import Hypersender

app = Flask(__name__)
hs = Hypersender()
SECRET = os.environ["HYPERSENDER_WHATSAPP_WEBHOOK_SECRET"]  # the secret you set on the webhook


@app.post("/whatsapp/webhook")
def whatsapp_webhook():
    if not hmac.compare_digest(request.headers.get("Authorization", ""), SECRET):
        abort(401)

    event = request.get_json()
    message = event["data"]["payload"]
    if event["event"] == "message.any" and not message["fromMe"]:
        hs.whatsapp.send_text(message["from"], f"You said: {message['body']}")

    return {"status": "ok"}
```

Set the webhook URL and secret for your instance in the dashboard. See [WhatsApp webhooks](https://docs.hypersender.com/v2/api-reference/whatsapp-webhooks/whatsapp-webhooks-introduction) for every event.

## Send SMS with Python

Hypersender sends SMS through your own Android phone with the Hypersender SMS app.

```python
hs.sms.send_message("+201234567890", "Your order has shipped!")

# List delivered messages
hs.sms.list_messages(filters={"status": "delivered"}, per_page=20)
```

## OTP verification

Send a one-time code over WhatsApp or SMS and check it:

```python
hs.otp.request_code("201234567890@c.us", length=6, name="My Shop")

result = hs.otp.validate_code("201234567890@c.us", "123456")
```

Or create a WhatsApp OTP link the user taps to verify:

```python
link = hs.otp.generate_link(
    "201234567890@c.us",
    name="My Shop",
    callback={"success": "https://myshop.com/verified", "failed": "https://myshop.com/failed"},
)
```

## Enterprise: manage WhatsApp instances

```python
instance = hs.enterprise.create_instance("+201234567890", "Support line")
hs.enterprise.list_instances(filters={"status": "WORKING"})
hs.enterprise.get_instance_health(instance["id"])
hs.enterprise.request_new_qr_code(instance["id"])
```

## Errors

Failed requests raise `HypersenderError` with the HTTP status and the API's response:

```python
from hypersender import HypersenderError

try:
    hs.whatsapp.send_text("201234567890@c.us", "Hi")
except HypersenderError as error:
    print(error.status_code, error.message, error.body)
```

## All methods

| Client | Methods |
| --- | --- |
| `hs.whatsapp` | `send_text`, `send_text_safe`, `send_link_custom_preview`, `send_file`, `send_image`, `send_video`, `send_voice`, `send_poll`, `send_contact_card`, `send_location`, `forward_message`, `react_to_message`, `star_message`, `delete_message`, `get_queued_request`, `send_seen`, `read_chat`, `start_typing`, `stop_typing` |
| `hs.whatsapp.contacts` | `check_contact_exists`, `get_all_contacts`, `get_contact`, `get_profile_picture`, `upsert_contact`, `get_all_known_lids`, `get_lids_count`, `get_phone_number_by_lid`, `get_lid_by_phone_number` |
| `hs.sms` | `send_message`, `list_messages`, `delete_message`, `list_message_threads`, `edit_message_thread`, `delete_message_thread`, `get_heartbeats` |
| `hs.otp` | `request_code`, `validate_code`, `generate_link` |
| `hs.enterprise` | `list_instances`, `create_instance`, `get_instance_health`, `request_new_qr_code`, `restart_instance` |

Every method has a docstring with its parameters, so your editor shows them as you type.

## Documentation

Full documentation: [docs.hypersender.com](https://docs.hypersender.com/v2/packages-and-sdks/python/installation). Also available for [Laravel](https://github.com/hypersender/hypersender-laravel) and [Node.js](https://github.com/hypersender/hypersender-node).

## License

MIT. See [LICENSE](LICENSE).
