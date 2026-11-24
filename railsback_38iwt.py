#!/usr/bin/env python

import argparse
import math
from datetime import date

# ==============================================================================
# ACOUSTIC & PSYCHOACOUSTIC CALIBRATION CONSTANTS
# ==============================================================================
# Standard concert pitch anchor (MIDI 69 = A4)
REF_MIDI = 69
REF_FREQ_HZ = 440.0

# Standard AnaMark 0-cent reference frequency (MIDI 0 = C-1 in 12-EDO at A440)
C_MINUS_1_HZ = 8.175798915643707

# Empirical string inharmonicity coefficients at A4 (B_A4) by instrument class.
# In string physics, partial frequencies sharpen as f_n = n * f_0 * sqrt(1 + B * n^2).
PIANO_PROFILES = {
    "concert_grand": 3.5e-4,  # ~274 cm (9 ft) concert grand: long strings, gentle stretch (~±20¢)
    "medium_grand": 5.5e-4,   # ~180 cm (6 ft) studio/parlor grand: standard Railsback (~±30-35¢)
    "upright": 8.5e-4,        # ~122 cm (48 in) upright piano: short stiff strings, steep stretch (~±45¢)
}

# Active instrument calibration target for generation
ACTIVE_PROFILE = "medium_grand"
B_A4 = PIANO_PROFILES[ACTIVE_PROFILE]

# Dimensionless partial-matching stretch weight (k_type):
# Scales the octave-widening envelope across 4:2 / 6:3 partial alignment regimes.
# Calibrated so B_A4 = 5.5e-4 (medium_grand) yields ~-35¢ at A0 and ~+26¢ at C8.
PARTIAL_STRETCH_WEIGHT = 2.615

# Physical safety bounds preventing extreme register divergence below A0 or above C8
BASS_STRETCH_FLOOR = 0.50
TREBLE_STRETCH_CEILING = 1.15


def compute_railsback_alpha(
    steps_per_period: int,
    period_ratio: float,
    b_a4: float = B_A4,
    stretch_weight: float = PARTIAL_STRETCH_WEIGHT,
) -> float:
    """
    Derives the continuous S-curve coefficient (alpha) from physical string
    inharmonicity at A4 (b_a4) and partial-matching stretch weight.

    Normalizing by (step_size_in_octaves)^2 makes alpha invariant to the
    underlying lattice division (e.g., 38-step tritave vs. 12-step octave),
    ensuring identical macroscopic pitch stretch in Hz/cents for a given piano.
    """
    step_octaves = math.log2(period_ratio) / steps_per_period
    return stretch_weight * b_a4 * (step_octaves ** 2)


def railsback_freq(
    m: int,
    steps_per_period: int,
    period_ratio: float,
    alpha: float,
    ref_midi: int = REF_MIDI,
    ref_freq: float = REF_FREQ_HZ,
) -> float:
    """
    Evaluates the continuous Railsback-warped frequency at step index m:
        f(m) = f_ref * r^((m - m_0)/N) * (1 + alpha * dm * |dm|)
    """
    dm = m - ref_midi
    stretch = 1.0 + alpha * dm * abs(dm)
    stretch = max(BASS_STRETCH_FLOOR, min(stretch, TREBLE_STRETCH_CEILING))
    return ref_freq * (period_ratio ** (dm / steps_per_period)) * stretch


def generate_freq_series(
    steps_per_period: int,
    period_ratio: float,
    alpha: float,
    stride: int = 1,
    extended: bool = False,
    max_hz: float = 20000.0,
) -> list[float]:
    freqs = []
    m = 0
    while True:
        effective_m = REF_MIDI + stride * (m - REF_MIDI)
        f = railsback_freq(effective_m, steps_per_period, period_ratio, alpha)
        if not extended and m >= 128:
            break
        if extended and m >= 128 and f > max_hz:
            break
        freqs.append(f)
        m += 1
    return freqs

