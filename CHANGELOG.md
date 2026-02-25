# Changelog

## v0.26.0 — Modernized Fork

> This release marks the beginning of the [HGFantasy/pydub](https://github.com/HGFantasy/pydub)
> fork, based on [jiaaro/pydub](https://github.com/jiaaro/pydub) v0.25.1.

### Breaking changes
- **Python 2 support removed.** Minimum version is now Python 3.9.
- **NumPy is now a required dependency.** The deprecated C `audioop` module
  (removed in Python 3.13) has been replaced with a vectorized NumPy
  implementation in `pydub/pyaudioop.py`.

### New
- `pyproject.toml` with hatchling build backend (replaces `setup.py`/`setup.cfg`)
- `ruff` linter configuration (replaces `pylama`)
- Optional dependency groups: `pip install pydub[playback]`, `pip install pydub[scipy]`, `pip install pydub[dev]`

### Fixed
- `scipy_effects.py`: added missing `AudioSegment` import
- `scipy_effects.py`: fixed misspelled `from_mono_audio_segements` → `from_mono_audiosegments` (4 call sites)
- `test/test.py`: fixed `assertEquals` → `assertEqual` for Python 3.12+ compatibility

### Removed
- All Python 2 compatibility code (~200 lines): `from __future__`, `basestring`/`xrange`/`izip` shims, `StringIO` fallbacks, `tostring()` calls
- `setup.py`, `setup.cfg`, `MANIFEST.in`
- Dead CI configs: `.travis.yml`, `appveyor.yml`

### Modernized
- `class Foo(object)` → `class Foo`
- `super(Cls, self)` → `super()`
- Bare `except:` → `except Exception:`
- `.format()` → f-strings
- All imports sorted with `isort` (via ruff)

---

*Upstream changelog for the original jiaaro/pydub project follows below.*

---

# v0.25.1
- Fix crashing bug in new scipy-powered EQ effects

# v0.25.0
- Don't show a runtime warning about the optional ffplay dependency being missing until someone tries to use it
- Documentation improvements
- Python 3.9 support
- Improved efficiency of loading wave files with `pydub.AudioSegment.from_file()`
- Ensure `pydub.AudioSegment().export()` always returns files with a seek position at the beginning of the file
- Added more EQ effects to `pydub.scipy_effects` (requires scipy to be installed)
- Fix a packaging bug where the LICENSE file was not included in the source distribution
- Add a way to instantiate a `pydub.AudioSegment()` with a portion of an audio file via `pydub.AudioSegment().from_file()`

# v0.24.1
- Fix bug where ffmpeg errors in Python 3 are illegible
- Fix bug where `split_on_silence` fails when there are one or fewer nonsilent segments
- Fix bug in fallback audioop implementation

# v0.24.0
- Fix inconsistent handling of 8-bit audio
- Fix bug where certain files will fail to parse
- Fix bug where pyaudio stream is not closed on error
- Allow codecs and parameters in wav and raw export
- Fix bug in `pydub.AudioSegment.from_file` where supplied codec is ignored
- Allow `pydub.silence.split_on_silence` to take a boolean for `keep_silence`
- Fix bug where `pydub.silence.split_on_silence` sometimes adds non-silence from adjacent segments
- Fix bug where `pydub.AudioSegment.extract_wav_headers` fails on empty wav files
- Add new function `pydub.silence.detect_leading_silence`
- Support conversion between an arbitrary number of channels and mono in `pydub.AudioSegment.set_channels`
- Fix several issues related to reading from filelike objects

# v0.23.1
- Fix bug in passing ffmpeg/avconv parameters for `pydub.AudioSegment.from_mp3()`, `pydub.AudioSegment.from_flv()`, `pydub.AudioSegment.from_ogg()`, and `pydub.AudioSegment.from_wav()`
- Fix logic bug in `pydub.effects.strip_silence()`

# v0.23.0
- Add support for playback via simpleaudio
- Allow users to override the type in `pydub.AudioSegment().get_array_of_samples()` (PR #313)
- Fix a bug where the wrong codec was used for 8-bit audio (PR #309 - issue #308)

# v0.22.1
- Fix `pydub.utils.mediainfo_json()` to work with newer, backwards-incompatible versions of ffprobe/avprobe

# v0.22.0
- Adds support for audio with frame rates (sample rates) of 48k and higher (requires scipy) (PR #262, fixes #134, #237, #209)
- Adds support for PEP 519 File Path protocol (PR #252)
- Fixes a few places where handles to temporary files are kept open (PR #280)
- Add the license file to the python package to aid other packaging projects (PR #279, fixes #274)
- Bug fix for `pydub.silence.detect_silence()` (PR #263)

# v0.21.0
- NOTE: Semi-counterintuitive change: using a stride when slicing AudioSegment instances (for example, `sound[::5000]`) will return chunks of 5000ms (not 1ms chunks every 5000ms) (#222)
- Debug output from ffmpeg/avlib is no longer printed to the console unless you set up logging (#223)
- All pydub exceptions are now subclasses of `pydub.exceptions.PydubException` (PR #244)
- The utilities in `pydub.silence` now accept a `seek_step` argument which can optionally be passed to improve the performance of silence detection (#211)
- Fix to `pydub.silence` utilities which allow you to detect perfect silence (#233)
- Fix a bug where threaded code screws up your terminal session due to ffmpeg inheriting the stdin from the parent process (#231)
- Fix a bug where crashing programs using pydub would leave behind their temporary files (#206)

# v0.20.0
- Add new parameter `gain_during_overlay` to `pydub.AudioSegment.overlay`
- `pydub.playback.play()` No longer displays the verbose playback "banner" when using ffplay
- Fix a confusing error message when using invalid crossfade durations (issue #193)

# v0.19.0
- Allow codec and ffmpeg/avconv parameters to be set in `pydub.AudioSegment.from_file()`
- Allow `AudioSegment` objects with more than two channels to be split using `pydub.AudioSegment().split_to_mono()`
- Add support for inverting the phase of only one channel in a multi-channel `pydub.AudioSegment` object
- Fix a bug with the latest avprobe that broke `pydub.utils.mediainfo()`
- Add tests for webm encoding/decoding

# v0.18.0
- Add `pydub.AudioSegment.from_mono_audiosegments()` constructor
- Refactor `pydub.AudioSegment._sync()` to support an arbitrary number of audiosegment arguments

# v0.17.0
- Add cover image support for MP3 exports via `cover` keyword argument
- Add `pydub.AudioSegment().get_dc_offset()` and `pydub.AudioSegment().remove_dc_offset()`
- Minor fixes for Windows users

# v0.16.7
- Make `pydub.AudioSegment()._spawn()` accept `array.array` instances

# v0.16.6
- Inline playback in IPython notebooks
- Add scipy-powered high/low/band pass filters
- Fix minor bug in `pydub.silence.detect_silence()`

# v0.16.5
- Allow user subclassing of `pydub.AudioSegment`
- Workaround for incorrect duration reporting of some mp3 files on macOS

# v0.16.4
- Add `sum()` support for iterables of AudioSegments
- Fix bug in 24-bit wav support

# v0.16.3
- Add Python 3.5 support
- Add native 24-bit wav file support

# v0.16.2
- Fix bug with direct `bytes` instantiation in Python 3

# v0.16.1
- Search current directory for ffmpeg/avconv before system PATH

# v0.16.0
- Easier direct `AudioSegment` instantiation from raw audio data
- Add `get_array_of_samples()` and `raw_data` property
- Allow custom frame rate in `AudioSegment.silent()`

# v0.15.0
- RAW audio format support
- Add `CouldntDecodeError` exception

# v0.14.2
- Fix Python 3.4 empty wave file bug

# v0.14.1
- Fix `mediainfo()` unescaped characters bug

# v0.14.0
- Rename `set_gain()` to `apply_gain_stereo()`

# v0.13.0
- Add `AudioSegment.pan()`

# v0.12.0
- Add `pydub.converter` logger
- Add `split_to_mono()`
- Fix `detect_silence()` edge case
- Fix uncommon wav format handling

# v0.11.0
- Add `max_dBFS` property

# v0.10.0
- Documentation overhaul
- Performance improvements for `overlay()`
- Add `invert_phase()`
- Fix type error in `get_sample_slice()`

# v0.9.5
- Add `pydub.generators` module
- Add `loops` keyword to `overlay()`

# v0.9.4
- Fix `db_to_float()` off-by-factor-of-2 bug

# v0.9.3
- Allow setting converter path via `AudioSegment.converter`

# v0.9.2
- Python 3.4 support
- Add `pydub.silence` module
- Fix ffmpeg auto-detection on Windows

# v0.9.1
- Runtime warning when ffmpeg/avconv not found

# v0.9.0
- PyPy support (pure-python audioop)
- avconv support
- Add `pydub.playback` module
- Add `pydub.utils.mediainfo()`
