import os
import wave
import struct
import math

def create_wav(filename, samples, sample_rate=44100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)        # Mono
        wav_file.setsampwidth(2)        # 16-bit
        wav_file.setframerate(sample_rate)
        for s in samples:
            # Clamp to 16-bit signed range (-32767 to 32767)
            val = max(-32767, min(32767, int(s * 32767)))
            wav_file.writeframes(struct.pack('<h', val))

def generate_paddle(sample_rate=44100):
    # Short soft bounce blip (80ms, 520Hz -> 440Hz)
    duration = 0.08
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        freq = 520 - (t / duration) * 80
        envelope = math.exp(-t * 35)
        sample = 0.8 * math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(4 * math.pi * freq * t)
        samples.append(sample * envelope)
    return samples

def generate_brick(sample_rate=44100):
    # Short higher-pitched crunchy brick-break sound (110ms, 780Hz -> 320Hz)
    duration = 0.11
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        freq = 780 - (t / duration) * 460
        envelope = math.exp(-t * 28)
        sample = 0.7 * math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(6 * math.pi * freq * t)
        samples.append(sample * envelope)
    return samples

def generate_wall(sample_rate=44100):
    # Short click/bounce sound (50ms, 380Hz)
    duration = 0.05
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        freq = 380
        envelope = math.exp(-t * 45)
        sample = math.sin(2 * math.pi * freq * t)
        samples.append(sample * envelope)
    return samples

def generate_win(sample_rate=44100):
    # Pleasant ascending 4-tone victory arpeggio: C5 -> E5 -> G5 -> C6 (440ms)
    notes = [523.25, 659.25, 783.99, 1046.50]
    note_dur = 0.11
    samples = []
    for note_idx, freq in enumerate(notes):
        num_samples = int(note_dur * sample_rate)
        decay = 12 if note_idx == len(notes) - 1 else 20
        for i in range(num_samples):
            t = i / sample_rate
            env = math.exp(-t * decay)
            s = 0.75 * math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(4 * math.pi * freq * t)
            samples.append(s * env)
    return samples

def generate_lose(sample_rate=44100):
    # Descending 4-tone game-over sequence (560ms)
    notes = [440.0, 369.99, 293.66, 196.0]
    note_dur = 0.14
    samples = []
    for freq in notes:
        num_samples = int(note_dur * sample_rate)
        for i in range(num_samples):
            t = i / sample_rate
            env = math.exp(-t * 15)
            s = 0.8 * math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(3 * math.pi * freq * t)
            samples.append(s * env)
    return samples

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "assets", "sounds")
    create_wav(os.path.join(out_dir, "paddle.wav"), generate_paddle())
    create_wav(os.path.join(out_dir, "brick.wav"), generate_brick())
    create_wav(os.path.join(out_dir, "wall.wav"), generate_wall())
    create_wav(os.path.join(out_dir, "win.wav"), generate_win())
    create_wav(os.path.join(out_dir, "lose.wav"), generate_lose())
    print("Sound files created successfully in:", out_dir)

if __name__ == "__main__":
    main()