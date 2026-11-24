# Railsback-Field 38-IWT: Specification & Theoretical Framework

## 1. Overview & Motivation
**Railsback-Field 38-IWT** (38-step Inharmonic Warped Tritave) is a non-logarithmic microtonal pitch architecture designed for isomorphic grid controllers, digital synthesizers, physical-modeling pianos (e.g., Pianoteq), and acoustic practice/tuning software. It unifies two physical and psychoacoustic principles into a single continuous pitch field:

1. **Microscopic Harmonic Resolution (`38-IWT`):** Replaces 12-EDO's coarse 100-cent grid with a 38-step division of the `3:1` tritave (`~50.05` cents/step), retaining a clean 24-step pseudo-octave (`~1201.23` cents) while unlocking low-beating 3-limit, 5-limit, and 11-limit intervals (`3:2`, `11:8`, `11:4`, `11:9`).
2. **Macroscopic Register Envelope (Physical Railsback Field):** Replaces rigid logarithmic periodicity (`f(m) = f_0 · r^(m/N)`) with a continuous S-shaped stretch curve anchored at `A4 = 440 Hz` and parameterized directly by measured string inharmonicity (\(B_{\text{A4}}\)).

---

## 2. Unified Acoustic & Psychoacoustic Foundation
Standard logarithmic tuning (`12-EDO` or pure equal-step scales) assumes ideal 1D strings and air columns with strictly harmonic integer overtones (`f_n = n · f_0`). Real acoustic instruments and human hearing diverge from pure logarithmic spacing through coupled mechanisms that pull toward a shared S-shaped stretch envelope:

* **String Stiffness & Dispersion:** Thick steel and nylon strings exhibit bending stiffness (`f_n ≈ n · f_0 · √(1 + B·n²)`), sharpening upper partials and requiring lower fundamentals in the bass (`-20¢` to `-40¢`) and raised fundamentals in the treble (`+20¢` to `+40¢`) to eliminate octave and twelfth beating.
* **Air-Column Impedance & End Corrections:** Conical and cylindrical woodwinds and flared brass bells experience frequency-dependent radiation impedance and tonehole cutoff shifts that subtly widen upper-register modes.
* **Psychoacoustic Octave Stretch & Mutual Entrainment:** Human auditory pitch perception naturally prefers slightly widened octaves (`> 1200¢`) in high registers, and ensemble performers continuously minimize partial beating against one another across overlapping registers. While local chord voicings shift dynamically toward Just Intonation, the **register-wide center of gravity** settles onto an S-shaped Railsback field whose curvature scales with the active register span and string stiffness of the instrument.

---

## 3. Mathematical Formulation

### Base Unwarped 38-IWT Lattice
An unwarped 38-step equal division of the `3:1` tritave (`1901.955` cents) defines step size:
$$\Delta c_{\text{base}} = \frac{1200 \log_2(3)}{38} \approx 50.05145\text{ cents}$$

### Continuous S-Shaped Railsback Field
Anchored at MIDI note \(m_0 = 69\) (`A4 = 440.0 Hz`), the frequency \(f(m)\) for any step index \(m\) is given by:

$$f(m) = f_{\text{ref}} \cdot r^{\frac{m - m_0}{N}} \cdot \left(1 + \alpha \cdot (m - m_0) \cdot |m - m_0|\right)$$

Where:
* \(f_{\text{ref}} = 440.0\text{ Hz}\), \(m_0 = 69\)
* \(r = 3.0\), \(N = 38\) (for full 38-IWT; or \(r = 2.0\), \(N = 12\) for standalone 12-EDO)
* \(\alpha\): Period-normalized register stretch coefficient derived from physical string inharmonicity:

$$\alpha = k_{\text{type}} \cdot B_{\text{A4}} \cdot \left(\frac{\log_2(r)}{N}\right)^2$$

### Acoustic Calibration Constants (`B_A4` & `k_type`)
Normalizing by \((\log_2(r)/N)^2\) makes \(\alpha\) invariant to the underlying lattice division (`38-IWT` tritave vs. `12-EDO` octave), ensuring that both scales follow the exact same macroscopic pitch envelope in Hz/cents for a given instrument profile:

