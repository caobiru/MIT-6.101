"""
6.101 Lab 0:
Audio Processing
"""

import wave
import struct

# No additional imports allowed!


def backwards(sound):
    """
    Returns a new sound containing the samples of the original in reverse
    order, without modifying the input sound.

    Args:
        sound: a dictionary representing the original mono sound

    Returns:
        A new mono sound dictionary with the samples in reversed order
    """
    reversed_sound = {
        "rate": sound["rate"],
        "samples": list(reversed(sound["samples"])),
    }
    
    return reversed_sound


def mix(sound1, sound2, p):
    # mix 2 good sounds
    if (
        (sound1["rate"]) == False 
        or (sound2["rate"]) == False 
        or (sound1["rate"] != sound2["rate"])
    ): 
        return None

    rate = sound1["rate"]  # get rate
    sound1 = sound1["samples"]
    sound2 = sound2["samples"]
    length = min(len(sound1), len(sound2))

    mix = []
    for i in range(0, length):
        mix.append(p * sound1[i] + sound2[i] * (1 - p))  # add sounds

    return {"rate": rate, "samples": mix}  # return new sound


def echo(sound, num_echoes, delay, scale):
    """
    Compute a new signal consisting of several scaled-down and delayed versions
    of the input sound. Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        num_echoes: int, the number of additional copies of the sound to add
        delay: float, the amount of seconds each echo should be delayed
        scale: float, the amount by which each echo's samples should be scaled

    Returns:
        A new mono sound dictionary resulting from applying the echo effect.
    """
    
    sample_delay = round(delay * sound["rate"])
    echo_sound = sound["samples"][:]
    added_sound = sound["samples"][:]

    for i in range(1, num_echoes + 1):
        added_sound = [x * scale for x in added_sound]

        length = len(echo_sound)
        added_length = len(added_sound)
        
        if sample_delay <= added_length:
            for j in range(sample_delay * i, length):
                echo_sound[j] += added_sound[j - sample_delay * i]
            echo_sound.extend(added_sound[length - sample_delay * i :])
                            
        else:
            echo_sound.extend([0,] * (sample_delay - added_length))
            echo_sound.extend(added_sound)
        
    # print(echo_sound)
    
    return {"rate": sound["rate"], "samples": echo_sound}


def pan(sound):

    left = sound["left"][:]
    right = sound["right"][:]
    length = len(left)
    
    if length == 1:
        right[0] = 0
        left[0] = 1
        
    else:
        for i in range(0, length):
            right[i] *= i / (length - 1)
            left[i] *= 1 - i / (length - 1)

    return {"rate": sound["rate"], "left": left, "right": right}    
    
    
def remove_vocals(sound):
    left = sound["left"][:]
    right = sound["right"][:]
    remove = sound["right"][:]
    length = len(left)
    
    for i in range(0, length):
        remove[i] = left[i] - right[i]
    
    return {"rate": sound["rate"], "samples": remove}       


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Load a file and return a sound dictionary.

    Args:
        filename: string ending in '.wav' representing the sound file
        stereo: bool, by default sound is loaded as mono, if True sound will
            have left and right stereo channels.

    Returns:
        A dictionary representing that sound.
    """
    sound_file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = sound_file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    left = []
    right = []
    for i in range(count):
        frame = sound_file.readframes(1)
        if chan == 2:
            left.append(struct.unpack("<h", frame[:2])[0])
            right.append(struct.unpack("<h", frame[2:])[0])
        else:
            datum = struct.unpack("<h", frame)[0]
            left.append(datum)
            right.append(datum)

    if stereo:
        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = [(ls + rs) / 2 for ls, rs in zip(left, right)]
        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Save sound to filename location in a WAV format.

    Args:
        sound: a mono or stereo sound dictionary
        filename: a string ending in .WAV representing the file location to
            save the sound in
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for l_val, r_val in zip(sound["left"], sound["right"]):
            l_val = int(max(-1, min(1, l_val)) * (2**15 - 1))
            r_val = int(max(-1, min(1, r_val)) * (2**15 - 1))
            out.append(l_val)
            out.append(r_val)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    
    mystery = load_wav("sounds/mystery.wav")
    write_wav(backwards(mystery), "mystery_reversed.wav")     
    
    synth = load_wav("sounds/synth.wav")
    water = load_wav("sounds/water.wav")
    write_wav(mix(synth, water, 0.2), "mix.wav")     
    
    chord = load_wav("sounds/chord.wav")
    write_wav(echo(chord, 5, 0.3, 0.6), "echo.wav")

    car = load_wav("sounds/car.wav", stereo=True)
    write_wav(pan(car), "ltorcar.wav")

    mountain = load_wav("sounds/lookout_mountain.wav", stereo = True)
    write_wav(remove_vocals(mountain), "removevocals_mountain.wav")