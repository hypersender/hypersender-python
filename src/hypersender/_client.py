from __future__ import annotations

import os
from typing import Any

import httpx

from . import __version__
from .enterprise import Enterprise
from .otp import OTP
from .sms import SMS
from .whatsapp import WhatsApp

BASE_URL = "https://app.hypersender.com/api"


class Hypersender:
    """Hypersender API client.

    Credentials come from the arguments, or from the same environment variables
    the Laravel and Node.js SDKs use::

        HYPERSENDER_WHATSAPP_API_KEY, HYPERSENDER_WHATSAPP_INSTANCE_ID
        HYPERSENDER_SMS_API_KEY,      HYPERSENDER_SMS_INSTANCE_ID
        HYPERSENDER_OTP_API_KEY,      HYPERSENDER_OTP_INSTANCE_ID
        HYPERSENDER_ENTERPRISE_API_KEY

    Example::

        from hypersender import Hypersender

        hs = Hypersender()
        hs.whatsapp.send_text("201234567890@c.us", "Hello from Python")
    """

    def __init__(
        self,
        *,
        whatsapp_api_key: str | None = None,
        whatsapp_instance_id: str | None = None,
        sms_api_key: str | None = None,
        sms_instance_id: str | None = None,
        otp_api_key: str | None = None,
        otp_instance_id: str | None = None,
        enterprise_api_key: str | None = None,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._http = http_client or httpx.Client(
            timeout=timeout, headers={"User-Agent": f"hypersender-python/{__version__}"}
        )
        base_url = base_url.rstrip("/")

        def env(name: str, value: str | None) -> str | None:
            return value if value is not None else os.environ.get(f"HYPERSENDER_{name}")

        self.whatsapp = WhatsApp(
            self._http,
            f"{base_url}/whatsapp/v2",
            env("WHATSAPP_API_KEY", whatsapp_api_key),
            env("WHATSAPP_INSTANCE_ID", whatsapp_instance_id),
            "WHATSAPP",
        )
        self.sms = SMS(
            self._http,
            f"{base_url}/sms/v1",
            env("SMS_API_KEY", sms_api_key),
            env("SMS_INSTANCE_ID", sms_instance_id),
            "SMS",
        )
        self.otp = OTP(
            self._http,
            f"{base_url}/otp/v2",
            env("OTP_API_KEY", otp_api_key),
            env("OTP_INSTANCE_ID", otp_instance_id),
            "OTP",
        )
        self.enterprise = Enterprise(
            self._http,
            f"{base_url}/whatsapp/v2",
            env("ENTERPRISE_API_KEY", enterprise_api_key),
            None,
            "ENTERPRISE",
        )

    def close(self) -> None:
        """Close the underlying HTTP connections."""
        self._http.close()

    def __enter__(self) -> Hypersender:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
