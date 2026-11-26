"""Offline checks of the shared snippet runner."""
import os

import pytest

from snippets import __main__ as runner


@pytest.mark.parametrize("file_present, existing", [(False, None), (True, None), (True, "shell"), (True, "")])
def test_dotenv_loaded_before_snippet(tmp_path, monkeypatch, file_present, existing):
    key = "SNIPPET_TEST_ENV"
    monkeypatch.delenv(key, raising=False)
    if existing is not None:
        monkeypatch.setenv(key, existing)
    if file_present:
        (tmp_path / ".env").write_text(f"{key}=file\n")
    folder = tmp_path / "snippets" / "lecture_test" / "example1"
    folder.mkdir(parents=True)
    (folder / "probe.py").touch()
    monkeypatch.setattr(runner, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(runner, "SNIPPETS_ROOT", tmp_path / "snippets")
    monkeypatch.setattr(runner.sys, "argv", ["snippets", "-l", "test", "-e", "1"])
    observed = []
    monkeypatch.setattr(runner.runpy, "run_module", lambda *args, **kwargs: observed.append(os.getenv(key)))

    runner.main()

    assert observed == [existing if existing is not None else "file" if file_present else None]
