from __future__ import annotations

from typing import Any

from ._base import Service, _filters


class Enterprise(Service):
    """Manage many WhatsApp instances on an Enterprise account: `hs.enterprise`.
    The instance ID is passed on each call instead of being set on the client."""

    def list_instances(self, *, filters: dict[str, Any] | None = None) -> Any:
        """List instances. Filter by uuid, name (partial), phone, or status
        (STOPPED, STARTING, WORKING, SCAN_QR_CODE, FAILED, PENDING)."""
        return self._request("GET", "/instances", params=_filters(filters), per_instance=False)

    def create_instance(self, phone: str, name: str, *, webhook_url: str | None = None) -> Any:
        """Create an instance. `phone` is E.164 (+201234567890). The response has a QR code."""
        return self._request(
            "POST",
            "/create-instance",
            json={"phone": phone, "name": name, "webhook_url": webhook_url},
            per_instance=False,
        )

    def get_instance_health(self, instance_id: str) -> Any:
        """Check whether an instance is connected and working."""
        return self._request("GET", f"/{instance_id}/health", per_instance=False)

    def request_new_qr_code(self, instance_id: str) -> Any:
        """Get a fresh QR code to connect the phone."""
        return self._request("POST", f"/{instance_id}/request-new-qr-code", per_instance=False)

    def restart_instance(self, instance_id: str) -> Any:
        """Restart an instance."""
        return self._request("POST", f"/{instance_id}/restart", per_instance=False)