* **\(B_{\text{A4}}\) (String Inharmonicity at `A4`):**
  * `concert_grand` (`3.5e-4`): ~274 cm (9 ft) concert grand; long strings, gentle stretch (`~±20¢`).
  * `medium_grand` (`5.5e-4`, default): ~180 cm (6 ft) studio/parlor grand; standard Railsback curve (`~-35¢` at `A0` to `+26¢` at `C8`, yielding \(\alpha \approx 2.502 \times 10^{-6}\) for 38-IWT).
  * `upright` (`8.5e-4`): ~122 cm (48 in) upright piano; short, stiff strings, steep stretch (`~±45¢`).
* **\(k_{\text{type}}\) (`2.615`):** Dimensionless partial-matching stretch weight balancing `4:2` and `6:3` octave/twelfth partial alignment.
* **Register Clamps:** Stretch multiplier is bounded within `[0.50, 1.15]` to prevent divergence beyond audible extremes.

---

## 4. Harmonic Geometry of 38-IWT & Register Stretch

Because \(38\) is even and \(24 / 38 \approx \log_3(2)\), the unwarped 38-IWT lattice preserves exact octave, tritone, and minor-third symmetries while unlocking 11-limit intervals (`11:9`, `11:8`, `11:4`) that fall directly in the cracks between standard 12-EDO semitones.

| Interval | Target Ratio | Pure JI | 38-IWT Step | Unwarped 38-IWT Error | Warped Error (`A4`) | Warped Range (`C2` – `C7`) | Nearest 12-EDO Error |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Unison** | `1:1` | `0.00¢` | `0` | `0.00¢` | `0.00¢` | `0.00¢` | `0.00¢` *(0 st)* |
| **Neutral Third** | `11:9` | `347.41¢` | `7` | `+2.95¢` | `+3.16¢` | `+5.99¢` to `+6.78¢` | `-47.41¢` / `+52.59¢` *(3 or 4 st)* |
| **Major Third** | `5:4` | `386.31¢` | `8` | `+14.10¢` | `+14.37¢` | `+17.54¢` to `+18.43¢` | `+13.69¢` *(4 st)* |
| **Perfect Fourth** | `4:3` | `498.04¢` | `10` | `+2.47¢` | `+2.90¢` | `+6.69¢` to `+7.80¢` | `+1.96¢` *(5 st)* |
| **Tritone** | `√2` | `600.00¢` | `12` | `+0.62¢` | `+1.24¢` | `+5.57¢` to `+6.91¢` | `0.00¢` *(6 st)* |
| **Perfect Fifth** | `3:2` | `701.96¢` | `14` | `-1.23¢` | `-0.39¢` | `+4.43¢` to `+5.98¢` | `-1.96¢` *(7 st)* |
| **Octave** | `2:1` | `1200.00¢` | `24` | `+1.23¢` | `+3.73¢` | `+9.92¢` to `+12.54¢` | `0.00¢` *(12 st)* |
| **11th Harmonic** | `11:4` | `1751.32¢` | `35` | `+0.48¢` | `+5.78¢` | `+11.50¢` to `+15.27¢` | `-51.32¢` / `+48.68¢` *(17 or 18 st)* |
| **Tritave** | `3:1` | `1901.96¢` | `38` | `0.00¢` | `+6.24¢` | `+11.47¢` to `+15.56¢` | `-1.96¢` *(19 st)* |

### Notes on Methodology & Register Warping
* **Tonic Independence:** Unlike fixed 12-tone Just Intonation (which requires choosing one of 12 tonic centers and incurs `21.5¢–41.1¢` wolf intervals upon modulation), the unwarped 38-IWT lattice is **translation-invariant**. Every interval is measured relative to any local `1:1` root, yielding consistent harmonic behavior across all 38 roots.
* **12-EDO Comparison (`st` = semitones):** Standard 12-EDO cannot represent 11-limit ratios (`11:9` and `11:4`). Both values are shown (`-47.41¢` / `+52.59¢`) to indicate that 12-EDO's closest neighboring semitones miss the pure ratio by roughly a quarter-tone on either side, whereas 38-IWT lands within `3¢` (`7` steps) and `0.5¢` (`35` steps).
* **Register Stretch (`C2` – `C7`):** Warped values are measured from `C2` (`m = 3`, `~64.6 Hz` upward), `A4` (`m = 69`, `440.0 Hz` upward), and `C7` (`m = 123`, `~2111.7 Hz` downward). Because the S-shaped Railsback curve compresses the bass and expands the treble, intervals widen slightly toward both register extremes—matching the stretched partials of acoustic strings rather than static mathematical ratios.