def write_tun_from_freqs(
    filename: str,
    name: str,
    scale_id: str,
    description: str,
    notes_per_octave: int,
    freqs_hz: list[float],
    ref_midi: int = REF_MIDI,
    ref_freq: float = REF_FREQ_HZ,
):
    today_str = date.today().isoformat()

    lines = [
        f"; AnaMark Tuning File (.tun) - {name}",
        "[Scale Begin]",
        'Format= "AnaMark-TUN"',
        "FormatVersion= 200",
        'FormatSpecs= "http://mark-henning.de"',
        "",
        "[Info]",
        f'Name= "{name}"',
        f'ID= "{scale_id}"',
        f'Filename= "{filename}"',
        'Author= "Generated Tuning Script"',
        f'Description= "{description}"',
        f'Date= "{today_str}"',
        'Editor= "Python Generator"',
        f"NotesPerOctave= {notes_per_octave}",
        "",
        "[Editor]",
        "Tuned= 1",
        "Invert= 0",
        "",
        "[Tuning]",
    ]

    exact_tuning_lines = ["", "[Exact Tuning]"]

    for m, freq in enumerate(freqs_hz):
        abs_cents = 1200.0 * math.log2(freq / C_MINUS_1_HZ)
        lines.append(f"note {m}={int(round(abs_cents))}")
        exact_tuning_lines.append(f"note {m}= {abs_cents:.6f}")

    lines.extend(exact_tuning_lines)

    # Emit Scale Workshop / AnaMark v2 [Functional Tuning] block anchored at ref_midi
    anchor_idx = ref_midi if (ref_midi + notes_per_octave) < len(freqs_hz) else 0
    if (anchor_idx + notes_per_octave) < len(freqs_hz):
        anchor_hz = freqs_hz[anchor_idx]
        lines.extend(["", "[Functional Tuning]"])
        for step in range(1, notes_per_octave):
            rel_cents = 1200.0 * math.log2(freqs_hz[anchor_idx + step] / anchor_hz)
            lines.append(f'note {step}="#=0 % {rel_cents:.6f}"')
        period_cents = 1200.0 * math.log2(freqs_hz[anchor_idx + notes_per_octave] / anchor_hz)
        lines.append(f'note {notes_per_octave}="#>-{notes_per_octave} % {period_cents:.6f} ~999"')
        lines.extend(["", f'note {ref_midi}="! {ref_freq:.6f}"'])

    lines.append("\n[Scale End]")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated '{filename}' ({notes_per_octave} notes/period, {len(freqs_hz)} total notes).")


