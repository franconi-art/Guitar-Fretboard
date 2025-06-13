import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

chromatic = ['C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B']

interval_map = {
    0: "1", 1: "b2", 2: "2", 3: "b3", 4: "3",
    5: "4", 6: "b5", 7: "5", 8: "#5", 9: "6",
    10: "b7", 11: "7"
}

scales = {
    "C Major": ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    "A Minor": ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    "G Major": ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    "E Minor": ['E', 'F#', 'G', 'A', 'B', 'C', 'D']
}

tunings = {
    "Standard (E A D G B E)": ['E', 'B', 'G', 'D', 'A', 'E']
}

def note_at(note, fret):
    idx = chromatic.index(note)
    return chromatic[(idx + fret) % 12]

def interval_label(root, note):
    root_idx = chromatic.index(root)
    note_idx = chromatic.index(note)
    diff = (note_idx - root_idx) % 12
    return interval_map.get(diff, "")

def generate_fretboard(tuning, start_fret, end_fret):
    return [[note_at(note, fret) for fret in range(start_fret, end_fret + 1)] for note in tuning[::-1]]

def draw_fretboard(ax, fretboard, selected_notes, root_note, tuning, start_fret, label_mode, title=""):
    frets = len(fretboard[0])
    ax.set_xlim(-0.5, frets - 0.5)
    ax.set_ylim(0.5, 6.5)
    ax.axis('off')
    ax.set_facecolor("#f1e2c6")

    for s in range(6):
        ax.hlines(s + 1, -0.5, frets - 0.5, color="black", linewidth=1.5)
    for f in range(frets + 1):
        ax.vlines(f - 0.5, 0.5, 6.5, color="grey", linestyle="--", linewidth=1)

    for m in [3, 5, 7, 9, 12]:
        x = m - start_fret
        if 0 <= x < frets:
            ax.text(x, 0.3, "•", fontsize=14, ha="center", va="center", color="gray")

    for s_idx, string in enumerate(fretboard):
        for f_idx, note in enumerate(string):
            if note in selected_notes:
                x, y = f_idx, s_idx + 1
                if label_mode == "Note":
                    label = note
                elif label_mode == "Interval":
                    label = interval_label(root_note, note)
                else:
                    label = ""
                color = "darkred" if note == root_note else "saddlebrown"
                ax.plot(x, y, 'o', color=color, markersize=14)
                ax.text(x, y, label, color="white", ha="center", va="center", fontsize=9, weight="bold")

    for i, note in enumerate(tuning[::-1]):
        ax.text(-1.2, i + 1, note, ha="right", va="center", fontsize=10, fontweight="bold")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)

# Streamlit UI
st.title("🎸 Fretboard Comparison View")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Left Fretboard")
    tuning_left = tunings["Standard (E A D G B E)"]
    scale_left = st.selectbox("Scale (Left)", list(scales.keys()), key="scale_left")
    start_fret_left = st.slider("Start Fret (Left)", 0, 12, 0, key="start_left")
    end_fret_left = st.slider("End Fret (Left)", start_fret_left + 1, 24, start_fret_left + 11, key="end_left")
    label_mode_left = st.radio("Labels (Left)", ["Note", "Interval", "None"], key="label_left")
    notes_left = scales[scale_left]
    root_left = notes_left[0]
    fretboard_left = generate_fretboard(tuning_left, start_fret_left, end_fret_left)

with col2:
    st.subheader("Right Fretboard")
    tuning_right = tunings["Standard (E A D G B E)"]
    scale_right = st.selectbox("Scale (Right)", list(scales.keys()), index=1, key="scale_right")
    start_fret_right = st.slider("Start Fret (Right)", 0, 12, 0, key="start_right")
    end_fret_right = st.slider("End Fret (Right)", start_fret_right + 1, 24, start_fret_right + 11, key="end_right")
    label_mode_right = st.radio("Labels (Right)", ["Note", "Interval", "None"], key="label_right")
    notes_right = scales[scale_right]
    root_right = notes_right[0]
    fretboard_right = generate_fretboard(tuning_right, start_fret_right, end_fret_right)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
draw_fretboard(ax1, fretboard_left, notes_left, root_left, tuning_left, start_fret_left, label_mode_left, title=scale_left)
draw_fretboard(ax2, fretboard_right, notes_right, root_right, tuning_right, start_fret_right, label_mode_right, title=scale_right)
st.pyplot(fig)
update: Vergleichsansicht
