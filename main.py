import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# --- Noten & Skalen ---
chromatic = ['C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B']

# Standard-Stimmung
standard_tuning = ['E', 'B', 'G', 'D', 'A', 'E']

# Skalen
scales = {
    "C Major": ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    "A Minor": ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    "G Major": ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    "E Minor": ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
    "Pentatonic C Major": ['C', 'D', 'E', 'G', 'A'],
    "Pentatonic A Minor": ['A', 'C', 'D', 'E', 'G']
}

# Stimmungen
tunings = {
    "Standard (E A D G B E)": ['E', 'B', 'G', 'D', 'A', 'E'],
    "Drop D (D A D G B E)": ['E', 'B', 'G', 'D', 'A', 'D'],
    "Open D (D A D F# A D)": ['D', 'A', 'F#', 'D', 'A', 'D'],
    "Open G (D G D G B D)": ['D', 'B', 'G', 'D', 'G', 'D'],
    "DADGAD": ['D', 'A', 'G', 'D', 'A', 'D']
}

# Beispiel-Akkorde
chords = {
    "C Major": ['C', 'E', 'G'],
    "A Minor": ['A', 'C', 'E'],
    "G Major": ['G', 'B', 'D'],
    "E Minor": ['E', 'G', 'B'],
    "D Major": ['D', 'F#', 'A']
}

# --- Funktionen ---
def note_at(string_note, fret):
    idx = chromatic.index(string_note)
    return chromatic[(idx + fret) % 12]

def generate_fretboard(tuning, frets=12):
    data = []
    for string in tuning[::-1]:
        row = [note_at(string, fret) for fret in range(frets + 1)]
        data.append(row)
    return data

def draw_fretboard(fretboard, selected_notes, frets, root_note, tuning):
    fig, ax = plt.subplots(figsize=(frets * 0.6, 3.5))
    ax.set_xlim(-0.5, frets + 0.5)
    ax.set_ylim(0.5, 6.5)
    ax.axis('off')
    ax.set_facecolor("#f1e2c6")

    # Saiten
    for string in range(1, 7):
        ax.hlines(string, -0.5, frets + 0.5, color="black", linewidth=1.5)

    # Bünde
    for fret in range(frets + 1):
        ax.vlines(fret, 0.5, 6.5, color="grey", linestyle="--" if fret > 0 else "-", linewidth=1)

    # Positionsmarker
    for marker in [3, 5, 7, 9, 12, 15, 17]:
        if marker <= frets:
            ax.text(marker, 0.3, "•", fontsize=14, ha="center", va="center", color="gray")

    # Notenpunkte
    for string_idx, string in enumerate(fretboard):
        for fret_idx, note in enumerate(string):
            if note in selected_notes:
                y = string_idx + 1
                color = "darkred" if note == root_note else "saddlebrown"
                ax.plot(fret_idx, y, 'o', color=color, markersize=14)
                ax.text(fret_idx, y, note, color="white", ha="center", va="center", fontsize=9, weight="bold")

    # Saitennamen links
    for i, note in enumerate(tuning[::-1]):
        ax.text(-1.2, i + 1, note, ha="right", va="center", fontsize=10, fontweight="bold")

    return fig

# --- UI ---
st.title("🎸 Guitar Fretboard Visualizer")

frets = st.slider("Number of Frets", min_value=12, max_value=24, value=12)
selected_tuning_name = st.selectbox("Tuning", list(tunings.keys()))
selected_tuning = tunings[selected_tuning_name]
fretboard_data = generate_fretboard(selected_tuning, frets)

# Modusauswahl
mode = st.radio("Display Mode", ["Scale", "Chord", "Custom Notes"])

if mode == "Scale":
    selected_scale = st.selectbox("Select a Scale", list(scales.keys()))
    selected_notes = scales[selected_scale]
    root_note = selected_notes[0]

elif mode == "Chord":
    selected_chord = st.selectbox("Select a Chord", list(chords.keys()))
    selected_notes = chords[selected_chord]
    root_note = selected_notes[0]

elif mode == "Custom Notes":
    selected_notes = st.multiselect("Select Notes", chromatic)
    root_note = selected_notes[0] if selected_notes else None

# Visualisierung
if selected_notes:
    fig = draw_fretboard(fretboard_data, selected_notes, frets, root_note, selected_tuning)
    st.pyplot(fig)

    # Export als PNG
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    st.download_button(
        label="📥 Download Fretboard as PNG",
        data=buffer.getvalue(),
        file_name="fretboard.png",
        mime="image/png"
    )
else:
    st.info("Please select at least one note to display.")