---

## 5. Isomorphic Grid Mapping & Tritave-Origin Projection

### `(4, 1)` Isomorphic Lattice Layout
On a row-offset grid where moving right adds `+1` step and moving up-right adds `+4` steps (`(4, 1)`):
* **Octave (`+24` steps):** Vector `(+6, 0)` (pure horizontal translation).
* **Tritave (`+38` steps):** Vector `(+9, +2)` (`9 × 4 + 2 = 38`).
* **12-Note Octave Subset (`railsback_38iwt_12sub`):** Stepping by stride `2` (`m_38 = 69 + 2·(m_12 - 69)`) extracts every second step (`~100.10¢` per key) rather than truncating consecutive `~50.05¢` steps. This maps a standard 12-key octave (`24` steps) onto a Piano or Jankó keyboard while keeping every pitch frequency-locked to the parent 38-IWT lattice.

### Conceptual Lens: 12-EDO as Tritave-Lattice Projection
Rather than treating 12-EDO as an isolated octave circle, 12-EDO chord inversions and upper extensions (`7ths`, `9ths`, `#11s`, `13ths`) can be reframed as a 2:1 modulo compression of a continuous 38-IWT tritave field—preserving familiar 12-tone voice-leading symmetries (`24`-step octave, `12`-step tritone) while restoring access to 11-limit upper partials (`11:4`, `11:9`) and natural register stretch.

---

## 6. Related Systems & Why the Tritave + S-Curve Works for 12-Tone & Jazz Harmony

