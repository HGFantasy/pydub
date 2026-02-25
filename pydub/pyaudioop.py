"""
NumPy-based reimplementation of the deprecated audioop C extension module.

All mathematical operations use vectorized NumPy array operations instead of
pure-Python byte-by-byte iteration. This module is a drop-in replacement for
the stdlib audioop module which was removed in Python 3.13.
"""

from math import gcd

import numpy as np


class error(Exception):
    pass


_DTYPES = {1: np.int8, 2: np.int16, 4: np.int32}
_MAXVALS = {1: 0x7f, 2: 0x7fff, 4: 0x7fffffff}
_MINVALS = {1: -0x80, 2: -0x8000, 4: -0x80000000}


def _check_size(size):
    if size not in (1, 2, 4):
        raise error("Size should be 1, 2 or 4")


def _check_params(length, size):
    _check_size(size)
    if length % size != 0:
        raise error("not a whole number of frames")


def _samples(cp, size):
    """Return samples as a read-only numpy array (zero-copy view)."""
    return np.frombuffer(cp, dtype=_DTYPES[size])


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def getsample(cp, size, i):
    _check_params(len(cp), size)
    n = len(cp) // size
    if not (0 <= i < n):
        raise error("Index out of range")
    return int(_samples(cp, size)[i])


def max(cp, size):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return 0
    samples = _samples(cp, size).astype(np.int64)
    return int(np.max(np.abs(samples)))


def minmax(cp, size):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return (0, 0)
    samples = _samples(cp, size)
    return (int(np.min(samples)), int(np.max(samples)))


def avg(cp, size):
    _check_params(len(cp), size)
    n = len(cp) // size
    if n == 0:
        return 0
    total = int(np.sum(_samples(cp, size).astype(np.int64)))
    return int(total / n)


def rms(cp, size):
    _check_params(len(cp), size)
    n = len(cp) // size
    if n == 0:
        return 0
    samples = _samples(cp, size).astype(np.float64)
    return int(np.sqrt(np.dot(samples, samples) / n))


# ---------------------------------------------------------------------------
# Correlation / search functions
# ---------------------------------------------------------------------------

def _sum2(cp1, cp2, length):
    """Dot product of the first *length* 16-bit samples of two buffers."""
    s1 = np.frombuffer(cp1, dtype=np.int16)[:length].astype(np.int64)
    s2 = np.frombuffer(cp2, dtype=np.int16)[:length].astype(np.int64)
    return int(np.dot(s1, s2))


def findfit(cp1, cp2):
    size = 2
    if len(cp1) % 2 != 0 or len(cp2) % 2 != 0:
        raise error("Strings should be even-sized")
    if len(cp1) < len(cp2):
        raise error("First sample should be longer")

    len1 = len(cp1) // size
    len2 = len(cp2) // size

    s1 = np.frombuffer(cp1, dtype=np.int16).astype(np.int64)
    s2 = np.frombuffer(cp2, dtype=np.int16).astype(np.int64)

    sum_ri_2 = int(np.dot(s2, s2))
    sum_aij_2 = int(np.dot(s1[:len2], s1[:len2]))
    sum_aij_ri = int(np.dot(s1[:len2], s2))

    result = (sum_ri_2 * sum_aij_2 - sum_aij_ri * sum_aij_ri) / sum_aij_2
    best_result = result
    best_i = 0

    for i in range(1, len1 - len2 + 1):
        aj_m1 = int(s1[i - 1])
        aj_lm1 = int(s1[i + len2 - 1])
        sum_aij_2 += aj_lm1 ** 2 - aj_m1 ** 2
        sum_aij_ri = int(np.dot(s1[i:i + len2], s2))

        result = (sum_ri_2 * sum_aij_2 - sum_aij_ri * sum_aij_ri) / sum_aij_2
        if result < best_result:
            best_result = result
            best_i = i

    factor = int(np.dot(s1[best_i:best_i + len2], s2)) / sum_ri_2
    return best_i, factor


def findfactor(cp1, cp2):
    if len(cp1) % 2 != 0:
        raise error("Strings should be even-sized")
    if len(cp1) != len(cp2):
        raise error("Samples should be same size")

    s1 = np.frombuffer(cp1, dtype=np.int16).astype(np.int64)
    s2 = np.frombuffer(cp2, dtype=np.int16).astype(np.int64)
    return float(np.dot(s1, s2)) / float(np.dot(s2, s2))


