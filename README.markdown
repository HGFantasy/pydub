# Pydub

> **This is a modernized fork of [jiaaro/pydub](https://github.com/jiaaro/pydub)**, the original audio manipulation library created by [James Robert](https://github.com/jiaaro). This fork drops Python 2 support, replaces the deprecated `audioop` C extension with a NumPy-based engine, migrates to modern Python tooling, and targets Python 3.9+.

Pydub lets you do stuff to audio in a way that isn't stupid.

| | |
| --- | --- |
| **Original project** | [github.com/jiaaro/pydub](https://github.com/jiaaro/pydub) |
| **Original author** | [James Robert (@jiaaro)](https://github.com/jiaaro) |
| **This fork** | [github.com/HGFantasy/pydub](https://github.com/HGFantasy/pydub) |
| **License** | [MIT](LICENSE) |

---

**Quick links**:
[Installation](#installation) ·
[API Documentation](API.markdown) ·
[Dependencies](#dependencies) ·
[Playback](#playback) ·
[ffmpeg setup](#getting-ffmpeg-set-up) ·
[What changed in this fork](#whats-different-in-this-fork) ·
[Bugs & Questions](#bugs--questions)


## What's different in this fork

| Area | Original (`jiaaro/pydub`) | This fork |
| --- | --- | --- |
| Python support | 2.7, 3.4–3.9 | **3.9+** |
| Audio math engine | C `audioop` (removed in Python 3.13) | **NumPy** vectorized ops |
| Build system | `setup.py` | **`pyproject.toml`** (hatchling) |
| Linting | pylama (advisory) | **ruff** (enforced) |
| CI | Travis CI + AppVeyor (defunct) | removed (bring your own) |
| Python 2 compat shims | ~200 lines (`basestring`, `xrange`, `izip`, …) | **deleted** |
| `scipy_effects.py` bugs | undefined `AudioSegment`, misspelled methods | **fixed** |


## Quickstart

Open a WAV file

```python
from pydub import AudioSegment

song = AudioSegment.from_wav("never_gonna_give_you_up.wav")
```

...or an mp3

```python
song = AudioSegment.from_mp3("never_gonna_give_you_up.mp3")
```

...or an ogg, or flv, or [anything else ffmpeg supports](https://www.ffmpeg.org/general.html#File-Formats)

```python
ogg_version = AudioSegment.from_ogg("never_gonna_give_you_up.ogg")
flv_version = AudioSegment.from_flv("never_gonna_give_you_up.flv")

mp4_version = AudioSegment.from_file("never_gonna_give_you_up.mp4", "mp4")
wma_version = AudioSegment.from_file("never_gonna_give_you_up.wma", "wma")
aac_version = AudioSegment.from_file("never_gonna_give_you_up.aiff", "aac")
```

Slice audio:

```python
# pydub does things in milliseconds
ten_seconds = 10 * 1000

first_10_seconds = song[:ten_seconds]

last_5_seconds = song[-5000:]
```

Make the beginning louder and the end quieter

```python
# boost volume by 6dB
beginning = first_10_seconds + 6

# reduce volume by 3dB
end = last_5_seconds - 3
```

Concatenate audio (add one file to the end of another)

```python
without_the_middle = beginning + end
```

How long is it?

```python
without_the_middle.duration_seconds == 15.0
```

AudioSegments are immutable

```python
# song is not modified
backwards = song.reverse()
```

Crossfade (again, beginning and end are not modified)

```python
# 1.5 second crossfade
with_style = beginning.append(end, crossfade=1500)
```

Repeat

```python
# repeat the clip twice
do_it_over = with_style * 2
```

Fade (note that you can chain operations because everything returns
an AudioSegment)

```python
# 2 sec fade in, 3 sec fade out
awesome = do_it_over.fade_in(2000).fade_out(3000)
```

Save the results (again whatever ffmpeg supports)

```python
awesome.export("mashup.mp3", format="mp3")
```

Save the results with tags (metadata)

```python
awesome.export("mashup.mp3", format="mp3",
    tags={'artist': 'Various artists', 'album': 'Best of 2011',
          'comments': 'This album is awesome!'})
```

You can pass an optional bitrate argument to export using any syntax ffmpeg
supports.

```python
awesome.export("mashup.mp3", format="mp3", bitrate="192k")
```

Any further arguments supported by ffmpeg can be passed as a list in a
`parameters` argument, with switch first, argument second. Note that no
validation takes place on these parameters, and you may be limited by what
your particular build of ffmpeg supports.

```python
# Use preset mp3 quality 0 (equivalent to lame V0)
awesome.export("mashup.mp3", format="mp3", parameters=["-q:a", "0"])

# Mix down to two channels and set hard output volume
awesome.export("mashup.mp3", format="mp3", parameters=["-ac", "2", "-vol", "150"])
```

## Debugging

Most issues people run into are related to converting between formats using
ffmpeg. Pydub provides a logger that outputs the subprocess calls to
help you track down issues:

```python
>>> import logging

>>> l = logging.getLogger("pydub.converter")
>>> l.setLevel(logging.DEBUG)
>>> l.addHandler(logging.StreamHandler())

>>> AudioSegment.from_file("./test/data/test1.mp3")
subprocess.call(['ffmpeg', '-y', '-i', '/tmp/tmpeZTgMy', '-vn', '-f', 'wav', '/tmp/tmpK5aLcZ'])
<pydub.audio_segment.AudioSegment object at 0x101b43e10>
```

Don't worry about the temporary files used in the conversion. They're cleaned up
automatically.

## Bugs & Questions

You can file bugs in the [issue tracker](https://github.com/HGFantasy/pydub/issues).

For questions about the core pydub API you can also browse
[Stack Overflow using the pydub tag](https://stackoverflow.com/questions/tagged/pydub).

## Installation

```
pip install pydub
```

Pydub requires **Python 3.9+**,
[NumPy](https://numpy.org/) (installed automatically), and
[ffmpeg](https://www.ffmpeg.org/) (see below).

Or install from this fork directly:

```
pip install git+https://github.com/HGFantasy/pydub.git@master
```

For development:

```
git clone https://github.com/HGFantasy/pydub.git
cd pydub
pip install -e ".[dev]"
```

## Dependencies

- **[NumPy](https://numpy.org/)** — required. Installed automatically via pip.
  Used internally for all audio sample manipulation (volume scaling, mixing,
  sample-rate conversion, etc.).
- **[ffmpeg](https://www.ffmpeg.org/)** — required for opening and saving
  non-WAV files (mp3, ogg, flac, etc.). See [Getting ffmpeg set up](#getting-ffmpeg-set-up) below.

### Playback

You can play audio if you have one of these installed (simpleaudio _strongly_ recommended):

- [simpleaudio](https://simpleaudio.readthedocs.io/en/latest/)
- [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/docs/#)
- ffplay (usually bundled with ffmpeg)

```python
from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("mysound.wav", format="wav")
play(sound)
```

## Getting ffmpeg set up

Mac (using [homebrew](https://brew.sh)):

```bash
brew install ffmpeg
```

Linux (using apt):

```bash
apt-get install ffmpeg
```

Windows:

1. Download a static build from [ffmpeg.org](https://ffmpeg.org/download.html) or [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
2. Extract and add the `bin` folder to your PATH.
3. `pip install pydub`

## Important Notes

`AudioSegment` objects are immutable.

### Ogg exporting and default codecs

The Ogg specification ([RFC 5334](https://tools.ietf.org/html/rfc5334)) does not specify
the codec to use, this choice is left up to the user. Vorbis and Theora are just
some of a number of potential codecs (see page 3 of the RFC) that can be used for the
encapsulated data.

When no codec is specified, exporting to `ogg` will _default_ to using `vorbis`
as a convenience. That is:

```python
from pydub import AudioSegment
song = AudioSegment.from_mp3("test/data/test1.mp3")
song.export("out.ogg", format="ogg")  # Is the same as:
song.export("out.ogg", format="ogg", codec="libvorbis")
```

## Examples

Convert a directory of videos to mp3:

```python
import os
import glob
from pydub import AudioSegment

video_dir = '/home/johndoe/downloaded_videos/'
extension_list = ('*.mp4', '*.flv')

os.chdir(video_dir)
for extension in extension_list:
    for video in glob.glob(extension):
        mp3_filename = os.path.splitext(os.path.basename(video))[0] + '.mp3'
        AudioSegment.from_file(video).export(mp3_filename, format='mp3')
```

Build a playlist with crossfades:

```python
from glob import glob
from pydub import AudioSegment

playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("*.mp3")]

first_song = playlist_songs.pop(0)
beginning_of_song = first_song[:30 * 1000]

playlist = beginning_of_song
for song in playlist_songs:
    playlist = playlist.append(song, crossfade=(10 * 1000))

playlist = playlist.fade_out(30)

playlist_length = len(playlist) / (1000 * 60)

with open(f"{playlist_length}_minute_playlist.mp3", 'wb') as out_f:
    playlist.export(out_f, format='mp3')
```

## License ([MIT](https://opensource.org/licenses/mit-license.php))

Original work copyright © 2011 [James Robert](http://jiaaro.com).
See [AUTHORS](AUTHORS) for the full list of contributors to the original project.

This fork is maintained by [@HGFantasy](https://github.com/HGFantasy) and is
distributed under the same MIT license.

```
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
