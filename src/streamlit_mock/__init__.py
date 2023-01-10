import importlib
import io
import sys
from pathlib import Path
from typing import Union

sys.path.insert(0, str(Path(__file__).parent.resolve()))

import impl.utils  # noqa: E402
import streamlit as st  # noqa: E402

imported = {}


class UploadedFile(io.BytesIO):
    def __init__(
        self,
        upload_filename: Path,
    ):
        self.name = upload_filename.name
        with open(upload_filename, mode="rb") as f:
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

    def run(self, python_main: Union[str, Path], args=[]) -> dict:
        if isinstance(python_main, str):
            python_main = Path(python_main)
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

    def set_uploaded_file(
        self,
        key: str,
        upload_filename: Union[Path, list[Path]],
    ):
        # TODO: type validation
        if isinstance(upload_filename, Path):
            self.session_state[key] = UploadedFile(upload_filename)
        elif isinstance(upload_filename, list):
            self.session_state[key] = [UploadedFile(file) for file in upload_filename]
