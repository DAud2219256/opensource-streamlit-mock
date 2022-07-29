import re

import streamlit_mock

import common


def test_simple_login():
    sm = streamlit_mock.StreamlitMock()
    session_state = sm.get_session_state()

    results = common.run(sm)
    assert re.search("test@example.com", results.markdown[1])
    assert re.search("Neptune User Manual", " ".join(results.markdown))
