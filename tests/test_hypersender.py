import json

import httpx
import pytest

from hypersender import Hypersender, HypersenderError

API = "https://app.hypersender.com/api"
WA = f"{API}/whatsapp/v2/wa-instance"
SMS = f"{API}/sms/v1/sms-instance"
OTP = f"{API}/otp/v2/otp-instance"
ENT = f"{API}/whatsapp/v2"


@pytest.fixture
def sent():
    return []


@pytest.fixture
def hs(sent):
    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(200, json={"ok": True})

    return Hypersender(
        whatsapp_api_key="wa-key",
        whatsapp_instance_id="wa-instance",
        sms_api_key="sms-key",
        sms_instance_id="sms-instance",
        otp_api_key="otp-key",
        otp_instance_id="otp-instance",
        enterprise_api_key="ent-key",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def body(request):
    return json.loads(request.content) if request.content else None


# (call, HTTP method, URL with query string, JSON body)
CASES = [
    # WhatsApp: sending
    (
        lambda hs: hs.whatsapp.send_text("1@c.us", "Hi"),
        "POST",
        f"{WA}/send-text",
        {"chatId": "1@c.us", "text": "Hi"},
    ),
    (
        lambda hs: hs.whatsapp.send_text("1@c.us", "Hi", reply_to="m1", link_preview=True),
        "POST",
        f"{WA}/send-text",
        {"chatId": "1@c.us", "text": "Hi", "reply_to": "m1", "link_preview": True},
    ),
    (
        lambda hs: hs.whatsapp.send_text_safe("1@c.us", "Hi"),
        "POST",
        f"{WA}/send-text-safe",
        {"chatId": "1@c.us", "text": "Hi"},
    ),
    (
        lambda hs: hs.whatsapp.send_link_custom_preview(
            "1@c.us",
            "Look",
            preview_title="T",
            preview_description="D",
            preview_url="https://x.com",
            preview_image_url="https://x.com/i.png",
        ),
        "POST",
        f"{WA}/send-link-custom-preview",
        {
            "chatId": "1@c.us",
            "text": "Look",
            "preview_title": "T",
            "preview_description": "D",
            "preview_url": "https://x.com",
            "preview_image_url": "https://x.com/i.png",
        },
    ),
    (
        lambda hs: hs.whatsapp.send_file("1@c.us", url="https://x.com/a.pdf", caption="Doc"),
        "POST",
        f"{WA}/send-file",
        {"chatId": "1@c.us", "url": "https://x.com/a.pdf", "caption": "Doc"},
    ),
    (
        lambda hs: hs.whatsapp.send_image("1@c.us", url="https://x.com/a.png"),
        "POST",
        f"{WA}/send-image",
        {"chatId": "1@c.us", "url": "https://x.com/a.png"},
    ),
    (
        lambda hs: hs.whatsapp.send_video("1@c.us", url="https://x.com/a.mp4"),
        "POST",
        f"{WA}/send-video",
        {"chatId": "1@c.us", "url": "https://x.com/a.mp4"},
    ),
    (
        lambda hs: hs.whatsapp.send_voice("1@c.us", url="https://x.com/a.ogg"),
        "POST",
        f"{WA}/send-voice",
        {"chatId": "1@c.us", "url": "https://x.com/a.ogg"},
    ),
    (
        lambda hs: hs.whatsapp.send_poll("1@c.us", "Lunch?", ["Yes", "No"]),
        "POST",
        f"{WA}/send-poll",
        {
            "chatId": "1@c.us",
            "poll": {"name": "Lunch?", "options": ["Yes", "No"], "multipleAnswers": False},
        },
    ),
    (
        lambda hs: hs.whatsapp.send_contact_card("1@c.us", [{"fullName": "A", "phoneNumber": "2"}]),
        "POST",
        f"{WA}/send-contact-card",
        {"chatId": "1@c.us", "contacts": [{"fullName": "A", "phoneNumber": "2"}]},
    ),
    (
        lambda hs: hs.whatsapp.send_location("1@c.us", 30.0, 31.2, title="Cairo"),
        "POST",
        f"{WA}/send-location",
        {"chatId": "1@c.us", "latitude": 30.0, "longitude": 31.2, "title": "Cairo"},
    ),
    (
        lambda hs: hs.whatsapp.forward_message("1@c.us", "m1"),
        "POST",
        f"{WA}/forward-message",
        {"chatId": "1@c.us", "messageId": "m1"},
    ),
    # WhatsApp: messages and chats
    (
        lambda hs: hs.whatsapp.react_to_message("1@c.us", "m1", "👍"),
        "PUT",
        f"{WA}/react-to-message",
        {"chatId": "1@c.us", "messageId": "m1", "reaction": "👍"},
    ),
    (
        lambda hs: hs.whatsapp.star_message("1@c.us", "m1"),
        "PUT",
        f"{WA}/star-message",
        {"chatId": "1@c.us", "messageId": "m1", "star": True},
    ),
    (
        lambda hs: hs.whatsapp.delete_message("1@c.us", "m1"),
        "DELETE",
        f"{WA}/delete-message?chatId=1%40c.us&messageId=m1",
        None,
    ),
    (lambda hs: hs.whatsapp.get_queued_request("q-1"), "GET", f"{WA}/queued-requests/q-1", None),
    (
        lambda hs: hs.whatsapp.send_seen("1@c.us", "m1"),
        "POST",
        f"{WA}/send-seen",
        {"chatId": "1@c.us", "messageId": "m1"},
    ),
    (
        lambda hs: hs.whatsapp.read_chat("1@c.us", days=7),
        "POST",
        f"{WA}/read-chat?days=7",
        {"chatId": "1@c.us"},
    ),
    (
        lambda hs: hs.whatsapp.start_typing("1@c.us"),
        "POST",
        f"{WA}/start-typing",
        {"chatId": "1@c.us"},
    ),
    (
        lambda hs: hs.whatsapp.stop_typing("1@c.us"),
        "POST",
        f"{WA}/stop-typing",
        {"chatId": "1@c.us"},
    ),
    # WhatsApp: contacts
    (
        lambda hs: hs.whatsapp.contacts.check_contact_exists("201234567890"),
        "POST",
        f"{WA}/contacts/check-exists",
        {"phone": "201234567890"},
    ),
    (
        lambda hs: hs.whatsapp.contacts.get_all_contacts(limit=50, sort_by="name"),
        "GET",
        f"{WA}/contacts/get-all?limit=50&sort_by=name",
        None,
    ),
    (
        lambda hs: hs.whatsapp.contacts.get_contact("1@lid"),
        "GET",
        f"{WA}/contacts/get?chat_id=1%40lid",
        None,
    ),
    (
        lambda hs: hs.whatsapp.contacts.get_profile_picture("1@c.us"),
        "GET",
        f"{WA}/contacts/profile-picture?chat_id=1%40c.us",
        None,
    ),
    (
        lambda hs: hs.whatsapp.contacts.upsert_contact("1@c.us", "John"),
        "POST",
        f"{WA}/contacts/upsert",
        {"chat_id": "1@c.us", "first_name": "John"},
    ),
    (
        lambda hs: hs.whatsapp.contacts.get_all_known_lids(limit=10),
        "GET",
        f"{WA}/contacts/get-all-known-lids?limit=10",
        None,
    ),
    (
        lambda hs: hs.whatsapp.contacts.get_lids_count(),
        "GET",
        f"{WA}/contacts/get-lids-count",
        None,
    ),
    (
        lambda hs: hs.whatsapp.contacts.get_phone_number_by_lid("1@lid"),
        "GET",
        f"{WA}/contacts/get-phone-number-by-lid?lid=1%40lid",
        None,
    ),
    (
        lambda hs: hs.whatsapp.contacts.get_lid_by_phone_number("3@c.us"),
        "GET",
        f"{WA}/contacts/get-lid-by-phone-number?phoneNumber=3%40c.us",
        None,
    ),
    # SMS
    (
        lambda hs: hs.sms.send_message("+201234567890", "Hi", max_send_attempts=3),
        "POST",
        f"{SMS}/send-message",
        {"to": "+201234567890", "content": "Hi", "max_send_attempts": 3},
    ),
    (
        lambda hs: hs.sms.list_messages(filters={"status": "delivered"}, per_page=20),
        "GET",
        f"{SMS}/messages?filter%5Bstatus%5D=delivered&per_page=20",
        None,
    ),
    (lambda hs: hs.sms.delete_message("m1"), "DELETE", f"{SMS}/delete-message?messageId=m1", None),
    (lambda hs: hs.sms.list_message_threads(), "GET", f"{SMS}/message-threads", None),
    (
        lambda hs: hs.sms.edit_message_thread("t1", is_archived=True),
        "PUT",
        f"{SMS}/edit-message-thread",
        {"messageThreadId": "t1", "is_archived": True},
    ),
    (
        lambda hs: hs.sms.delete_message_thread("t1"),
        "DELETE",
        f"{SMS}/delete-message-thread?messageThreadId=t1",
        None,
    ),
    (
        lambda hs: hs.sms.get_heartbeats(sort="-created_at"),
        "GET",
        f"{SMS}/heartbeats?sort=-created_at",
        None,
    ),
    # OTP
    (
        lambda hs: hs.otp.request_code("1@c.us", length=6, use_number=True, name="Shop"),
        "POST",
        f"{OTP}/request-code",
        {"chatId": "1@c.us", "length": 6, "useNumber": True, "name": "Shop"},
    ),
    (
        lambda hs: hs.otp.validate_code("1@c.us", "123456"),
        "POST",
        f"{OTP}/validate-code",
        {"chatId": "1@c.us", "code": "123456"},
    ),
    (
        lambda hs: hs.otp.generate_link("1@c.us", expires=600, callback={"success": "https://x"}),
        "POST",
        f"{OTP}/generate-link",
        {"chatId": "1@c.us", "expires": 600, "callback": {"success": "https://x"}},
    ),
    # Enterprise
    (
        lambda hs: hs.enterprise.list_instances(filters={"status": "WORKING"}),
        "GET",
        f"{ENT}/instances?filter%5Bstatus%5D=WORKING",
        None,
    ),
    (
        lambda hs: hs.enterprise.create_instance("+201234567890", "Support"),
        "POST",
        f"{ENT}/create-instance",
        {"phone": "+201234567890", "name": "Support"},
    ),
    (lambda hs: hs.enterprise.get_instance_health("i-1"), "GET", f"{ENT}/i-1/health", None),
    (
        lambda hs: hs.enterprise.request_new_qr_code("i-1"),
        "POST",
        f"{ENT}/i-1/request-new-qr-code",
        None,
    ),
    (lambda hs: hs.enterprise.restart_instance("i-1"), "POST", f"{ENT}/i-1/restart", None),
]


@pytest.mark.parametrize("call, method, url, expected_body", CASES)
def test_requests(hs, sent, call, method, url, expected_body):
    assert call(hs) == {"ok": True}
    (request,) = sent
    assert request.method == method
    assert str(request.url) == url
    assert body(request) == expected_body


@pytest.mark.parametrize(
    "call, key",
    [
        (lambda hs: hs.whatsapp.send_text("1@c.us", "Hi"), "wa-key"),
        (lambda hs: hs.whatsapp.contacts.get_lids_count(), "wa-key"),
        (lambda hs: hs.sms.list_message_threads(), "sms-key"),
        (lambda hs: hs.otp.validate_code("1@c.us", "1"), "otp-key"),
        (lambda hs: hs.enterprise.list_instances(), "ent-key"),
    ],
)
def test_each_product_sends_its_own_key(hs, sent, call, key):
    call(hs)
    assert sent[0].headers["Authorization"] == f"Bearer {key}"


def test_upload_from_bytes_is_multipart(hs, sent):
    hs.whatsapp.send_image("1@c.us", file=b"\x89PNG", filename="logo.png", caption="Logo")
    request = sent[0]
    assert request.headers["Content-Type"].startswith("multipart/form-data")
    content = request.content
    assert b'name="chatId"' in content and b"1@c.us" in content
    assert b'name="caption"' in content
    assert b'name="file"; filename="logo.png"' in content
    assert b"\x89PNG" in content


def test_upload_from_path(hs, sent, tmp_path):
    path = tmp_path / "invoice.pdf"
    path.write_bytes(b"%PDF")
    hs.whatsapp.send_file("1@c.us", file=path)
    assert b'filename="invoice.pdf"' in sent[0].content


def test_multipart_booleans_are_sent_as_1_or_0(hs, sent):
    hs.whatsapp.send_link_custom_preview(
        "1@c.us",
        "Look",
        preview_title="T",
        preview_description="D",
        preview_url="https://x.com",
        preview_image_file=b"img",
        high_quality=True,
    )
    assert b'name="high_quality"\r\n\r\n1\r\n' in sent[0].content
    assert b'name="preview_image_file"' in sent[0].content


def test_media_needs_exactly_one_of_url_or_file(hs):
    with pytest.raises(ValueError, match="exactly one"):
        hs.whatsapp.send_image("1@c.us")
    with pytest.raises(ValueError, match="exactly one"):
        hs.whatsapp.send_image("1@c.us", url="https://x", file=b"x")


def test_api_errors_raise_with_status_and_body():
    client = httpx.Client(
        transport=httpx.MockTransport(
            lambda r: httpx.Response(422, json={"message": "The chat id field is required."})
        )
    )
    hs = Hypersender(whatsapp_api_key="k", whatsapp_instance_id="i", http_client=client)
    with pytest.raises(HypersenderError) as error:
        hs.whatsapp.send_text("", "Hi")
    assert error.value.status_code == 422
    assert error.value.message == "The chat id field is required."
    assert error.value.body == {"message": "The chat id field is required."}
    assert str(error.value) == "[422] The chat id field is required."


def test_error_without_json_body():
    client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(502, text="Bad")))
    hs = Hypersender(whatsapp_api_key="k", whatsapp_instance_id="i", http_client=client)
    with pytest.raises(HypersenderError, match=r"\[502\] HTTP 502"):
        hs.whatsapp.send_text("1@c.us", "Hi")


