from __future__ import annotations

from typing import Any

from ._base import Service


class OTP(Service):
    """One-time passwords over WhatsApp or SMS: `hs.otp`."""

    def request_code(
        self,
        chat_id: str,
        *,
        length: int | None = None,
        use_number: bool | None = None,
        use_letter: bool | None = None,
        all_capital: bool | None = None,
        name: str | None = None,
        expires: int | None = None,
    ) -> Any:
        """Send a one-time code. `length` is 4-10; `expires` is seconds (60-1800);
        `name` is your app or company name shown in the message."""
        return self._request(
            "POST",
            "/request-code",
            json={
                "chatId": chat_id,
                "length": length,
                "useNumber": use_number,
                "useLetter": use_letter,
                "allCapital": all_capital,
                "name": name,
                "expires": expires,
            },
        )

    def validate_code(self, chat_id: str, code: str) -> Any:
        """Check a code the user entered."""
        return self._request("POST", "/validate-code", json={"chatId": chat_id, "code": code})

    def generate_link(
        self,
        chat_id: str,
        *,
        expires: int | None = None,
        name: str | None = None,
        message: dict[str, str] | None = None,
        callback: dict[str, str] | None = None,
    ) -> Any:
        """Create a WhatsApp OTP link the user opens to verify.
        `message` keys: prompt, success, failed, expired. `callback` keys: success, failed."""
        return self._request(
            "POST",
            "/generate-link",
            json={
                "chatId": chat_id,
                "expires": expires,
                "name": name,
                "message": message,
                "callback": callback,
            },
        )
