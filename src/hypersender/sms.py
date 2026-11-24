from __future__ import annotations

from typing import Any

from ._base import Service, _filters


class SMS(Service):
    """SMS messaging through your Android phone: `hs.sms`."""

    def send_message(
        self,
        to: str,
        content: str,
        *,
        request_id: str | None = None,
        schedule_send_at: str | None = None,
        max_send_attempts: int | None = None,
        message_expiration_seconds: int | None = None,
    ) -> Any:
        """Send an SMS. `schedule_send_at` is an ISO 8601 datetime to send later."""
        return self._request(
            "POST",
            "/send-message",
            json={
                "to": to,
                "content": content,
                "request_id": request_id,
                "schedule_send_at": schedule_send_at,
                "max_send_attempts": max_send_attempts,
                "message_expiration_seconds": message_expiration_seconds,
            },
        )

    def list_messages(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: str | None = None,
        include: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Any:
        """List messages. `filters={"status": "delivered"}` becomes `filter[status]=delivered`."""
        return self._request(
            "GET",
            "/messages",
            params={
                **_filters(filters),
                "sort": sort,
                "include": include,
                "page": page,
                "per_page": per_page,
            },
        )

    def delete_message(self, message_id: str) -> Any:
        """Delete a message."""
        return self._request("DELETE", "/delete-message", params={"messageId": message_id})

    def list_message_threads(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: str | None = None,
        include: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Any:
        """List conversations (message threads)."""
        return self._request(
            "GET",
            "/message-threads",
            params={
                **_filters(filters),
                "sort": sort,
                "include": include,
                "page": page,
                "per_page": per_page,
            },
        )

    def edit_message_thread(self, message_thread_id: str, *, is_archived: bool) -> Any:
        """Archive or unarchive a conversation."""
        return self._request(
            "PUT",
            "/edit-message-thread",
            json={"messageThreadId": message_thread_id, "is_archived": is_archived},
        )

    def delete_message_thread(self, message_thread_id: str) -> Any:
        """Delete a conversation."""
        return self._request(
            "DELETE", "/delete-message-thread", params={"messageThreadId": message_thread_id}
        )

    def get_heartbeats(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: str | None = None,
        include: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Any:
        """List the phone's heartbeats (app version, battery, charging) to check it is online."""
        return self._request(
            "GET",
            "/heartbeats",
            params={
                **_filters(filters),
                "sort": sort,
                "include": include,
                "page": page,
                "per_page": per_page,
            },
        )
