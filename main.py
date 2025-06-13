import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Daten für Noten und Skalen ---
chromatic = ['C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B']

# Standard-Stimmung EADGBE
standard_tuning = ['E', 'B', 'G', 'D', 'A', 'E']

# Gängige Skalen
scales = {
    "C Major": ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    "A Minor": ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    "G Major": ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    "E Minor": ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
    "A Major": ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    "E Major": ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    "Pentatonic C Major": ['C', 'D', 'E', 'G', 'A'],
    "Pentatonic A Minor": ['A', 'C', 'D', 'E', 'G']
}

# --- Funktionen ---
def note_at(string_note, fret):
    idx = chromatic.index(string_note)
    return chromatic[(idx + fret) % 12]

def generate_fretboard(tuning, frets=12):
    data = []
    for string in tuning[::-1]:  # tiefste Saite zuerst
        row = [note_at(string, fret) for fret in range(frets + 1)]
        data.append(row)
    return data

def draw_fretboard(fretboard, scale_notes, frets):
    fig, ax = plt.subplots(figsize=(frets * 0.6, 4))
    ax.set_xlim(0, frets)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Hintergrund wie helles Griffbrett
    ax.set_facecolor("#f1e2c6")

    for string in range(6):
        ax.hlines(string + 0.5, 0, frets, color="black", linewidth=1)

    for fret in range(frets + 1):
        ax.vlines(fret, 0.5, 6.5, color="grey", linestyle="--" if fret > 0 else "-", linewidth=1)

    for string_idx, string in enumerate(fretboard):
        for fret_idx, note in enumerate(string):
            if note in scale_notes:
                ax.plot(fret_idx, string_idx + 0.5, 'o', color="saddlebrown", markersize=14)
                ax.text(fret_idx, string_idx + 0.5, note,
                        color="white", ha="center", va="center", fontsize=9, weight="bold")
    st.pyplot(fig)

# --- Streamlit Interface ---
st.title("🎸 Guitar Fretboard Visualizer")

frets = st.slider("Number of Frets", min_value=12, max_value=24, value=12)
selected_scale = st.selectbox("Select a Scale", list(scales.keys()))

fretboard_data = generate_fretboard(standard_tuning, frets)
draw_fretboard(fretboard_data, scales[selected_scale], frets)
