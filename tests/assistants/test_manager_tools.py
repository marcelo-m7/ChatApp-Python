from assistants.utils.manager_tools import ManagerTools


def test_debugger_exception_decorator_returns_result_on_success():
    wrapped = ManagerTools.debugger_exception_decorator(lambda x: x + 1)

    assert wrapped(1) == 2


def test_debugger_exception_decorator_swallows_exception(capsys):
    def boom():
        raise RuntimeError("fail")

    wrapped = ManagerTools.debugger_exception_decorator(boom)

    assert wrapped() is None
    captured = capsys.readouterr()
    assert "boom Error: fail" in captured.out