While microtonal theory and psychoacoustic stretch curves are typically treated as separate domains, **Railsback-Field 38-IWT** bridges equal-tritave temperaments (`19-EDT` / `38-EDT`) with timbre-driven register stretching (Plomp–Levelt consonance curves, William Sethares's inharmonic tuning theory, and empirical piano Railsback curves):

* **Why a Virtual Tritave Lattice Improves Standard 12-Tone & Jazz Harmony:** Performers playing standard 12-note repertoire (via `railsback_38iwt_12sub` or on even steps of the `(4, 1)` grid) operate inside a `stride 2` projection of `38-IWT` (`2 × 19-EDT`). Because an unwarped `3:1` tritave lattice places its `3:2` fifth (`-1.23¢`), `11:8` harmonic tritone (`-0.75¢`), `9:4` major ninth (`-2.47¢`), `12:5` minor tenth (`-14.10¢`), and `27:8` major thirteenth (`-3.70¢`) slightly *flat* of pure ratios, the upward Railsback S-curve absorbs that deficit and lifts those intervals directly into Just Intonation:
  * **Middle Register (`C4–B4`):** `3:2` fifths (`0.10¢–0.80¢` error), `9:4` major ninths (`0.09¢–1.89¢`), and `27:8` major thirteenths (`0.19¢–2.61¢` across `C4–G4`) lock onto pure ratios across all 12 keys.
  * **Outer Registers (`C2–B2` & `C6–B6`):** The widened S-curve pulls the `9:5` minor seventh (`5.93¢–10.66¢` vs. `17.60¢` in 12-EDO) and `12:5` minor tenth (`0.08¢–3.92¢` vs. `15.64¢` in 12-EDO) directly into alignment.
* **Equal-Density Advantage over `24-EDO` and `39-EDT`:** At the same `~24` steps-per-octave grid density, `24-EDO` (`50.00¢/step`) simply bisects 12-EDO and leaves `3:2` (`-1.11¢`), `11:8` (`-0.77¢`), and `12:5` (`-11.75¢`) further from pure ratios once stretched, while **39-EDT** (Triple Bohlen–Pierce, `48.77¢/step`) lacks a usable `2:1` octave (`25` steps = `1219.20¢`) and cannot host standard 12-tone repertoire.

### Equal-Density S-Curve Comparison at `A4` (`Unwarped → Warped Error`)

| Interval | Ratio | **38-IWT (`~24` st/oct)** | **24-EDO (`24` st/oct)** | **12-EDO (`stride-2` subset)** |
| :--- | :---: | :---: | :---: | :---: |
| **Minor 3rd** | `6:5` | `-15.33¢ → -15.18¢` *(6)* | `-15.64¢ → -15.49¢` *(6)* | `-15.64¢ → -15.49¢` *(3)* |
| **Neutral 3rd** | `11:9` | **`+2.95¢ → +3.16¢`** *(7)* | `+2.59¢ → +2.80¢` *(7)* | *N/A (`-47.25¢` / `+52.75¢`)* |
| **Major 3rd** | `5:4` | `+14.10¢ → +14.37¢` *(8)* | `+13.69¢ → +13.96¢` *(8)* | `+13.69¢ → +13.96¢` *(4)* |
| **Perfect 4th** | `4:3` | `+2.47¢ → +2.90¢` *(10)* | `+1.96¢ → +2.39¢` *(10)* | `+1.96¢ → +2.39¢` *(5)* |
| **Harmonic Tritone** | `11:8` | **`-0.75¢ → -0.23¢`** *(11)* | `-1.32¢ → -0.77¢` *(11)* | *N/A (`+49.31¢`)* |
| **Perfect 5th** | `3:2` | **`-1.23¢ → -0.39¢`** *(14)* | `-1.96¢ → -1.11¢` *(14)* | `-1.96¢ → -1.11¢` *(7)* |
| **Harmonic 7th** | `7:4` | **`-17.85¢ → -16.29¢`** *(19)* | `-18.83¢ → -17.21¢` *(19)* | `+31.17¢ → +32.90¢` *(10)* |
| **Octave** | `2:1` | `+1.23¢ → +3.73¢` *(24)* | `0.00¢ → +2.49¢` *(24)* | `0.00¢ → +2.49¢` *(12)* |
| **Major 9th** | `9:4` | **`-2.47¢ → +0.92¢`** *(28)* | `-3.91¢ → -0.52¢` *(28)* | `-3.91¢ → -0.52¢` *(14)* |
| **Minor 10th** | `12:5` | **`-14.10¢ → -10.21¢`** *(30)* | `-15.64¢ → -11.75¢` *(30)* | `-15.64¢ → -11.75¢` *(15)* |
| **11th Harmonic** | `11:4` | **`+0.48¢ → +5.78¢`** *(35)* | `-1.32¢ → +4.28¢` *(35)* | *N/A (`+54.28¢`)* |
| **Tritave / 12th** | `3:1` | **`0.00¢ → +6.24¢`** *(38)* | `-1.96¢ → +4.28¢` *(38)* | `-1.96¢ → +4.28¢` *(19)* |
| **Major 13th** | `27:8` | **`-3.70¢ → +3.92¢`** *(42)* | `-5.87¢ → +1.74¢` *(42)* | `-5.87¢ → +1.74¢` *(21)* |

---

## 7. Synthesizer & Physical-Modeling Export (`.tun` & `.scl`/`.kbm`)
Because standard Scala (`.scl`) files wrap periodically at the final interval, non-periodic S-curves are exported as a **single full-range pseudo-octave** paired with a 1:1 linear `.kbm` mapping anchored at MIDI note `69` (`440.0 Hz`):

* **Standard 128-Note Tables (`0–127`):** `railsback_38iwt_12sub.scl` + `.kbm` maps directly to any 88-key controller or standard MIDI repertoire.
* **Extended Full-Spectrum Tables (`--extended`, up to `20 kHz`):** Generates ~200-note `.tun` and `.scl`/`.kbm` pairs for engines supporting extended keymaps (e.g., Surge XT?).
* **Pianoteq Calibration Note:** When loading `.scl`/`.kbm` files into physical-modeling pianos like Pianoteq, set Pianoteq's internal **Octave Stretching** parameter to `1.00` under the **Flat** temperament (or reduce Octave Stretching to `0.50–0.70` when blending with physical string dispersion) to prevent double-stretching the upper register.
