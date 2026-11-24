<p align="center"><img width="307" height="63" src="https://raw.githubusercontent.com/hypersender/hypersender-python/main/art/hy.svg" alt="Hypersender Logo"></p>

<p align="center">
<a href="https://pypi.org/project/hypersender/"><img src="https://img.shields.io/pypi/dm/hypersender" alt="Monthly Downloads"></a>
<a href="https://pypi.org/project/hypersender/"><img src="https://img.shields.io/pypi/v/hypersender" alt="Latest Stable Version"></a>
<a href="https://pypi.org/project/hypersender/"><img src="https://img.shields.io/pypi/pyversions/hypersender" alt="Python Versions"></a>
<a href="https://github.com/hypersender/hypersender-python/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" alt="License"></a>
</p>

# Introduction

The official Python SDK for the Hypersender WhatsApp API, SMS API, and OTP API. Send WhatsApp messages, build a Python WhatsApp bot, send SMS from your own Android phone, and verify users with one-time codes.

# Installation

You can install the package via pip (Python 3.10+):

```bash
pip install hypersender
```

```python
from hypersender import Hypersender

hs = Hypersender()  # reads HYPERSENDER_WHATSAPP_API_KEY and HYPERSENDER_WHATSAPP_INSTANCE_ID
hs.whatsapp.send_text("201234567890@c.us", "Hello from Python!")
```

# Official Documentation

You can find the official documentation at [Hypersender Python SDK Documentation](https://docs.hypersender.com/v2/packages-and-sdks/python/installation).

Building a WhatsApp bot in Python? Follow [Build a WhatsApp Bot in Python](https://docs.hypersender.com/v2/packages-and-sdks/python/whatsapp/whatsapp-bot) for a complete Flask and FastAPI example.

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) for details.

## Security Vulnerabilities

Please review [our security policy](../../security/policy) on how to report security vulnerabilities.

## Credits

-   [Hypersender](https://github.com/hypersender)
-   [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.
