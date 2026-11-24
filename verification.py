#!/usr/bin/env python
import math
import re
import statistics


def load_tun_freqs(filename: str) -> dict[int, float]:
    """Reads [Exact Tuning] cents from an AnaMark .tun file and converts to Hz."""
    c_minus_1_hz = 8.175798915643707
    freqs = {}
    in_exact = False

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "[Exact Tuning]":
                in_exact = True
                continue
            elif line.startswith("[") and in_exact:
                break

            if in_exact and line.startswith("note "):
                match = re.match(r"note\s+(\d+)\s*=\s*([-\d.]+)", line)
                if match:
                    midi = int(match.group(1))
                    cents = float(match.group(2))
                    freqs[midi] = c_minus_1_hz * (2.0 ** (cents / 1200.0))
    return freqs


def generate_12edo_freqs(ref_midi: int = 69, ref_freq: float = 440.0) -> dict[int, float]:
    """Generates standard logarithmic 12-EDO frequencies (A4 = 440 Hz)."""
    return {m: ref_freq * (2.0 ** ((m - ref_midi) / 12.0)) for m in range(128)}


def generate_12ji_freqs(ref_midi: int = 69, ref_freq: float = 440.0) -> dict[int, float]:
    """Generates symmetric 5-limit Just Intonation anchored at C4 (MIDI 60) with A4 = 440 Hz."""
    ji_ratios = [
        1.0,         # C  (1:1)
        16.0 / 15.0, # C# (16:15)
        9.0 / 8.0,   # D  (9:8)
        6.0 / 5.0,   # Eb (6:5)
        5.0 / 4.0,   # E  (5:4)
        4.0 / 3.0,   # F  (4:3)
        45.0 / 32.0, # F# (45:32)
        3.0 / 2.0,   # G  (3:2)
        8.0 / 5.0,   # Ab (8:5)
        5.0 / 3.0,   # A  (5:3)
        9.0 / 5.0,   # Bb (9:5)
        15.0 / 8.0,  # B  (15:8)
    ]
    c4_hz = ref_freq / (5.0 / 3.0)
    freqs = {}
    for m in range(128):
        octave_shift = (m - 60) // 12
        degree = (m - 60) % 12
        freqs[m] = c4_hz * ji_ratios[degree] * (2.0 ** octave_shift)
    return freqs


def cents_error(f_root: float, f_upper: float, p_root: int, p_upper: int) -> float:
    """Calculates absolute cents deviation from the pure ratio (p_root / p_upper)."""
    actual_cents = 1200.0 * math.log2(f_upper / f_root)
    pure_cents = 1200.0 * math.log2(p_root / p_upper)
    return abs(actual_cents - pure_cents)


def run_verification(tun_38_12sub: str, tun_railsback_12edo: str):
    scales = {
        "38-IWT 12sub": load_tun_freqs(tun_38_12sub),
        "Railsback 12-EDO": load_tun_freqs(tun_railsback_12edo),
        "Standard 12-EDO": generate_12edo_freqs(),
        "12-JI (C-tonic)": generate_12ji_freqs(),
    }

    # (Interval Name, Semitone Offset, Numerator, Denominator)
    intervals = [
        ("Minor Third (6:5)", 3, 6, 5),
        ("Major Third (5:4)", 4, 5, 4),
        ("Perfect Fourth (4:3)", 5, 4, 3),
        ("Perfect Fifth (3:2)", 7, 3, 2),
        ("Minor Seventh (9:5)", 10, 9, 5),
        ("Major Seventh (15:8)", 11, 15, 8),
        ("Octave (2:1)", 12, 2, 1),
        ("Major Ninth (9:4)", 14, 9, 4),
        ("Minor Tenth (12:5)", 15, 12, 5),
        ("Major Tenth (5:2)", 16, 5, 2),
        ("Perfect 11th (8:3)", 17, 8, 3),
        ("Tritave / 12th (3:1)", 19, 3, 1),
        ("Major 13th (27:8)", 21, 27, 8),
        ("Double Octave (4:1)", 24, 4, 1),
    ]

    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octaves = [2, 4, 6] # MIDI bases: C2=36, C4=60, C6=84

    scale_names = list(scales.keys())
    all_errors: dict[str, dict[str, list[float]]] = {
        s: {iv[0]: [] for iv in intervals} for s in scale_names
    }

    header = f"{'Tonic':<6} | {'Interval':<20} | " + " | ".join(
        f"{s:<16}" for s in scale_names
    )
    print("=== ABSOLUTE CENTS ERROR (¢) FOR EVERY TONIC ACROSS OCTAVES 2, 4, AND 6 ===")
    print(header)
    print("-" * len(header))

    for oct_num in octaves:
        base_midi = (oct_num + 1) * 12
        for deg, note in enumerate(note_names):
            m_root = base_midi + deg
            tonic_label = f"{note}{oct_num}"
            for name, semi, p_num, p_den in intervals:
                row_vals = []
                for s in scale_names:
                    err = cents_error(scales[s][m_root], scales[s][m_root + semi], p_num, p_den)
                    all_errors[s][name].append(err)
                    row_vals.append(f"{err:>10.2f} ¢    ")
                print(f"{tonic_label:<6} | {name:<20} | " + " | ".join(row_vals))
            print("-" * len(header))

    print("\n=== ALL-TONIC CENTS ERROR STD DEV SUMMARY (Across all 36 Roots: C2..B2, C4..B4, C6..B6) ===")
    sum_header = f"{'Interval':<20} | " + " | ".join(f"{s:<16}" for s in scale_names)
    print(sum_header)
    print("-" * len(sum_header))

    total_std_devs = {s: 0.0 for s in scale_names}
    total_means = {s: 0.0 for s in scale_names}

    for name, _, _, _ in intervals:
        std_vals = []
        for s in scale_names:
            sd = statistics.stdev(all_errors[s][name])
            mn = statistics.mean(all_errors[s][name])
            total_std_devs[s] += sd
            total_means[s] += mn
            std_vals.append(f"{sd:>10.2f} ¢    ")
        print(f"{name:<20} | " + " | ".join(std_vals))

    print("-" * len(sum_header))
    print(
        f"{'SUM TOTAL STD DEV':<20} | "
        + " | ".join(f"{total_std_devs[s]:>10.2f} ¢    " for s in scale_names)
    )
    print(
        f"{'SUM TOTAL MEAN ERR':<20} | "
        + " | ".join(f"{total_means[s]:>10.2f} ¢    " for s in scale_names)
    )


if __name__ == "__main__":
    run_verification("railsback_38iwt_12sub.tun", "railsback_12edo.tun")
