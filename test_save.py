
from ursina import *
from notesection import NoteSection
from note import Note



NoteSection(
    x=0.0, y=0, scroll=0, octave=0,
    instrument='samples/0DefaultPiano_n48', attack=0, falloff=4,
    size=0.5, loops=4.0,
    notes=[Note(0.0, 0, 0.25, 1), Note(0.25, 2, 0.25, 1), Note(0.5, 4, 0.25, 1), Note(0.75, 6, 0.25, 1)],
    )

