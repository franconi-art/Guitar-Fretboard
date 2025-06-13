import streamlit as st
import pandas as pd

standard_tuning = ['E', 'B', 'G', 'D', 'A', 'E']
chromatic = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_at(string_note, fret):
    idx = chromatic.index(string_note)
    return chromatic[(idx + fret) % 12]

def generate_fretboard(tuning, frets=12):
    data = []
    for string in tuning[::-1]:
        row = [note_at(string, fret) for fret in range(frets + 1)]
        data.append(row)
    return pd.DataFrame(data, index=[f'Saite {i+1}' for i in range(6, 0, -1)])

st.title("🎸 Guitar Fretboard Tool")
frets = st.slider("Number of Frets", min_value=12, max_value=24, value=12)
fretboard = generate_fretboard(standard_tuning, frets)
st.dataframe(fretboard)
