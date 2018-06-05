from pandaeditor import *
import scalechanger
import notesheet
from notesection import NoteSection

class Keyboard(Entity):

    def __init__(self):
        super().__init__()
        allkeys = 'zxcvbnmasdfghjklqwertyuiop1234567890'
        self.keys = [char for char in allkeys]
        print(scalechanger.scale)
        self.octave_offset = 0

        self.note_names = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B","C", "C#")
        # self.instantiate_note_overlays()
        # self.update_note_names()
        self.parent = camera.ui
        self.scale *= .025
        self.position = (-.5 * camera.aspect_ratio, -.5)


    def input(self, key):
        for i, k in enumerate(self.keys):
            if key == k:
                note_num = i + (self.octave_offset * len(scalechanger.scale))
                note_num = scalechanger.note_offset(note_num)

                if base.notesheet.prev_selected:
                    base.notesheet.prev_selected.play_note(note_num)
                    if i < len(self.children):
                        self.children[i].color = color.lime

            if key == k + ' up':
                print('stop:', i)
                # instrumentChanger.StopPlayingNote(i + (octaveOffset * octaveLength))
                if i < len(self.children):
                    self.children[i].color = self.children[i].unpressed_color

        if key == ',':
            print('noteoffset -')
            self.octave_offset -= 1
            self.octave_offset = max(self.octave_offset, -2)

        if key == '.':
            print('noteoffset +')
            self.octave_offset += 1
            self.octave_offset = min(self.octave_offset, 5)


    def instantiate_note_overlays(self):
        for i in range(128):
            nb = Button()
            nb.parent = self
            nb.scale_y = 1.5
            nb.x = i
            nb.text = 'N'
            nb.text_entity.y = -.25
            nb.origin = (-.5, -.5)


    def update_note_names(self):
        for i, child in enumerate(self.children):
            if i % len(scalechanger.scale) == 0:
                child.color = color.black66 * .8
            else:
                child.color = color.black66

            child.unpressed_color = child.color
            child.text = self.note_names[scalechanger.note_offset(i, True)] + str(i // len(scalechanger.scale))


if __name__ == '__main__':
    app = PandaEditor()
    kb = Keyboard()
    app.run()

    #                 instrumentChanger.PlayNote(i + (octaveOffset * octaveLength), Random.Range(0.8f, 0.9f))
    #                 overlays[i + (octaveOffset * octaveLength)].SetActive(true)
    #                 if musicScore.recording and musicScore.playing:
    #                     musicScore.currentNoteSection.StartNote(i + (octaveOffset * octaveLength), 1f)
    #
    #             if Input.GetKeyUp(keys[i]):
    #                 instrumentChanger.StopPlayingNote(i + (octaveOffset * octaveLength))
    #                 overlays[i + (octaveOffset * octaveLength)].SetActive(false)
    #                 if musicScore.recording and musicScore.playing:
    #                     musicScore.currentNoteSection.StopNote(i + (octaveOffset * octaveLength))
    #
    #     if usingMidiKeyboard == true:
    #         for k in range(128):
    #             if MidiMaster.GetKeyDown(k):
    #                 /*rand = Random.Range(-1f, 1f)
    #                 print(rand)*/
    #                 instrumentChanger.PlayNote(k,MidiMaster.GetKey(k))
    #                 /*if rand > 0f:
    #                     instrumentChanger.PlayNote(k+2,MidiMaster.GetKey(k))
    #                 else:
    #                     instrumentChanger.PlayNote(k+3,MidiMaster.GetKey(k))*/
    #
    #                 overlays[k].SetActive(true)
    #                 overlays1[k].SetActive(true)
    #                 if musicScore.recording and musicScore.playing:
    #                     musicScore.currentNoteSection.StartNote(k,MidiMaster.GetKey(k))
    #
    #             if MidiMaster.GetKeyUp(k):
    #                 instrumentChanger.StopPlayingNote(k)
    #                 if rand > 0:
    #                     instrumentChanger.StopPlayingNote(k+2)
    #                 else:
    #                     instrumentChanger.StopPlayingNote(k+3)
    #
    #                 if musicScore.recording and musicScore.playing:
    #                     musicScore.currentNoteSection.StopNote(k)
    #                 overlays[k].SetActive(false)
    #                 overlays1[k].SetActive(false)
    #
    #
    #         if MidiMaster.GetKnob(7, 0f) != lastVolumeKnob:
    #             lastVolumeKnob = MidiMaster.GetKnob(7, 0f)
    #             instrumentChanger.currentInstrument.dynamicVolumeSlider.value = lastVolumeKnob
    #
    #
    # public def InstantiateNoteOverlays():
    #     overlays = array(GameObject, 128)
    #     overlays1 = array(GameObject, 128)
    #
    #     for i in range(128):
    #         overlayElement = Instantiate(noteOverlay)
    #         overlayElement.transform.SetParent(pianoRoll, false)
    #         overlayElement.transform.localPosition = Vector2(0, i)
    #         rectTransform as RectTransform = overlayElement.GetComponent(RectTransform)
    #         rectTransform.anchorMin = Vector2(0f, 0f)
    #         rectTransform.anchorMax = Vector2(1f, 0f)
    #         overlays[i] = overlayElement.transform.GetChild(0).gameObject
    #
    #         //overlays inside note section
    #         overlayElement1 = Instantiate(noteOverlay1)
    #         overlayElement1.transform.SetParent(noteOverlayInsideNoteSection, false)
    #         overlayElement1.gameObject.SetActive(false)
    #         # rectTransform = overlayElement1.AddComponent(RectTransform)
    #         # rectTransform.anchorMin = Vector2(0f, 0f)
    #         # rectTransform.anchorMax = Vector2(1f, 0f)
    #
    #         overlayElement1.transform.localPosition = Vector2(0, i)
    #         overlays1[i] = overlayElement1
    #
    # public def UpdateNoteNames():
    #     scaleChanger = Amvol.GetScaleChanger()
    #     scaleLength as int = scaleChanger.GetScaleLength()
    #
    #     for i in range(overlays.Length):
    #         # print(scaleChanger.NoteOffset(i - scaleChanger.noteOffset, true) +" / ")
    #
    #         if i % scaleLength == 0:
    #             overlays[i].SetActive(true)
    #             overlays[i].GetComponent(Image).color = Color(1,1,1,0.05)
    #         else:
    #             overlays[i].SetActive(false)
    #             overlays[i].GetComponent(Image).color = Color(0.3, 0.5, 0.7, 0.5)
    #         overlays[i].transform.parent.GetChild(1).GetComponent(Text).text = noteNames[scaleChanger.NoteOffset(i, true)] + (i/scaleLength).ToString()
