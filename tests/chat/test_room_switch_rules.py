from chat.application.chat_controller import ChatController, ChatViewState
from chat.chat_app import ChatApp
from chat.entities.message import Message


class SessionDict(dict):
    def set(self, key, value):
        self[key] = value


class PageStub:
    def __init__(self):
        self.session = SessionDict()


class PubSubStub:
    def send_all(self, _message):
        return None


class AssistantStub:
    nome = "assistant"

    def process_message(self, _message):
        return None


def build_controller(chat_app: ChatApp, state: ChatViewState):
    page = PageStub()
    page.session.set("current_room", state.current_room)

    calls = {
        "room_titles": [],
        "clear_chat": 0,
        "close_drawer": 0,
        "update_page": 0,
    }

    controller = ChatController(
        page=page,
        chat_app=chat_app,
        pubsub=PubSubStub(),
        assistant_responder=AssistantStub(),
        state=state,
        refresh_users_drawer=lambda: None,
        append_chat_control=lambda _control: None,
        clear_chat_controls=lambda: calls.__setitem__("clear_chat", calls["clear_chat"] + 1),
        focus_message_input=lambda: None,
        update_room_title=lambda title: calls["room_titles"].append(title),
        close_drawer=lambda: calls.__setitem__("close_drawer", calls["close_drawer"] + 1),
        update_page=lambda: calls.__setitem__("update_page", calls["update_page"] + 1),
        create_chat_message=lambda message: message,
    )

    return controller, calls


def test_change_room_by_id_updates_state_and_session(monkeypatch):
    app = ChatApp()
    state = ChatViewState(user_name="Alice", user_id="alice", current_room="geral")
    controller, calls = build_controller(app, state)

    rendered_messages = []
    monkeypatch.setattr(controller, "on_message", lambda msg: rendered_messages.append(msg))

    controller.change_room_by_id("casual")

    assert controller.state.current_room == "casual"
    assert controller.page.session.get("current_room") == "casual"
    assert calls["room_titles"] == ["Bate-papo Casual"]
    assert calls["clear_chat"] == 1
    assert calls["close_drawer"] == 1
    assert calls["update_page"] == 1
    assert rendered_messages == []


def test_send_private_message_uses_existing_room_before_creating_new(monkeypatch):
    app = ChatApp()
    state = ChatViewState(user_name="Alice", user_id="alice", current_room="geral")
    controller, _ = build_controller(app, state)

    app.new_private_room(owner="Alice", reciver="bob", room_id="alicebob")

    changed_to = []
    monkeypatch.setattr(controller, "change_room_by_id", lambda room_id: changed_to.append(room_id))

    controller.send_private_message("bob")

    assert changed_to == ["alicebob"]


def test_send_private_message_accepts_reverse_existing_room_id(monkeypatch):
    app = ChatApp()
    state = ChatViewState(user_name="Alice", user_id="alice", current_room="geral")
    controller, _ = build_controller(app, state)

    app.new_private_room(owner="Bob", reciver="Alice", room_id="bobalice")

    changed_to = []
    monkeypatch.setattr(controller, "change_room_by_id", lambda room_id: changed_to.append(room_id))

    controller.send_private_message("bob")

    assert changed_to == ["bobalice"]


def test_send_private_message_creates_room_when_missing(monkeypatch):
    app = ChatApp()
    state = ChatViewState(user_name="Alice", user_id="alice", current_room="geral")
    controller, _ = build_controller(app, state)

    changed_to = []
    monkeypatch.setattr(controller, "change_room_by_id", lambda room_id: changed_to.append(room_id))

    controller.send_private_message("bob")

    assert "alicebob" in app.rooms
    assert changed_to == ["alicebob"]


def test_send_message_click_ignores_blank_message():
    app = ChatApp()
    state = ChatViewState(user_name="Alice", user_id="alice", current_room="geral")
    controller, _ = build_controller(app, state)

    sent = []
    controller.pubsub = type("Pub", (), {"send_all": lambda self, message: sent.append(message)})()

    message_input = type("Input", (), {"value": "   "})()
    controller.send_message_click(message_input)

    assert sent == []
    assert app.rooms["geral"].room.messages == []


def test_send_message_click_publishes_and_persists_message():
    app = ChatApp()
    state = ChatViewState(user_name="Alice", user_id="alice", current_room="geral")
    controller, _ = build_controller(app, state)

    sent = []
    focused = {"called": 0}
    updated = {"called": 0}
    controller.pubsub = type("Pub", (), {"send_all": lambda self, message: sent.append(message)})()
    controller.focus_message_input = lambda: focused.__setitem__("called", focused["called"] + 1)
    controller.update_page = lambda: updated.__setitem__("called", updated["called"] + 1)

    message_input = type("Input", (), {"value": "Olá"})()
    controller.send_message_click(message_input)

    assert len(sent) == 1
    assert sent[0].text == "Olá"
    assert app.rooms["geral"].room.messages[-1].text == "Olá"
    assert message_input.value == ""
    assert focused["called"] == 1
    assert updated["called"] == 1


def test_on_message_ignores_messages_from_other_room(monkeypatch):
    app = ChatApp()
    state = ChatViewState(user_name="Alice", user_id="alice", current_room="geral")
    controller, _ = build_controller(app, state)

    appended = []
    controller.append_chat_control = lambda control: appended.append(control)
    controller.update_page = lambda: appended.append("updated")
    controller.page.session.set("current_room", "geral")

    msg = Message(user_name="bob", text="oi", message_type="chat_message", room_id="casual")
    controller.on_message(msg)

    assert appended == []
