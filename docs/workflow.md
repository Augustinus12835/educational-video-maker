# Course concept video making

## Project Overview

**Goal:** Produce 8-10 educational finance videos per week for university students. Claude Code will help me plan the concept videos and gather academic sources and materials using perplexity to plan the concept videos. The user will create multi-frame Excalidraw for each concept video and export all frames. Claude code will help me to write script with Frame Timing, then murf is used to generate TTS Audio and compile videos.

## Weekly Workflow

1. **Concept Video Planning**

Parse weekly lecture content (pptx or pdf) and describe concepts covered in each week. Group concepts under common theme, and suggest the number of the concept videos to make and the scope of each concept video. The length of the video should be under 6 mins and we should have about 60 mins of videos each week (10 videos). For each video, outline the key points: Decide on the 2-3 main takeaways for the students. Prepare a md document saved as plan.md in the same week (e.g. Week-1 folder) for your recommendation for the user to examine.

Example:

---

## **Video 5: Credit Risk - The Risk of Counterparty Failure**
**Duration:** 6 minutes
**Theme:** Major Types of Financial Risks

### Content Scope:
- Default risk
- Bankruptcy risk
- Credit downgrade risk
- Settlement risk

### Key Takeaways:
1. **Credit risk is counterparty-focused:** The risk that a borrower, issuer, or counterparty fails to meet their financial obligations
2. **Multiple dimensions of credit risk:** Credit risk manifests not just as default, but also as downgrades and settlement failures, each requiring different management approaches

---

2. **Perplexity Research**

Once plan.md is reviewed by the user, create folder for each video under the week number (e.g. teaching/FIN101/Week-1) for each video (e.g. Week-1/Video-1/)

For each concept video in plan.md, use perplexity api (availble in project root .env) to prepare the context output:Week-{N}/Video-{M}/slide_context.md.

Please follow the detailed instructions in teaching/FIN101/perplexity_slide_context_instructions.md.


3. **Excalidraw slides to scripts**

**Frame File Naming (CRITICAL):**
- Export Excalidraw frames as PNG images
- Rename files to: `frame_0.png`, `frame_1.png`, `frame_2.png`, etc.
- Frame numbers start at 0 (not 1)
- Use underscore `_` not hyphen or space
- Single digit: `frame_0.png` NOT `frame_00.png`
- Save all frames to: `Week-N/Video-M/frames/`

**Script Creation Requirements:**

Follow teaching_style_guide.md to create narration script.

**CRITICAL RULES:**
1. **One narration per frame** - NO combined frames (e.g., NO "Frame 1-2")
2. **No separate closing section** - integrate closing into last frame
3. **Frame header format:**
   ```
   ## Frame N (MM:SS-MM:SS) • NN words

   [Narration text]
   ```
4. **Word count target:** 2.5 words/second (e.g., 15s → 38 words)

**Script location:** Save to `Week-N/Video-M/script.md`

**Example structure:**
```markdown
## Frame 0 (0:00-0:15) • 38 words

[Introduction narration]

---

## Frame 1 (0:15-0:25) • 25 words

[First content narration]

---

## Frame 11 (3:00-4:00) • 150 words

[Final content + closing summary integrated]
```

4. **Use Murf to create per frame audio**
I need you to automate TTS generation using Murf API for my educational videos.

**Context:**
- Input: script.md in teaching/FIN101/Week-1/Video-1/script.md with frame-by-frame narration
- Output: Individual MP3 files for each frame (frame_0.mp3, frame_1.mp3, etc.) in teaching/FIN101/Week-1/Video-1/audio
- Frame naming: Matches PNG files (frame_0, frame_1, NOT frame_00, frame_01)
- Target: 2.5 words/second speaking rate
- API Key: In .env file as MURF_API_KEY

**Task:**
Create a Python script that:
1. Parses script.md to extract frame narration text
2. Calls Murf API for each frame
3. Generates MP3 files with correct timing
4. Verifies output matches target duration
5. Reports any timing discrepancies

**Murf API Configuration:**
```python
# API Settings
MURF_API_ENDPOINT = "https://api.murf.ai/v1/speech/generate-audio"
VOICE_ID = "en-AU-marcus"  # Australian male, professional
SPEAKING_RATE = 0.85       # Slower than default for natural pacing
OUTPUT_FORMAT = "mp3"
AUDIO_QUALITY = "high"     # 192 kbps

# Frame extraction pattern
# Each frame in script.md follows this format:
# ## Frame X (MM:SS-MM:SS) • NN words
# [narration text]
```

**Expected Behavior:**

Input (script.md):
```markdown
## Frame 0 (0:00-0:15) • 38 words

Here we'll look at risk versus uncertainty. These terms aren't interchangeable - 
they're fundamentally different. The left shows a probability distribution - 
that's risk. The right shows a black swan - that's uncertainty.
```

Output:
- File: audio/frame_0.mp3
- Duration: ~15 seconds
- Quality: Clear, natural speech at 2.5 w/s

**Key Requirements:**

1. **Parse script.md accurately:**
   - Extract frame number
   - Extract target duration (from timing)
   - Extract narration text only (remove formatting, bullets, headers)

2. **Call Murf API with settings:**
   - Voice: en-AU-marcus (or equivalent Australian professional voice)
   - Speed: 0.85x (to hit 2.5 words/second)
   - Format: MP3, 192 kbps
   - Include proper error handling

3. **Save outputs organized:**
```
   Week-X/Video-Y/
   ├── audio/
   │   ├── frame_0.mp3
   │   ├── frame_1.mp3
   │   ├── frame_2.mp3
   │   └── ...
   ├── frames/
   │   ├── frame_0.png
   │   ├── frame_1.png
   │   └── ...
   └── script.md
```

4. **Verify timing:**
   - After generation, check each MP3 duration
   - Compare to target from script.md
   - Report frames that are >2 seconds off target
   - Suggest speed adjustment if needed

5. **Handle errors gracefully:**
   - API failures: Retry 3 times with backoff
   - Rate limits: Wait and retry
   - Invalid responses: Log and continue with next frame
   - Missing API key: Clear error message

**Output Report Format:**
```
TTS Generation Complete
=======================

✓ frame_0.mp3: 15.2s (target: 15s) - OK
✓ frame_1.mp3: 10.1s (target: 10s) - OK
⚠ frame_5.mp3: 16.8s (target: 20s) - 3.2s short - consider speed 0.80x
✓ frame_6.mp3: 15.3s (target: 15s) - OK
...

Summary:
- Total frames: 12
- Successful: 11
- Need adjustment: 1
- Failed: 0
- Total audio duration: 3:58 (target: 4:00)

Next step: Review frame_05, then run video compilation
```

**File to create:** `generate_tts.py` in teaching/FIN101/scripts

**Usage:** `python generate_tts.py Week-2/Video-1/script.md`

Please implement this with proper error handling and timing verification.