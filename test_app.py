"""Streamlit AppTest smoke checks for Explore Majors."""
from streamlit.testing.v1 import AppTest


def test_explore_majors_renders_in_english_and_vietnamese():
    at = AppTest.from_file("app.py").run()
    assert not at.exception

    at.sidebar.radio[0].set_value("Explore Majors").run()
    assert not at.exception
    assert len(at.expander) >= 20

    at.sidebar.selectbox[0].set_value("Tiếng Việt").run()
    assert not at.exception
    at.sidebar.radio[0].set_value("Khám phá ngành học").run()
    assert not at.exception
    assert len(at.expander) >= 20
    assert at.title[0].value == "Khám phá ngành học"
