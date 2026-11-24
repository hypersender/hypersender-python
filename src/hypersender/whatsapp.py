from __future__ import annotations

import os
from pathlib import Path
from typing import IO, Any, Union

from ._base import Service

FileInput = Union[str, "os.PathLike[str]", bytes, IO[bytes]]


def _file(file: FileInput, filename: str | None) -> tuple[str, Any]:
    """A path, bytes, or open binary file -> an httpx multipart file tuple."""
    if isinstance(file, (str, os.PathLike)):
        path = Path(file)
        return (filename or path.name, path.read_bytes())
    return (filename or getattr(file, "name", "file"), file)


def _form(data: dict[str, Any]) -> dict[str, Any]:
    """Multipart fields must be strings; send booleans the way the API's validator expects."""
    return {k: ("1" if v else "0") if isinstance(v, bool) else v for k, v in data.items()}


class Contacts(Service):
    """WhatsApp contacts and LID lookups: `hs.whatsapp.contacts`."""

    def check_contact_exists(self, phone: str) -> Any:
        """Check if a phone number has WhatsApp. `phone` has the country code, no + or spaces."""
        return self._request("POST", "/contacts/check-exists", json={"phone": phone})

    def get_all_contacts(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> Any:
        """List contacts. `sort_by` is "id" or "name"; `sort_order` is "asc" or "desc"."""
        return self._request(
            "GET",
            "/contacts/get-all",
            params={"limit": limit, "offset": offset, "sort_by": sort_by, "sort_order": sort_order},
        )

    def get_contact(self, chat_id: str) -> Any:
        """Get a contact by phone number or chat ID (`123@c.us` or `123@lid`)."""
        return self._request("GET", "/contacts/get", params={"chat_id": chat_id})

    def get_profile_picture(self, chat_id: str) -> Any:
        """Get a contact's WhatsApp profile picture URL."""
        return self._request("GET", "/contacts/profile-picture", params={"chat_id": chat_id})

    def upsert_contact(self, chat_id: str, first_name: str, last_name: str | None = None) -> Any:
        """Create a contact, or update its name if it already exists."""
        return self._request(
            "POST",
            "/contacts/upsert",
            json={"chat_id": chat_id, "first_name": first_name, "last_name": last_name},
        )

    def get_all_known_lids(self, *, limit: int | None = None, offset: int | None = None) -> Any:
        """List the LID to phone number mappings the instance knows."""
        return self._request(
            "GET", "/contacts/get-all-known-lids", params={"limit": limit, "offset": offset}
        )

    def get_lids_count(self) -> Any:
        """Count the known LID mappings."""
        return self._request("GET", "/contacts/get-lids-count")

    def get_phone_number_by_lid(self, lid: str) -> Any:
        """Resolve a LID (`1111111@lid`) to its phone number chat ID."""
        return self._request("GET", "/contacts/get-phone-number-by-lid", params={"lid": lid})

    def get_lid_by_phone_number(self, phone_number: str) -> Any:
        """Find the LID linked to a phone number (`3333333@c.us` or `3333333`)."""
        return self._request(
            "GET", "/contacts/get-lid-by-phone-number", params={"phoneNumber": phone_number}
        )


class WhatsApp(Service):
    """WhatsApp messaging: `hs.whatsapp`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.contacts = Contacts(*args, **kwargs)

    # Sending messages

    def send_text(
        self,
        chat_id: str,
        text: str,
        *,
        reply_to: str | None = None,
        link_preview: bool | None = None,
        link_preview_high_quality: bool | None = None,
    ) -> Any:
        """Send a text message. `chat_id` looks like `201234567890@c.us`."""
        return self._request(
            "POST",
            "/send-text",
            json={
                "chatId": chat_id,
                "text": text,
                "reply_to": reply_to,
                "link_preview": link_preview,
                "link_preview_high_quality": link_preview_high_quality,
            },
        )

    def send_text_safe(
        self,
        chat_id: str,
        text: str,
        *,
        reply_to: str | None = None,
        link_preview: bool | None = None,
        link_preview_high_quality: bool | None = None,
    ) -> Any:
        """Send a text message with human-like pacing and typing to lower the risk of a block."""
        return self._request(
            "POST",
            "/send-text-safe",
            json={
                "chatId": chat_id,
                "text": text,
                "reply_to": reply_to,
                "link_preview": link_preview,
                "link_preview_high_quality": link_preview_high_quality,
            },
        )

    def send_link_custom_preview(
        self,
        chat_id: str,
        text: str,
        *,
        preview_title: str,
        preview_description: str,
        preview_url: str,
        preview_image_url: str | None = None,
        preview_image_file: FileInput | None = None,
        reply_to: str | None = None,
        high_quality: bool | None = None,
    ) -> Any:
        """Send a link with your own preview title, description, and image (URL or file)."""
        fields = {
            "chatId": chat_id,
            "text": text,
            "preview_title": preview_title,
            "preview_description": preview_description,
            "preview_url": preview_url,
            "preview_image_url": preview_image_url,
            "reply_to": reply_to,
            "high_quality": high_quality,
        }
        if preview_image_file is not None:
            return self._request(
                "POST",
                "/send-link-custom-preview",
                data=_form(fields),
                files={"preview_image_file": _file(preview_image_file, None)},
            )
        return self._request("POST", "/send-link-custom-preview", json=fields)

    def _send_media(
        self,
        path: str,
        chat_id: str,
        url: str | None,
        file: FileInput | None,
        **fields: Any,
    ) -> Any:
        if (url is None) == (file is None):
            raise ValueError("Pass exactly one of url= or file=.")
        fields = {"chatId": chat_id, **fields}
        if file is not None:
            upload = _file(file, fields.get("filename"))
            return self._request("POST", path, data=_form(fields), files={"file": upload})
        return self._request("POST", path, json={**fields, "url": url})

    def send_file(
        self,
        chat_id: str,
        *,
        url: str | None = None,
        file: FileInput | None = None,
        filename: str | None = None,
        mimetype: str | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> Any:
        """Send a document from a URL or a local file (path, bytes, or open binary file)."""
        return self._send_media(
            "/send-file",
            chat_id,
            url,
            file,
            filename=filename,
            mimetype=mimetype,
            caption=caption,
            reply_to=reply_to,
        )

    def send_image(
        self,
        chat_id: str,
        *,
        url: str | None = None,
        file: FileInput | None = None,
        filename: str | None = None,
        mimetype: str | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> Any:
        """Send an image from a URL or a local file."""
        return self._send_media(
            "/send-image",
            chat_id,
            url,
            file,
            filename=filename,
            mimetype=mimetype,
            caption=caption,
            reply_to=reply_to,
        )

    def send_video(
        self,
        chat_id: str,
        *,
        url: str | None = None,
        file: FileInput | None = None,
        filename: str | None = None,
        mimetype: str | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> Any:
        """Send a video from a URL or a local file."""
        return self._send_media(
            "/send-video",
            chat_id,
            url,
            file,
            filename=filename,
            mimetype=mimetype,
            caption=caption,
            reply_to=reply_to,
        )

    def send_voice(
        self,
        chat_id: str,
        *,
        url: str | None = None,
        file: FileInput | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> Any:
        """Send a voice note from a URL or a local file."""
        return self._send_media(
            "/send-voice", chat_id, url, file, caption=caption, reply_to=reply_to
        )

    def send_poll(
        self,
        chat_id: str,
        name: str,
        options: list[str],
        *,
        multiple_answers: bool = False,
        reply_to: str | None = None,
    ) -> Any:
        """Send a poll."""
        return self._request(
            "POST",
            "/send-poll",
            json={
                "chatId": chat_id,
                "reply_to": reply_to,
                "poll": {"name": name, "options": options, "multipleAnswers": multiple_answers},
            },
        )

    def send_contact_card(self, chat_id: str, contacts: list[dict[str, Any]]) -> Any:
        """Send contact cards. Each contact has fullName, phoneNumber, and optionally
        organization, whatsappId, or a raw vcard."""
        return self._request(
            "POST", "/send-contact-card", json={"chatId": chat_id, "contacts": contacts}
        )

    def send_location(
        self,
        chat_id: str,
        latitude: float,
        longitude: float,
        *,
        title: str | None = None,
        reply_to: str | None = None,
    ) -> Any:
        """Send a location pin."""
        return self._request(
            "POST",
            "/send-location",
            json={
                "chatId": chat_id,
                "latitude": latitude,
                "longitude": longitude,
                "title": title,
                "reply_to": reply_to,
            },
        )

    def forward_message(self, chat_id: str, message_id: str) -> Any:
        """Forward a message to a chat."""
        return self._request(
            "POST", "/forward-message", json={"chatId": chat_id, "messageId": message_id}
        )

    # Message management

    def react_to_message(self, chat_id: str, message_id: str, reaction: str) -> Any:
        """React to a message with an emoji."""
        return self._request(
            "PUT",
            "/react-to-message",
            json={"chatId": chat_id, "messageId": message_id, "reaction": reaction},
        )

    def star_message(self, chat_id: str, message_id: str, star: bool = True) -> Any:
        """Star or unstar a message."""
        return self._request(
            "PUT",
            "/star-message",
            json={"chatId": chat_id, "messageId": message_id, "star": star},
        )

    def delete_message(self, chat_id: str, message_id: str) -> Any:
        """Delete a message for everyone."""
        return self._request(
            "DELETE", "/delete-message", params={"chatId": chat_id, "messageId": message_id}
        )

    def get_queued_request(self, uuid: str) -> Any:
        """Get a request's status by the `queued_request_uuid` every send method returns."""
        return self._request("GET", f"/queued-requests/{uuid}")

    # Chat status

    def send_seen(self, chat_id: str, message_id: str, *, participant: str | None = None) -> Any:
        """Mark a message as seen (blue ticks)."""
        return self._request(
            "POST",
            "/send-seen",
            json={"chatId": chat_id, "messageId": message_id, "participant": participant},
        )

    def read_chat(
        self, chat_id: str, *, messages: int | None = None, days: int | None = None
    ) -> Any:
        """Mark a chat's recent messages as read."""
        return self._request(
            "POST",
            "/read-chat",
            json={"chatId": chat_id},
            params={"messages": messages, "days": days},
        )

    def start_typing(self, chat_id: str) -> Any:
        """Show "typing..." in a chat."""
        return self._request("POST", "/start-typing", json={"chatId": chat_id})

    def stop_typing(self, chat_id: str) -> Any:
        """Stop showing "typing..." in a chat."""
        return self._request("POST", "/stop-typing", json={"chatId": chat_id})
