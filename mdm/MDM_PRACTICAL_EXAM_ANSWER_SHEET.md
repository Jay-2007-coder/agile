# MDM (Wireless & Mobile Communication) - Practical Exam Answer Sheet

---

## Student Details
- **Subject:** MDM - Wireless & Mobile Communication (CSDOL7012 / TE CSE-DS Sem V)
- **Institution:** Vidyavardhini's College of Engineering & Technology
- **Department:** Department of Computer Science & Engineering (Data Science)
- **Name:** Jay Chandrasen Talekar
- **Roll No & Branch:** 50 / CSE-DS
- **Academic Year:** 2026–27

---

## Table of Contents
1. [Experiment 02: Simulation of Basic Communication System (Tx-Channel-Rx)](#experiment-02-simulation-of-basic-communication-system-tx-channel-rx)
2. [Experiment 03: Demonstration of Frequency Reuse Concept in Cellular Systems](#experiment-03-demonstration-of-frequency-reuse-concept-in-cellular-systems)
3. [Experiment 04: Scanning Nearby Wi-Fi Networks Using Mobile Application](#experiment-04-scanning-nearby-wi-fi-networks-using-mobile-application)
4. [Experiment 05: Measurement of Wi-Fi Signal Strength (RSSI) vs Distance](#experiment-05-measurement-of-wi-fi-signal-strength-rssi-vs-distance)
5. [Experiment 06: Analysis of Channel Interference in 2.4 GHz Wi-Fi Band](#experiment-06-analysis-of-channel-interference-in-24-ghz-wi-fi-band)
6. [Experiment 07: Bluetooth Communication Between Mobile Devices](#experiment-07-bluetooth-communication-between-mobile-devices)
7. [Experiment 08: Study of Path Loss and Signal Attenuation in Indoor Wi-Fi Environment](#experiment-08-study-of-path-loss-and-signal-attenuation-in-indoor-wi-fi-environment)

---

# Experiment 02: Simulation of Basic Communication System (Tx-Channel-Rx)

### 1. Aim
To simulate a basic digital communication system consisting of a **Transmitter (Tx)**, an **Additive White Gaussian Noise (AWGN) Channel**, and a **Receiver (Rx)** using Python/MATLAB, and to evaluate system performance by calculating the **Bit Error Rate (BER)**.

---

### 2. Theory

#### 2.1 Basic Block Diagram of Communication System
A communication system transmits information from an information source to a destination via three primary building blocks:

```
+-------------------+      +-------------------+      +-------------------+
|  Transmitter (Tx) | ---> |  Channel (AWGN)   | ---> |   Receiver (Rx)   |
| (Gen, Mod, Amp)   |      | (Noise & Fading)  |      | (Demod, Detector) |
+-------------------+      +-------------------+      +-------------------+
```

1. **Transmitter (Tx):**
   - **Information Source & Encoding:** Generates binary digital sequence $b[n] \in \{0, 1\}$.
   - **Modulation (BPSK - Binary Phase Shift Keying):** Shifts the phase of a high-frequency carrier wave by $180^\circ$ depending on the input bit:
     $$\text{Bit } 0 \longrightarrow m(t) = -1 \implies s(t) = -A_c \cos(2\pi f_c t)$$
     $$\text{Bit } 1 \longrightarrow m(t) = +1 \implies s(t) = +A_c \cos(2\pi f_c t)$$
   - **Amplification:** Boosts signal power for transmission over the channel.

2. **Communication Channel:**
   - Physical medium (wireless free space, coaxial cable, optical fiber).
   - Introduces attenuation, distortion, and thermal noise modeled as **Additive White Gaussian Noise (AWGN)**:
     $$r(t) = s(t) + n(t)$$
     where $n(t)$ has zero mean ($\mu = 0$) and variance $\sigma^2 = \frac{N_0}{2}$.

3. **Receiver (Rx):**
   - **Coherent Demodulation:** Multiplies the received signal $r(t)$ with a locally synchronized carrier $\cos(2\pi f_c t)$:
     $$y(t) = r(t) \cdot \cos(2\pi f_c t) = s(t)\cos(2\pi f_c t) + n(t)\cos(2\pi f_c t)$$
   - **Integrator / Matched Filter:** Integrates over the bit period $T_b$:
     $$Y = \int_0^{T_b} y(t)\,dt$$
   - **Decision Device / Threshold Detector:**
     $$\hat{b} = \begin{cases} 1, & \text{if } Y > 0 \\ 0, & \text{if } Y \le 0 \end{cases}$$

#### 2.2 Bit Error Rate (BER)
Bit Error Rate measures the reliability of the digital link:
$$\text{BER} = \frac{\text{Number of Incorrect Bits Received}}{\text{Total Number of Transmitted Bits}}$$
Theoretically for BPSK in AWGN:
$$P_b = Q\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

---

### 3. Reading & Output

#### 3.1 Python Simulation Code
```python
import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_bits = 20
bits = np.random.randint(0, 2, num_bits)
fc = 5  # Carrier frequency (Hz)
fs = 1000  # Sampling frequency
tb = 1.0  # Bit duration (seconds)
t = np.linspace(0, num_bits * tb, num_bits * int(fs * tb), endpoint=False)

# NRZ Encoding: 0 -> -1, 1 -> +1
nrz_signal = np.repeat(np.where(bits == 0, -1, 1), int(fs * tb))

# Carrier Generation and BPSK Modulation
carrier = np.cos(2 * np.pi * fc * t)
tx_signal = nrz_signal * carrier

# AWGN Channel Addition
noise_std = 0.5
noise = np.random.normal(0, noise_std, len(tx_signal))
rx_signal = tx_signal + noise

# Coherent Demodulation & Detection
samples_per_bit = int(fs * tb)
recovered_bits = []
demodulated = rx_signal * carrier

for i in range(num_bits):
    bit_segment = demodulated[i * samples_per_bit:(i + 1) * samples_per_bit]
    integral_val = np.sum(bit_segment)
    recovered_bits.append(1 if integral_val > 0 else 0)

recovered_bits = np.array(recovered_bits)
errors = np.sum(bits != recovered_bits)
ber = errors / num_bits

print("Original Bits: ", bits)
print("Recovered Bits:", recovered_bits)
print("Number of Errors:", errors)
print("Bit Error Rate (BER):", ber)
```

#### 3.2 Experimental Readings & Output
- **Transmitted Data (20 bits):**
  `[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]`
- **Recovered Data at Receiver:**
  `[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]`
- **Total Transmitted Bits ($N$):** $20$
- **Total Erroneous Bits ($N_e$):** $0$
- **Calculated Bit Error Rate (BER):** $0.0$

#### 3.3 Visualized Waveforms Summary
1. **Original Binary Pulse:** Discrete rectangular waveform representing the binary sequence.
2. **Sine Wave Carrier:** Pure sinusoidal wave at frequency $f_c = 5\text{ Hz}$.
3. **Transmitted BPSK Signal:** Constant amplitude sinusoidal signal with abrupt $180^\circ$ ($\pi$ rad) phase transitions at bit boundaries where binary state changes.
4. **Received Signal with AWGN:** Modulated waveform superimposed with random Gaussian noise fluctuations.
5. **Demodulated Signal:** Baseband rectified integration output recovering clean binary decisions.

---

### 4. Conclusion
The basic communication system (Tx-Channel-Rx) was successfully simulated and analyzed. The modulation, transmission over a noisy channel, coherent demodulation, and detection stages were demonstrated. Under moderate noise variance ($\sigma = 0.5$), coherent detection effectively filtered out high-frequency noise and accurately recovered all 20 transmitted bits without errors, yielding a Bit Error Rate ($\text{BER}$) of $0.0$.

---
---

# Experiment 03: Demonstration of Frequency Reuse Concept in Cellular Systems

### 1. Aim
To demonstrate and visualize the **Frequency Reuse Concept** in cellular mobile communication systems using hexagonal geometry simulations, and to analyze the impact of cluster size ($N$) and reuse distance ($D$) on **Co-Channel Interference (CCI)** and **Signal-to-Interference-plus-Noise Ratio (SINR)**.

---

### 2. Theory

#### 2.1 Cellular Geometry and Hexagonal Cell Concept
To provide uniform coverage over large geographic areas without gaps or overlaps, cellular networks model coverage areas as regular hexagons with radius $R$.

#### 2.2 Frequency Reuse Principle
Instead of dedicating unique frequency bands to every cell, available radio channels are partitioned into disjoint channel sets (e.g., $A, B, C, D, E, F, G$) and reused in geographically separated cells (co-channel cells).

```
        / \     / \
       / B \___/ C \
       \   /   \   /
      / \ /  A  \ / \
     / G \   *   / D \
     \   / \___/ \   /
      \ /  E \ /  F \
       \_____/ \_____/
```

#### 2.3 Cluster Size ($N$)
A **cluster** is a group of $N$ cells where each cell uses a unique set of channel frequencies. Cluster size is constrained by the geometry of hexagonal tessellation:
$$N = i^2 + i \cdot j + j^2 \quad (i, j \in \{0, 1, 2, \dots\})$$
- For $i=2, j=1$:
  $$N = 2^2 + (2 \times 1) + 1^2 = 4 + 2 + 1 = 7$$
- Common valid cluster sizes: $N \in \{3, 4, 7, 9, 12, \dots\}$

#### 2.4 Frequency Reuse Distance ($D$) and Co-Channel Reuse Ratio ($Q$)
The physical separation between the centers of co-channel cells is given by:
$$D = R \sqrt{3N}$$
For $N = 7$:
$$D = R \sqrt{3 \times 7} = R \sqrt{21} \approx 4.58 R$$
The co-channel reuse ratio $Q$:
$$Q = \frac{D}{R} = \sqrt{3N} \approx 4.58$$

#### 2.5 Co-Channel Interference (CCI) and SINR
Co-channel interference arises when identical frequencies are reused too closely. With 6 first-tier co-channel interferers:
$$\frac{S}{I} = \frac{R^{-\gamma}}{\sum_{k=1}^6 D_k^{-\gamma}} \approx \frac{1}{6} \left(\frac{D}{R}\right)^\gamma = \frac{(\sqrt{3N})^\gamma}{6}$$
where $\gamma$ is the path loss exponent ($\gamma \approx 4$ in urban propagation).
- **Larger cluster size $N$:** Larger reuse distance $D$, lower interference, higher SINR, but lower total spectrum capacity per area.
- **Smaller cluster size $N$:** Shorter reuse distance $D$, higher capacity, but higher co-channel interference.

---

### 3. Reading & Output

#### 3.1 Simulation Parameters
- Cell Radius ($R$): $1.0$ unit
- Cluster Size ($N$): $7$
- Frequency Groups: $7$ groups ($A, B, C, D, E, F, G$)
- Calculated Frequency Reuse Distance ($D$): $4.58 R$

#### 3.2 Observation Table: Frequency Assignment vs. Interference & SINR
| Sr. No. | Frequency Assignment Condition | Physical Distance Between Same-Frequency Cells | Interference Level | Calculated SINR (dB) | Signal Quality Evaluation |
|:---:|---|:---:|:---:|:---:|:---:|
| 1 | Different frequencies in adjacent cells | $1.00 R$ | $0.05$ | $12.79\text{ dB}$ | Excellent / Good |
| 2 | Same frequency in sufficiently distant cells ($N=7$) | $4.58 R$ ($D$) | $0.10$ | $8.24\text{ dB}$ | Good (Acceptable CCI) |
| 3 | Same frequency in moderately separated cells | $2.50 R$ | $0.35$ | $3.98\text{ dB}$ | Reduced / Degraded |
| 4 | Same frequency assigned to adjacent cells | $1.00 R$ | $0.90$ | $0.22\text{ dB}$ | Severe Co-Channel Interference / Poor |

#### 3.3 Visual Output Summary
- **19-Cell Hexagonal Cellular Network:** Center cluster assigned frequencies $A$ through $G$, surrounded by first-tier clusters repeating identical frequency groups at distance $D = 4.58R$.
- **Adjacent Co-Channel Assignment Simulation:** When neighboring cells are both forced to frequency $A$, severe co-channel interference collapses the SINR from $12.79\text{ dB}$ to $0.22\text{ dB}$.

---

### 4. Conclusion
The simulation verified that frequency reuse is fundamental to maximizing spectral efficiency in cellular networks. By maintaining a geometric reuse distance of $D = R\sqrt{3N} \approx 4.58R$ for cluster size $N = 7$, the system operates with acceptable co-channel interference ($8.24\text{ dB}$ SINR). Conversely, assigning the same frequency to adjacent cells causes catastrophic co-channel interference and link failure.

---
---

# Experiment 04: Scanning Nearby Wi-Fi Networks Using Mobile Application

### 1. Aim
To scan nearby Wi-Fi networks using a mobile Wi-Fi Analyzer application and analyze network parameters including **SSID**, **BSSID**, **RSSI (Received Signal Strength Indicator)**, **operating channel**, **frequency band (2.4 GHz vs. 5 GHz)**, and **channel occupancy**.

---

### 2. Theory

#### 2.1 Wi-Fi Standards and Frequency Bands
- **IEEE 802.11 Standards:** Define Physical (PHY) and MAC layers for wireless local area networking.
  - **802.11b/g/n:** 2.4 GHz ISM band.
  - **802.11a/n/ac/ax:** 5.0 GHz / 6.0 GHz bands.

#### 2.2 Key Network Parameters
1. **SSID (Service Set Identifier):** The human-readable name of the wireless network broadcasted in periodic 802.11 beacon frames.
2. **BSSID (Basic Service Set Identifier):** The unique 48-bit hardware MAC address of the Access Point radio interface.
3. **RSSI (Received Signal Strength Indicator):** Received power measured in **dBm** (decibels relative to 1 milliwatt):
   $$\text{Power (dBm)} = 10 \cdot \log_{10}\left(\frac{P_{\text{mW}}}{1\text{ mW}}\right)$$
   RSSI values are negative. Values closer to $0\text{ dBm}$ indicate stronger signals:
   - **$-30$ to $-50\text{ dBm}$:** Excellent signal
   - **$-50$ to $-67\text{ dBm}$:** Very Good / Strong (optimal for HD streaming and VoIP)
   - **$-67$ to $-75\text{ dBm}$:** Good / Fair (usable for web browsing)
   - **$-75$ to $-85\text{ dBm}$:** Weak (frequent retries and packet loss)
   - **$< -85\text{ dBm}$:** Very Poor / Disconnected

#### 2.3 2.4 GHz vs. 5 GHz Band Comparison
| Feature | 2.4 GHz Band | 5.0 GHz Band |
|---|---|---|
| Frequency Range | 2400 MHz – 2483.5 MHz | 5150 MHz – 5850 MHz |
| Channel Width | 20 MHz (rarely 40 MHz) | 20 / 40 / 80 / 160 MHz |
| Non-Overlapping Channels | Only 3 (Channels 1, 6, 11) | Up to 24+ non-overlapping channels |
| Range & Obstacle Penetration | High (better wall penetration) | Moderate / Low (attenuates faster) |
| Max Data Throughput | Lower ($\sim 300\text{ Mbps}$) | Much Higher ($> 1\text{ Gbps}$) |

---

### 3. Reading & Output

#### 3.1 Experimental Setup
- **Mobile Device:** Android Smartphone (Wi-Fi 6 capable)
- **Application Used:** Wi-Fi Analyzer / NetSpot
- **Location:** VCET Campus / Academic Lab

#### 3.2 Observation Table: Detected Wireless Networks
| Sr. No. | SSID (Network Name) | BSSID (MAC Address) | RSSI (dBm) | Channel No. | Frequency Band | Channel Width | Signal Quality | Security |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `OnePlusNordCE4` | `6a:d9:bb:ec:b6:cc` | **-53 dBm** | 11 | 2.4 GHz | 20 MHz | Excellent | WPA2/WPA3 |
| 2 | `GSVCET 2.4G` | `64:29:43:b7:0b:c0` | **-55 dBm** | 1 | 2.4 GHz | 20 MHz | Very Good | WPA/WPA2 |
| 3 | `GSVCET 5G` | `64:29:43:b7:0b:c8` | **-58 dBm** | 149 (155) | 5.0 GHz | 80 MHz | Excellent | WPA/WPA2 |
| 4 | `Rugved` | `26:7e:2b:ea:9c:94` | **-59 dBm** | 149 (155) | 5.0 GHz | 80 MHz | Good | WPA2 |
| 5 | `Exam Section` | `a4:2b:b0:12:ef:31` | **-66 dBm** | 1 | 2.4 GHz | 20 MHz | Good | WPA2 |
| 6 | `office_conference` | `10:27:f5:37:55:b2` | **-67 dBm** | 11 | 2.4 GHz | 20 MHz | Fair | WPA/WPA2 |
| 7 | `VCET-5G` | `b0:a7:b9:30:4c:1d` | **-71 dBm** | 36 (42) | 5.0 GHz | 80 MHz | Fair / Weak | WPA2 |
| 8 | `VCET-2.4G` | `b0:a7:b9:30:4c:1c` | **-74 dBm** | 6 | 2.4 GHz | 20 MHz | Poor | WPA2 |

#### 3.3 Channel Occupancy Analysis
- **Strongest Network:** `OnePlusNordCE4` ($-53\text{ dBm}$) and `GSVCET 2.4G` ($-55\text{ dBm}$).
- **Most Crowded Channels:** Channel 1 (2 networks) and Channel 11 (2 networks).
- **Least Crowded Channel:** Channel 6 (1 network).
- **Band Observation:** The 5 GHz networks utilize wider channels (80 MHz) and operate on high channels (149 and 36) with zero co-channel congestion.

---

### 4. Conclusion
Using the Wi-Fi Analyzer application, nearby wireless networks were successfully scanned and analyzed. The results demonstrate that RSSI directly reflects link quality, with values above $-65\text{ dBm}$ providing stable performance. In the 2.4 GHz band, network deployment was concentrated on channels 1 and 11, while the 5 GHz band offered significantly higher channel bandwidth (80 MHz) and negligible co-channel interference.

---
---

# Experiment 05: Measurement of Wi-Fi Signal Strength (RSSI) vs Distance

### 1. Aim
To measure the Wi-Fi signal strength (**RSSI**) at varying distances from a wireless router and to evaluate the relationship between **signal attenuation and physical distance** based on radio propagation models.

---

### 2. Theory

#### 2.1 Free Space Path Loss (FSPL) and Friis Transmission Formula
In ideal free-space conditions, electromagnetic wave power density spreads over the surface of an expanding sphere:
$$P_r = P_t \cdot G_t \cdot G_r \left(\frac{\lambda}{4\pi d}\right)^2$$
This obeys the **Inverse Square Law**, where received power decreases proportionally to the square of distance:
$$P_r \propto \frac{1}{d^2}$$

#### 2.2 Log-Distance Path Loss Model
In realistic indoor propagation environments, path loss in dB is modeled logarithmically:
$$\text{PL}(d)\text{ [dB]} = \text{PL}(d_0) + 10 \cdot n \cdot \log_{10}\left(\frac{d}{d_0}\right) + X_\sigma$$
Consequently, the received signal strength (RSSI in dBm) decreases logarithmically with distance:
$$\text{RSSI}(d) = \text{RSSI}(d_0) - 10 \cdot n \cdot \log_{10}\left(\frac{d}{d_0}\right)$$
where:
- $d_0$ = Reference distance (typically $1\text{ meter}$).
- $n$ = Path loss exponent ($n = 2.0$ in free space; $n = 2.5 - 4.0$ in indoor environments).
- $X_\sigma$ = Zero-mean Gaussian random variable representing shadow fading.

As physical separation $d$ increases, RSSI values become significantly more negative.

---

### 3. Reading & Output

#### 3.1 Experimental Setup
- **Access Point:** Wi-Fi Router placed at fixed position (height: 1.2 m).
- **Receiver:** Handheld smartphone running Wi-Fi Analyzer at the same antenna orientation.
- **Line-of-Sight Distances:** $1\text{ m}, 2\text{ m}, 5\text{ m}, 10\text{ m}, 15\text{ m}$.

#### 3.2 Observation Table: RSSI vs. Distance Measurements
*(Three independent readings recorded per distance to eliminate multipath fading fluctuations)*

| Sr. No. | Distance ($d$) | Sample 1 (dBm) | Sample 2 (dBm) | Sample 3 (dBm) | Average RSSI (dBm) | Signal Quality Evaluation |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **1 m** | -41 | -43 | -42 | **-42.0 dBm** | Excellent (Very Strong) |
| 2 | **2 m** | -47 | -49 | -48 | **-48.0 dBm** | Very Good |
| 3 | **5 m** | -56 | -58 | -57 | **-57.0 dBm** | Good (Stable connection) |
| 4 | **10 m** | -66 | -68 | -67 | **-67.0 dBm** | Fair / Usable |
| 5 | **15 m** | -74 | -76 | -75 | **-75.0 dBm** | Weak / Lower throughput |

#### 3.3 Graphical Trend (RSSI vs. Distance)
```
RSSI (dBm)
   0 |
 -20 |
 -40 |   * (1m, -42)
 -50 |         * (2m, -48)
 -60 |               * (5m, -57)
 -70 |                     * (10m, -67)
 -80 |                           * (15m, -75)
     +----------------------------------------
       0   2   4   6   8  10  12  14  16  Distance (m)
```
The plotted curve demonstrates a characteristic **logarithmic drop-off**, with rapid initial attenuation within the first 5 meters, followed by a gradual decay over larger distances.

---

### 4. Conclusion
The experiment verified that Wi-Fi signal strength (RSSI) is inversely proportional to the logarithm of distance, confirming the Log-Distance Path Loss model. The average signal dropped from **$-42.0\text{ dBm}$** at $1\text{ m}$ to **$-75.0\text{ dBm}$** at $15\text{ m}$ (a net attenuation of $33\text{ dB}$). Maintaining receiver placement within $5 - 10\text{ meters}$ ensures optimal signal quality and maximum throughput.

---
---

# Experiment 06: Analysis of Channel Interference in 2.4 GHz Wi-Fi Band

### 1. Aim
To analyze channel interference in the **2.4 GHz Wi-Fi band** by identifying nearby networks, recording operating channels and RSSI values, and evaluating the effects of **Co-Channel Interference (CCI)** and **Adjacent-Channel Interference (ACI)**.

---

### 2. Theory

#### 2.1 2.4 GHz ISM Spectrum Architecture
- **Frequency Range:** $2400\text{ MHz}$ to $2483.5\text{ MHz}$ ($83.5\text{ MHz}$ total bandwidth).
- **Channel Allocation:** Divided into 14 channels spaced only **$5\text{ MHz}$ apart** (except Channel 14).
- **Channel Bandwidth:** Each 802.11 transmission occupies **$20\text{ MHz}$** to **$22\text{ MHz}$**.

#### 2.2 Channel Overlap and Non-Overlapping Channels
Because channel bandwidth ($20\text{ MHz}$) is four times wider than the channel spacing ($5\text{ MHz}$), adjacent channels overlap heavily.
- **The Three Non-Overlapping Channels:** **Channel 1 (2412 MHz)**, **Channel 6 (2437 MHz)**, and **Channel 11 (2462 MHz)**.

```
       Ch 1 (2412)          Ch 6 (2437)          Ch 11 (2462)
     /-------------\      /-------------\      /-------------\
    /               \    /               \    /               \
---|-----------------|--|-----------------|--|-----------------|--- Frequency
  2402             2422 2427            2447 2452            2472
```

#### 2.3 Types of Wireless Interference
1. **Co-Channel Interference (CCI):**
   - Occurs when two or more APs operate on the *exact same channel* (e.g., two routers on Channel 1).
   - Under 802.11 CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance), devices share channel airtime.
   - Leads to transmission delays and throughput reduction, but no physical RF packet corruption.
2. **Adjacent-Channel Interference (ACI):**
   - Occurs when an AP operates on an *overlapping non-standard channel* (e.g., Channel 3 or 4).
   - The spectral masks bleed RF power into Channels 1 and 6 as raw electromagnetic noise.
   - CSMA/CA cannot decode the overlapping preamble, causing packet collisions, high frame error rates, and aggressive retransmissions.

---

### 3. Reading & Output

#### 3.1 Observation Table: Detected Networks & Operating Channels
| Sr. No. | SSID | RSSI (dBm) | Channel No. | Frequency Band | Interference Classification |
|:---:|---|:---:|:---:|:---:|---|
| 1 | `GSVCET` | **-45 dBm** | 11 | 2.4 GHz | Strong signal; Co-channel with Ch 11 |
| 2 | `Exam Section` | **-57 dBm** | 1 | 2.4 GHz | Moderate signal; Co-channel on Ch 1 |
| 3 | `OM 13R` | **-61 dBm** | 11 | 2.4 GHz | Moderate signal; shares Ch 11 with GSVCET |
| 4 | `RD` | **-75 dBm** | 1 | 2.4 GHz | Weak signal on Ch 1 |
| 5 | `Oppo F25` | **-80 dBm** | 4 | 2.4 GHz | **Overlapping Channel (causes ACI to Ch 1 & 6)** |
| 6 | `Dinesh` | **-80 dBm** | 1 | 2.4 GHz | Weak signal on Ch 1 |

#### 3.2 Channel Occupancy & Congestion Table
| Channel No. | Total Networks Detected | Strongest RSSI | Channel Occupancy | Primary Interference Type |
|:---:|:---:|:---:|:---:|---|
| **Channel 1** | 3 (`Exam Section`, `RD`, `Dinesh`) | -57 dBm | High Occupancy | Co-Channel Interference (CCI) |
| **Channel 4** | 1 (`Oppo F25`) | -80 dBm | Non-standard | **Severe Adjacent-Channel Interference (ACI)** |
| **Channel 6** | 0 | None detected | **Empty / Clear** | **Lowest Interference** |
| **Channel 11** | 2 (`GSVCET`, `OM 13R`) | -45 dBm | Moderate | Co-Channel Interference (CCI) |

#### 3.3 Channel Interference Analysis
- **Most Crowded Channels:** Channel 1 (3 active networks).
- **Least Crowded Channel:** Channel 6 (0 active networks).
- **Channel with Strongest Network:** Channel 11 (`GSVCET` at $-45\text{ dBm}$).
- **Interference Source:** The mobile hotspot `Oppo F25` configured on Channel 4 overlaps with both Channel 1 (2402–2422 MHz) and Channel 6 (2427–2447 MHz), inducing ACI across both bands.
- **Recommended Channel Assignment:** Reassigning the network to **Channel 6** eliminates interference and maximizes throughput.

---

### 4. Conclusion
Channel interference analysis revealed that the 2.4 GHz spectrum experiences high contention on Channel 1 and Channel 11. Crucially, non-standard channel selection (Channel 4) introduces destructive Adjacent-Channel Interference that corrupts packets on neighboring standard channels. Network administrators must strictly adhere to non-overlapping channels (**1, 6, and 11**) to maximize spectral efficiency and minimize packet retransmissions.

---
---

# Experiment 07: Bluetooth Communication Between Mobile Devices

### 1. Aim
To study **Bluetooth wireless communication** between mobile devices, examine the multi-stage connection handshake (inquiry, paging, authentication, and pairing), measure **Bluetooth RSSI vs. distance**, and evaluate signal attenuation caused by physical obstacles.

---

### 2. Theory

#### 2.1 Bluetooth Architecture (IEEE 802.15.1)
Bluetooth is a short-range Wireless Personal Area Network (WPAN) operating in the **2.4 GHz ISM band** (2402 MHz to 2480 MHz).
- **Frequency Hopping Spread Spectrum (FHSS):** Uses 79 RF channels with $1\text{ MHz}$ spacing, hopping at **1600 hops/second** to prevent interference from stationary Wi-Fi networks.
- **Network Topology:** **Piconet** consisting of 1 Master device and up to 7 active Slave devices.

#### 2.2 Bluetooth Power Classes
| Power Class | Maximum Output Power | Nominal Operating Range | Typical Application |
|:---:|:---:|:---:|---|
| **Class 1** | $100\text{ mW}$ ($+20\text{ dBm}$) | Up to $100\text{ meters}$ | Industrial gateways, long-range adapters |
| **Class 2** | $2.5\text{ mW}$ ($+4\text{ dBm}$) | Up to $10\text{ meters}$ | Smartphones, laptops, wireless audio |
| **Class 3** | $1.0\text{ mW}$ ($0\text{ dBm}$) | Up to $1\text{ meter}$ | Ultra-low power wearables / sensors |

#### 2.3 Handshake Protocol Stages
1. **Inquiry (Device Discovery):** The master broadcasts inquiry packets; nearby discoverable devices respond with FHS (Frequency Hop Synchronization) packets containing their Bluetooth Device Address (BD_ADDR).
2. **Paging (Connection Establishment):** The master transmits page packets targeted to the specific BD_ADDR to synchronize clock and hop sequences.
3. **Authentication & Pairing:** Devices exchange cryptographic nonces using **Secure Simple Pairing (SSP)** with Elliptic Curve Diffie-Hellman (ECDH) key exchange and 6-digit numeric comparison.
4. **Bonding & Encryption:** A shared 128-bit Link Key is generated and stored for AES-128 payload encryption.

---

### 3. Reading & Output

#### 3.1 Device Specifications
- **Master / Receiver Device:** Realme Narzo 60 5G (MAC: `B8:3E:7A:41:C5:92`, Bluetooth 5.2, Class 2)
- **Slave / Transmitter Device:** OnePlus Nord CE 3 (Bluetooth 5.2, Class 2)

#### 3.2 Observation Table: Bluetooth RSSI vs. Distance & Obstacle Test
*(Three independent measurements averaged per test point)*

| Sr. No. | Distance ($d$) / Condition | Sample 1 (dBm) | Sample 2 (dBm) | Sample 3 (dBm) | Average RSSI (dBm) | Signal Quality | Link State & Stability |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| 1 | **1 m (LOS)** | -47 | -46 | -48 | **-47.0 dBm** | Excellent | Connected; maximum data throughput |
| 2 | **2 m (LOS)** | -53 | -52 | -54 | **-53.0 dBm** | Very Good | Connected; stable connection |
| 3 | **5 m (LOS)** | -64 | -65 | -63 | **-64.0 dBm** | Good | Connected; normal operation |
| 4 | **8 m (LOS)** | -71 | -72 | -70 | **-71.0 dBm** | Fair | Connected; minor throughput reduction |
| 5 | **10 m (LOS)** | -77 | -78 | -76 | **-77.0 dBm** | Weak | Connected; increased latency |
| 6 | **15 m (LOS)** | -88 | -87 | -89 | **-88.0 dBm** | Very Weak | Limit of communication; packet retries |
| 7 | **5 m (Behind Brick Wall)** | -74 | -75 | -73 | **-74.0 dBm** | Weak | Obstacle attenuation ($\approx 10\text{ dB}$ loss) |

#### 3.3 Observation Insights
- **Line-of-Sight Range:** Signal decreases steadily from **$-47.0\text{ dBm}$** at $1\text{ m}$ to **$-88.0\text{ dBm}$** at $15\text{ m}$.
- **Obstacle Effect:** Introducing an indoor brick wall at $5\text{ meters}$ dropped the RSSI from **$-64.0\text{ dBm}$** to **$-74.0\text{ dBm}$**, confirming that structural obstacles cause $\approx 10\text{ dB}$ of penetration attenuation.
- **Connection Limit:** At distances exceeding 15 meters, the Class 2 transceiver reaches its sensitivity threshold ($-90\text{ dBm}$), leading to connection termination.

---

### 4. Conclusion
The Bluetooth communication process was successfully evaluated across discovery, pairing, and data link phases. The experimental observations confirm that Class 2 Bluetooth devices operate with high stability within a $10\text{-meter}$ radius. Physical distance and indoor obstacles significantly attenuate signal strength, with a brick wall introducing approximately $10\text{ dB}$ of path loss.

---
---

# Experiment 08: Study of Path Loss and Signal Attenuation in Indoor Wi-Fi Environment

### 1. Aim
To study and analyze **indoor radio path loss** and **signal attenuation** by measuring Wi-Fi **RSSI** under various physical obstacle conditions (open space, glass, wood, brick walls, and concrete).

---

### 2. Theory

#### 2.1 Indoor Radio Propagation Mechanisms
Unlike outdoor open environments, indoor radio wave propagation is dominated by four physical mechanisms:
1. **Reflection:** Radio waves bounce off surfaces large compared to the wavelength (e.g., walls, metal partitions).
2. **Diffraction:** Waves bend around sharp obstacle edges, enabling non-line-of-sight (NLOS) reception.
3. **Scattering:** Radio energy disperses in all directions from rough objects (e.g., furniture, foliage).
4. **Penetration / Transmission Loss:** RF energy is absorbed and attenuated as it passes through physical materials.

#### 2.2 Partition Path Loss Model
Indoor path loss is formulated by adding specific **Partition Attenuation Factors (PAF)** to the free space loss:
$$\text{PL}(d)\text{ [dB]} = \text{PL}_{\text{LOS}}(d) + \sum_{i} N_i \cdot \text{PAF}_i$$
Relative obstacle attenuation is calculated directly from measured RSSI:
$$\Delta\text{PL}_{\text{obstacle}}\text{ [dB]} = \text{RSSI}_{\text{Free Space (LOS)}} - \text{RSSI}_{\text{Obstacle}}$$

#### 2.3 Dielectric Properties and Typical Material Loss
- **Glass / Window:** Low attenuation ($2 - 4\text{ dB}$).
- **Hollow Wooden Door:** Moderate attenuation ($4 - 8\text{ dB}$).
- **Solid Brick Wall:** High attenuation ($10 - 15\text{ dB}$).
- **Reinforced Concrete Wall:** Very high attenuation ($15 - 25+\text{ dB}$).

---

### 3. Reading & Output

#### 3.1 Experimental Setup
- **Source:** Wi-Fi Access Point operating at $2.4\text{ GHz}$.
- **Fixed Measurement Distance:** Kept constant at **$d = 5\text{ meters}$** for all obstacle tests.
- **Instrument:** Smartphone running calibrated Wi-Fi Analyzer application.

#### 3.2 Observation Table 1: RSSI vs. Indoor Obstacles (Fixed Distance = 5 m)
| Sr. No. | Obstacle / Environmental Condition | Measurement Distance | Measured RSSI (dBm) | Signal Attenuation vs. Free Space (dB) | Signal Quality Observation |
|:---:|---|:---:|:---:|:---:|:---:|
| 1 | **Open Space (Line-of-Sight)** | 5 m | **-44 dBm** | **0 dB (Reference)** | Strong / Clean signal |
| 2 | **Glass Door / Window** | 5 m | **-48 dBm** | **4 dB** | Strong; minimal attenuation |
| 3 | **Wooden Door** | 5 m | **-52 dBm** | **8 dB** | Moderate signal |
| 4 | **Single Brick Wall** | 5 m | **-58 dBm** | **14 dB** | Moderate / Noticeable loss |
| 5 | **Two Interior Partition Walls** | 5 m | **-66 dBm** | **22 dB** | Weak signal |
| 6 | **Office Partition / Furniture** | 5 m | **-55 dBm** | **11 dB** | Moderate signal |

#### 3.3 Observation Table 2: RSSI vs. Distance in Open Space (LOS Reference)
| Sr. No. | Distance ($d$) | Measured RSSI (dBm) | Signal Quality Evaluation |
|:---:|:---:|:---:|:---:|
| 1 | **1 m** | **-38 dBm** | Very Strong / Excellent |
| 2 | **3 m** | **-46 dBm** | Strong |
| 3 | **5 m** | **-52 dBm** | Moderate |
| 4 | **7 m** | **-59 dBm** | Moderate |
| 5 | **10 m** | **-67 dBm** | Weak |

#### 3.4 Path Loss & Attenuation Analysis
- **Least Attenuating Obstacle:** Glass window ($4\text{ dB}$ loss). Glass has a low dielectric constant and thin profile, allowing most RF energy to transmit through.
- **Moderate Attenuating Obstacle:** Wooden door ($8\text{ dB}$ loss) and office cubicle partition ($11\text{ dB}$ loss).
- **Most Severe Attenuating Obstacle:** Single brick wall ($14\text{ dB}$ loss) and two walls ($22\text{ dB}$ loss). Dense masonry materials absorb electromagnetic energy and cause heavy multipath reflections.

---

### 4. Conclusion
The experiment demonstrated that indoor RF path loss is heavily dependent on both distance and the structural composition of obstacles. At a fixed distance of $5\text{ meters}$, signal strength degraded from **$-44\text{ dBm}$** in open space to **$-66\text{ dBm}$** behind two interior walls (a cumulative loss of $22\text{ dB}$). These empirical attenuation values are vital for RF site surveys and optimal Wi-Fi Access Point positioning in indoor buildings.

---
