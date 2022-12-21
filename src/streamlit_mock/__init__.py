import importlib
import io
import pathlib
import sys
from typing import Union

import impl.utils
import streamlit as st

sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()))

imported = {}


class UploadedFile(io.BytesIO):
    def __init__(self, upload_filename, test_filename):
        path = pathlib.Path(test_filename).parent.resolve() / pathlib.Path(upload_filename)
        self.name = str(path)
        with open(path, mode="rb") as f:
            content = f.read()
        super(UploadedFile, self).__init__(content)
        pass


class StreamlitMock:
    def __init__(self):
        importlib.reload(st)
        self.session_state = st.session_state
        self.results = st._mock._results

    def get_session_state(self):
        return self.session_state

    def run(self, python_main: Union[str, pathlib.Path], args=[]) -> dict:
        if isinstance(python_main, str):
            python_main = pathlib.Path(python_main)
        sys.argv = [python_main.name] + args
        module_name = ".".join(python_main.parts[:-1] + (python_main.stem,))
        global imported
        while True:
            try:
                if module_name in imported:
                    importlib.reload(imported[module_name])
                else:
                    imported[module_name] = importlib.import_module(module_name)
                break
            except impl.utils.StreamlitStopException:
                break
            except impl.utils.StreamlitRerunException:
                continue

        return self.results

    def get_results(self) -> dict:
        return self.results

    def set_uploaded_file(self, key, upload_filename, test_filename):
        self.session_state[key] = UploadedFile(upload_filename, test_filename="./test.py")