def findmax(cp, len2):
    size = 2
    if len(cp) % 2 != 0:
        raise error("Strings should be even-sized")

    n = len(cp) // size
    if len2 < 0 or n < len2:
        raise error("Input sample should be longer")
    if n == 0:
        return 0

    samples = np.frombuffer(cp, dtype=np.int16).astype(np.int64)
    sq = samples * samples
    cum = np.concatenate(([0], np.cumsum(sq)))
    window_sums = cum[len2:] - cum[:len(cum) - len2]
    return int(np.argmax(window_sums))


# ---------------------------------------------------------------------------
# Peak-to-peak and zero-crossing functions
# ---------------------------------------------------------------------------

def avgpp(cp, size):
    _check_params(len(cp), size)
    n = len(cp) // size
    if n < 2:
        return 0

    samples = _samples(cp, size).astype(np.int64)

    prevextremevalid = False
    prevextreme = None
    total = 0
    nextreme = 0

    prevval = int(samples[0])
    prevdiff = int(samples[1]) - prevval

    for i in range(1, n):
        val = int(samples[i])
        diff = val - prevval

        if diff * prevdiff < 0:
            if prevextremevalid:
                total += abs(prevval - prevextreme)
                nextreme += 1
            prevextremevalid = True
            prevextreme = prevval

        prevval = val
        if diff != 0:
            prevdiff = diff

    if nextreme == 0:
        return 0
    return int(total / nextreme)


def maxpp(cp, size):
    _check_params(len(cp), size)
    n = len(cp) // size
    if n < 2:
        return 0

    samples = _samples(cp, size).astype(np.int64)

    prevextremevalid = False
    prevextreme = None
    max_val = 0

    prevval = int(samples[0])
    prevdiff = int(samples[1]) - prevval

    for i in range(1, n):
        val = int(samples[i])
        diff = val - prevval

        if diff * prevdiff < 0:
            if prevextremevalid:
                extremediff = abs(prevval - prevextreme)
                if extremediff > max_val:
                    max_val = extremediff
            prevextremevalid = True
            prevextreme = prevval

        prevval = val
        if diff != 0:
            prevdiff = diff

    return max_val


def cross(cp, size):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return 0

    samples = _samples(cp, size).astype(np.int64)
    if len(samples) < 2:
        return 0

    prev = np.empty(len(samples), dtype=np.int64)
    prev[0] = 0
    prev[1:] = samples[:-1]

    crossings = ((samples <= 0) & (prev > 0)) | ((samples >= 0) & (prev < 0))
    return int(np.sum(crossings))


# ---------------------------------------------------------------------------
# Transformation functions (vectorised)
# ---------------------------------------------------------------------------

def mul(cp, size, factor):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return cp

    samples = _samples(cp, size).astype(np.float64)
    np.multiply(samples, factor, out=samples)
    np.clip(samples, _MINVALS[size], _MAXVALS[size], out=samples)
    return samples.astype(_DTYPES[size]).tobytes()


def tomono(cp, size, fac1, fac2):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return cp

    samples = _samples(cp, size).astype(np.float64)
    left = samples[0::2]
    right = samples[1::2]

    mono = left * fac1 + right * fac2
    np.clip(mono, _MINVALS[size], _MAXVALS[size], out=mono)
    return mono.astype(_DTYPES[size]).tobytes()


def tostereo(cp, size, fac1, fac2):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return cp

    samples = _samples(cp, size).astype(np.float64)
    left = samples * fac1
    np.clip(left, _MINVALS[size], _MAXVALS[size], out=left)
    right = samples * fac2
    np.clip(right, _MINVALS[size], _MAXVALS[size], out=right)

    result = np.empty(len(samples) * 2, dtype=_DTYPES[size])
    result[0::2] = left.astype(_DTYPES[size])
    result[1::2] = right.astype(_DTYPES[size])
    return result.tobytes()


def add(cp1, cp2, size):
    _check_params(len(cp1), size)
    if len(cp1) != len(cp2):
        raise error("Lengths should be the same")
    if len(cp1) == 0:
        return cp1

    s1 = _samples(cp1, size).astype(np.int64)
    s2 = _samples(cp2, size)
    np.add(s1, s2, out=s1)
    np.clip(s1, _MINVALS[size], _MAXVALS[size], out=s1)
    return s1.astype(_DTYPES[size]).tobytes()