def write_scl_kbm_from_freqs(
    base_filename: str,
    description: str,
    freqs_hz: list[float],
    ref_midi: int = REF_MIDI,
    ref_freq: float = REF_FREQ_HZ,
):
    scl_filename = f"{base_filename}.scl"
    kbm_filename = f"{base_filename}.kbm"
    num_intervals = len(freqs_hz) - 1
    f0 = freqs_hz[0]

    # 1. Generate Scala (.scl) with all notes inside a single non-wrapping pseudo-octave
    scl_lines = [
        f"! {scl_filename}",
        "!",
        description,
        f" {num_intervals}",
        "!",
    ]
    for f in freqs_hz[1:]:
        cents = 1200.0 * math.log2(f / f0)
        scl_lines.append(f" {cents:.6f}")

    with open(scl_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(scl_lines) + "\n")

    # 2. Generate Keyboard Mapping (.kbm) spanning the entire table 1:1
    kbm_lines = [
        f"! {kbm_filename}",
        "! Size of map (pattern repeats every N keys; set to full span to prevent wrapping)",
        f"{num_intervals}",
        "! First MIDI note number to retune",
        "0",
        "! Last MIDI note number to retune",
        "127",
        "! Middle note where the first entry of the mapping is mapped to",
        "0",
        "! Reference note for which frequency is given",
        f"{ref_midi}",
        "! Frequency to tune the above note to (Hz)",
        f"{ref_freq:.6f}",
        "! Scale degree to consider as formal octave",
        f"{num_intervals}",
        "! Mapping.",
    ]
    for i in range(num_intervals):
        kbm_lines.append(f"{i}")

    with open(kbm_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(kbm_lines) + "\n")

    print(f"Generated '{scl_filename}' and '{kbm_filename}' ({num_intervals} intervals, span 0..{num_intervals}).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate AnaMark .tun and Scala .scl/.kbm files for Railsback-Field tunings."
    )
    parser.add_argument(
        "--extended",
        action="store_true",
        help="Extend note table beyond MIDI 127 up to 20 kHz for full-spectrum engines",
    )
    args = parser.parse_args()
    suffix = "_ext" if args.extended else ""

    # 1. Full Railsback-Field 38-IWT (3:1 tritave divided into 38 steps)
    alpha_38 = compute_railsback_alpha(steps_per_period=38, period_ratio=3.0)
    desc_38 = (
        f"38-step Inharmonic Warped Tritave calibrated to Railsback field "
        f"({ACTIVE_PROFILE}, B_A4={B_A4:.2e}, alpha={alpha_38:.3e})"
    )
    freqs_38 = generate_freq_series(38, 3.0, alpha_38, stride=1, extended=args.extended)
    write_tun_from_freqs(
        filename=f"railsback_38iwt{suffix}.tun",
        name="Railsback-Field 38-IWT" + (" (Extended)" if args.extended else ""),
        scale_id=f"railsback_38iwt{suffix}",
        description=desc_38,
        notes_per_octave=38,
        freqs_hz=freqs_38,
    )
    write_scl_kbm_from_freqs(
        base_filename=f"railsback_38iwt{suffix}",
        description=desc_38,
        freqs_hz=freqs_38,
    )

    # 2. 12-Note Octave Subset of Railsback-Field 38-IWT (stride 2)
    desc_38_12sub = (
        f"12-note ~1201-cent octave subset extracted from Railsback-Field 38-IWT "
        f"(stride 2, {ACTIVE_PROFILE}, B_A4={B_A4:.2e})"
    )
    freqs_38_12sub = generate_freq_series(38, 3.0, alpha_38, stride=2, extended=args.extended)
    write_tun_from_freqs(
        filename=f"railsback_38iwt_12sub{suffix}.tun",
        name="Railsback 38-IWT (12-Note Octave Subset)" + (" (Extended)" if args.extended else ""),
        scale_id=f"railsback_38iwt_12sub{suffix}",
        description=desc_38_12sub,
        notes_per_octave=12,
        freqs_hz=freqs_38_12sub,
    )
    write_scl_kbm_from_freqs(
        base_filename=f"railsback_38iwt_12sub{suffix}",
        description=desc_38_12sub,
        freqs_hz=freqs_38_12sub,
    )

    # 3. Standalone Railsback-Field 12-EDO (2:1 octave divided into 12 steps)
    alpha_12 = compute_railsback_alpha(steps_per_period=12, period_ratio=2.0)
    desc_12 = (
        f"12-EDO octave scale calibrated to Railsback register stretch "
        f"({ACTIVE_PROFILE}, B_A4={B_A4:.2e}, alpha={alpha_12:.3e})"
    )
    freqs_12 = generate_freq_series(12, 2.0, alpha_12, stride=1, extended=args.extended)
    write_tun_from_freqs(
        filename=f"railsback_12edo{suffix}.tun",
        name="Railsback-Field 12-EDO" + (" (Extended)" if args.extended else ""),
        scale_id=f"railsback_12edo{suffix}",
        description=desc_12,
        notes_per_octave=12,
        freqs_hz=freqs_12,
    )
    write_scl_kbm_from_freqs(
        base_filename=f"railsback_12edo{suffix}",
        description=desc_12,
        freqs_hz=freqs_12,
    )
