from __future__ import annotations

from typing import Any

import httpx


class HypersenderError(Exception):
    """Raised when the API returns an error response (HTTP 4xx or 5xx)."""

    def __init__(self, message: str, status_code: int, body: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body

    def __str__(self) -> str:
        return f"[{self.status_code}] {self.message}"


def _clean(data: dict[str, Any] | None) -> dict[str, Any] | None:
    """Drop arguments the caller left as None so the API uses its defaults."""
    if data is None:
        return None
    return {key: value for key, value in data.items() if value is not None}


def _filters(filters: dict[str, Any] | None) -> dict[str, Any]:
    """{"status": "sent"} -> {"filter[status]": "sent"}"""
    return {f"filter[{key}]": value for key, value in (filters or {}).items()}


class Service:
    """One API product (WhatsApp, SMS, OTP, Enterprise) with its own base URL and key."""

    def __init__(
        self,
        http: httpx.Client,
        base_url: str,
        api_key: str | None,
        instance_id: str | None,
        product: str,
    ) -> None:
        self._http = http
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._instance_id = instance_id
        self._product = product

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        per_instance: bool = True,
    ) -> Any:
        if not self._api_key:
            raise ValueError(
                f"Missing API key: pass {self._product.lower()}_api_key= "
                f"or set HYPERSENDER_{self._product}_API_KEY."
            )
        if per_instance:
            if not self._instance_id:
                raise ValueError(
                    f"Missing instance ID: pass {self._product.lower()}_instance_id= "
                    f"or set HYPERSENDER_{self._product}_INSTANCE_ID."
                )
            path = f"/{self._instance_id}{path}"

        response = self._http.request(
            method,
            self._base_url + path,
            json=_clean(json),
            params=_clean(params),
            data=_clean(data),
            files=files,
            headers={"Authorization": f"Bearer {self._api_key}", "Accept": "application/json"},
        )
        return _parse(response)


def _parse(response: httpx.Response) -> Any:
    try:
        body = response.json() if response.content else None
    except ValueError:
        body = response.text

    if response.is_error:
        message = body.get("message") if isinstance(body, dict) else None
        raise HypersenderError(
            message or f"HTTP {response.status_code}", response.status_code, body
        )
    return body