def test_reads_credentials_from_environment(monkeypatch, sent):
    monkeypatch.setenv("HYPERSENDER_WHATSAPP_API_KEY", "env-key")
    monkeypatch.setenv("HYPERSENDER_WHATSAPP_INSTANCE_ID", "env-instance")

    def handler(request):
        sent.append(request)
        return httpx.Response(200, json={})

    hs = Hypersender(http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    hs.whatsapp.send_text("1@c.us", "Hi")
    assert str(sent[0].url) == f"{API}/whatsapp/v2/env-instance/send-text"
    assert sent[0].headers["Authorization"] == "Bearer env-key"


def test_missing_credentials_say_which_env_var(monkeypatch):
    monkeypatch.delenv("HYPERSENDER_SMS_API_KEY", raising=False)
    monkeypatch.delenv("HYPERSENDER_SMS_INSTANCE_ID", raising=False)
    with pytest.raises(ValueError, match="HYPERSENDER_SMS_API_KEY"):
        Hypersender().sms.send_message("+1", "Hi")
    with pytest.raises(ValueError, match="HYPERSENDER_SMS_INSTANCE_ID"):
        Hypersender(sms_api_key="k").sms.send_message("+1", "Hi")


def test_empty_response_returns_none():
    client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(204)))
    hs = Hypersender(whatsapp_api_key="k", whatsapp_instance_id="i", http_client=client)
    assert hs.whatsapp.start_typing("1@c.us") is None


def test_default_client_sets_user_agent_and_closes():
    from hypersender import __version__

    with Hypersender() as hs:
        assert hs._http.headers["User-Agent"] == f"hypersender-python/{__version__}"
    assert hs._http.is_closed
