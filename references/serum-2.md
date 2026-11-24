# Serum 2 one-shot export

Use the drag-audio control beside the Serum 2 logo when the instance is available. It renders the last played note with the same pitch, velocity and duration. Alt-click the control to open the render folder. UI labels and storage can vary by build. [Xfer's guide](https://xferrecords.com/web-manual/serum-2/dragging-audio-to-your-daw)

1. Save the final patch and load it in the test instance. Use a MIDI note with known number and velocity. Start with C in the intended register. Hold it long enough for the intended one-shot, or match the release behavior being tested.
2. Play the note, then drag the audio control to an authorized destination. Use an isolated test when the drop would add a clip to an existing production project.
3. Find the new WAV, verify its creation time and patch name, and inspect its pitch and audible tail before comparing. If drag export is unavailable, use a render from the same Serum instance in the DAW.
4. Associate the render with the preset by filename or in the report. Check for the preset in the browser when it was copied into a bank. Use **Rescan Database** for a stale index when access to the instance is authorized.