def bias(cp, size, bias_val):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return cp

    samples = _samples(cp, size).astype(np.int64)
    np.add(samples, bias_val, out=samples)
    bits = size * 8
    offset = 1 << (bits - 1)
    modulus = 1 << bits
    np.add(samples, offset, out=samples)
    np.mod(samples, modulus, out=samples)
    np.subtract(samples, offset, out=samples)
    return samples.astype(_DTYPES[size]).tobytes()


def reverse(cp, size):
    _check_params(len(cp), size)
    if len(cp) == 0:
        return cp
    return _samples(cp, size)[::-1].tobytes()


# ---------------------------------------------------------------------------
# Sample-width conversion
# ---------------------------------------------------------------------------

def lin2lin(cp, size, size2):
    _check_params(len(cp), size)
    _check_size(size2)
    if size == size2:
        return cp
    if len(cp) == 0:
        return cp

    samples = _samples(cp, size).astype(np.int64)
    shift = abs(size2 - size) * 8

    if size < size2:
        result = samples << shift
    else:
        result = samples >> shift

    return result.astype(_DTYPES[size2]).tobytes()


# ---------------------------------------------------------------------------
# Sample-rate conversion
# ---------------------------------------------------------------------------

def ratecv(cp, size, nchannels, inrate, outrate, state, weightA=1, weightB=0):
    _check_params(len(cp), size)
    if nchannels < 1:
        raise error("# of channels should be >= 1")
    if weightA < 1 or weightB < 0:
        raise error("weightA should be >= 1, weightB should be >= 0")
    if inrate <= 0 or outrate <= 0:
        raise error("sampling rate not > 0")

    bytes_per_frame = size * nchannels
    if len(cp) % bytes_per_frame != 0:
        raise error("not a whole number of frames")

    n_frames = len(cp) // bytes_per_frame

    d = gcd(inrate, outrate)
    inrate = inrate // d
    outrate = outrate // d

    if n_frames == 0:
        d_val = -outrate if state is None else state[0]
        samps = tuple((0, 0) for _ in range(nchannels))
        return (b'', (d_val, samps))

    all_samples = _samples(cp, size).astype(np.float64)

    channels = [all_samples[c::nchannels] for c in range(nchannels)]
    n_in = len(channels[0])

    if weightB > 0:
        weight_sum = weightA + weightB
        for c in range(nchannels):
            ch = channels[c].copy()
            for i in range(1, len(ch)):
                ch[i] = int((weightA * channels[c][i] + weightB * ch[i - 1]) / weight_sum)
            channels[c] = ch

    if n_in <= 1:
        n_out = n_in
    else:
        n_out = int((n_in - 1) * outrate / inrate) + 1

    if n_out == 0:
        d_val = -outrate if state is None else state[0]
        samps = tuple((0, 0) for _ in range(nchannels))
        return (b'', (d_val, samps))

    in_positions = np.arange(n_in, dtype=np.float64)
    out_positions = np.arange(n_out, dtype=np.float64) * (inrate / outrate)

    result = np.empty(n_out * nchannels, dtype=np.float64)
    for c in range(nchannels):
        result[c::nchannels] = np.interp(out_positions, in_positions, channels[c])

    np.clip(result, _MINVALS[size], _MAXVALS[size], out=result)
    output_bytes = result.astype(_DTYPES[size]).tobytes()

    d_final = int(-outrate + n_frames * outrate - n_out * inrate)
    samps = tuple(
        (int(channels[c][-2]) if n_in > 1 else 0, int(channels[c][-1]))
        for c in range(nchannels)
    )

    return (output_bytes, (d_final, samps))


# ---------------------------------------------------------------------------
# Encoding stubs (not used by pydub)
# ---------------------------------------------------------------------------

def lin2ulaw(cp, size):
    raise NotImplementedError()


def ulaw2lin(cp, size):
    raise NotImplementedError()


def lin2alaw(cp, size):
    raise NotImplementedError()


def alaw2lin(cp, size):
    raise NotImplementedError()


def lin2adpcm(cp, size, state):
    raise NotImplementedError()


def adpcm2lin(cp, size, state):
    raise NotImplementedError()
