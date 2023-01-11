import streamlit_mock


def test_add():
    sm = streamlit_mock.StreamlitMock()
    session_state = sm.get_session_state()
    session_state.x_input = 3
    session_state.y_input = 4

    sm.submit_form(form_key="calculator_form", button_label="Add")

    sm.run("main_form_calculator.py")

    results = sm.get_results()
    assert results.form == ["calculator_form"]
    assert results.write == ["3 + 4 = 7"]


def test_subtract():
    sm = streamlit_mock.StreamlitMock()
    session_state = sm.get_session_state()
    session_state.x_input = 3
    session_state.y_input = 4

    sm.submit_form(form_key="calculator_form", button_label="Subtract")

    sm.run("main_form_calculator.py")

    results = sm.get_results()
    assert results.form == ["calculator_form"]
    assert results.write == ["3 - 4 = -1"]
