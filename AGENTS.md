# AGENTS.md

## Cursor Cloud specific instructions

This is **pydub**, a Python library for audio manipulation (not a web service). There are no running servers or databases.

### Key commands

| Task | Command |
|------|---------|
| Tests | `python test/test.py` |
| Lint | `ruff check pydub/` |
| Install (dev) | `pip install -e ".[dev]"` |

### Architecture notes

- **No C audioop dependency**: The legacy stdlib `audioop` module (removed in Python 3.13) has been replaced with `pydub/pyaudioop.py`, a NumPy-based reimplementation. All audio operations (mul, add, bias, rms, ratecv, etc.) use vectorized NumPy array operations.
- **Build system**: `pyproject.toml` with hatchling backend (no setup.py).
- **Lint**: Uses `ruff` (configured in pyproject.toml). Must pass cleanly.

### System dependencies

- `ffmpeg` is required for non-WAV format support (pre-installed in the VM).
- `libopus-dev` is required for Opus codec tests (pre-installed in the VM).
- `numpy` is a runtime dependency (used by `pyaudioop.py` for all audio math).
- `scipy` is needed for `pydub.scipy_effects` (high/low pass filters).

### Project structure

- `pydub/` — main package (AudioSegment, effects, generators, silence detection, playback)
- `pydub/pyaudioop.py` — NumPy-based audioop replacement (core audio math)
- `test/test.py` — full test suite (unittest, 113 tests)
- `test/data/` — audio fixtures (WAV, MP3, OGG, MP4, FLAC, etc.)
- See `README.markdown` for usage docs and `API.markdown` for full API reference.
