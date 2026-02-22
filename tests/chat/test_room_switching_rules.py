from types import SimpleNamespace

from chat.application.chat_controller import ChatController, ChatViewState
from chat.chat_app import ChatApp


class SessionStub:
    def __init__(self):
        self.data = {"current_room": "geral"}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)


class PubSubStub:
    def send_all(self, _message):
        return None


class AssistantStub:
    nome = "bot"

    def process_message(self, _message):
        return None


def build_controller(chat_app: ChatApp):
    page = SimpleNamespace(session=SessionStub())
    state = ChatViewState(user_name="Ana", user_id="ana", current_room="geral")

    calls = {"title": [], "clear": 0, "close": 0, "update": 0}

    controller = ChatController(
        page=page,
        chat_app=chat_app,
        pubsub=PubSubStub(),
        assistant_responder=AssistantStub(),
        state=state,
        refresh_users_drawer=lambda: None,
        append_chat_control=lambda _control: None,
        clear_chat_controls=lambda: calls.__setitem__("clear", calls["clear"] + 1),
        focus_message_input=lambda: None,
        update_room_title=lambda title: calls["title"].append(title),
        close_drawer=lambda: calls.__setitem__("close", calls["close"] + 1),
        update_page=lambda: calls.__setitem__("update", calls["update"] + 1),
        create_chat_message=lambda message: message,
    )
    return controller, calls


def test_change_room_updates_session_and_state():
    app = ChatApp()
    controller, calls = build_controller(app)

    controller.change_room_by_id("casual")

    assert controller.page.session.get("current_room") == "casual"
    assert controller.state.current_room == "casual"
    assert calls["title"] == ["Bate-papo Casual"]
    assert calls["clear"] == 1
    assert calls["close"] == 1


def test_send_private_message_reuses_existing_private_room_in_reverse_order():
    app = ChatApp()
    app.new_private_room(owner="joao", reciver="ana", room_id="joaoana")
    controller, _ = build_controller(app)

    controller.send_private_message("Joao")

    assert controller.state.current_room == "joaoana"
    assert controller.page.session.get("current_room") == "joaoana"


def test_send_private_message_creates_new_private_room_when_missing():
    app = ChatApp()
    controller, _ = build_controller(app)

    controller.send_private_message("Joao")

    assert "anajoao" in app.rooms
    assert controller.state.current_room == "anajoao"
