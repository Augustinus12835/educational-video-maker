# Educational Video Maker

> Create professional educational videos from lecture notes using Claude Code, AI APIs, and simple tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-required-red.svg)](https://ffmpeg.org/)
[![Claude Code Powered](https://img.shields.io/badge/Claude%20Code-Powered-blueviolet)](https://claude.com/claude-code)

---

## 🎬 See the Final Product First

**Want to see what this system creates?**

👉 **[Watch the example video](example/Week-1/Video-1/final_video.mp4)** (3.5 minutes, 12.3 MB)

This video demonstrates:
- ✅ Hand-drawn Excalidraw slides with smooth transitions
- ✅ Natural AI narration (Australian English voice)
- ✅ Whisper-enhanced subtitles (perfectly synchronized)
- ✅ Professional educational content on "Risk vs Uncertainty"

**Created from:**
- Lecture notes: [`Week-1-Lecture-Notes-SAMPLE.pdf`](example/Week-1/Week-1-Lecture-Notes-SAMPLE.pdf)
- 12 hand-drawn frames (created in Excalidraw)
- Script written with Claude Code assistance
- Total production time: ~40 minutes

---

## 📑 Table of Contents

- [🎬 See the Final Product First](#-see-the-final-product-first)
- [What This System Does](#what-this-system-does)
- [Automated vs Manual vs Claude Code Assisted](#automated-vs-manual-vs-claude-code-assisted)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Test with Example](#test-with-example)
- [Complete Workflow (6 Steps)](#complete-workflow-6-steps)
  - [Step 1: Planning Videos](#step-1-planning-videos-claude-code---10-min)
  - [Step 2: Research Context](#step-2-research-context-claude-code---5-min)
  - [Step 3: Create Slides](#step-3-create-slides-manual---25-min)
  - [Step 4: Write Scripts](#step-4-write-scripts-claude-code---10-min)
  - [Step 5: Generate Audio](#step-5-generate-audio-automated---2-min)
  - [Step 6: Compile Video](#step-6-compile-video-automated---1-min)
- [Working with Claude Code](#working-with-claude-code)
  - [Why Claude Code?](#why-claude-code)
  - [Typical Interactions](#typical-interactions)
  - [Why This Approach Works](#why-this-approach-works)
- [Example Video Breakdown](#example-video-breakdown)
- [Scripts Provided](#scripts-provided)
- [Key Documentation Files](#key-documentation-files)
- [Customization](#customization)
- [Critical File Naming Rules](#critical-file-naming-rules)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Advanced Features](#advanced-features)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Support](#support)

---

## What This System Does

**Transforms:**
- Your lecture notes (PDF/PPTX)
- Your subject expertise

**Into:**
- Multiple rofessional concept videos per week
- Hand-drawn style slides with Excalidraw (you need to do this, which provides paedagogical guidance, LLM is bad at generating complex diagrams).
- Natural AI narration with Australian English voice (you can change it)
- Whisper-enhanced subtitles (perfect synchronization)
- Automated research context from web search to help you create Excalidraw slides.

**Time:** ~40 minutes per 5-minute video (mostly manual frame creation)
**Cost:** ~$0.05-0.10 per video (API usage, can be zero if not using the research api)

---

## Automated vs Manual vs Claude Code Assisted

### Fully Automated
- **TTS Audio Generation** - Murf API converts scripts to natural narration
- **Subtitle Creation** - Whisper provides word-level timing + AI correction aligns script text for perfect accuracy
- **Video Compilation** - FFmpeg assembles everything automatically

### Claude Code Assisted (You + AI Working Together)
- **Video Planning** - Claude Code parses lecture content and suggests video breakdown following `templates/plan_template.md`, you review and approve
- **Script Writing** - Claude Code writes scripts following `docs/teaching_style_guide.md`
- **Research Context** - Claude Code searches web using `docs/perplexity_instructions.md`
- **Image Ideas** - Claude Code suggests/generates images using `docs/image_fetching_spec.md`
- **Workflow Customization** - Claude Code adapts the system to your teaching style

### Manual Work (You)
- **Frame Creation** - Create hand-drawn slides in Excalidraw (~25 min per video)
- **Review & Edit** - Polish scripts, verify content accuracy

---

## Quick Start

### Prerequisites

**Required:**
- Python 3.8 or higher
- FFmpeg installed ([download here](https://ffmpeg.org/download.html))
- Claude Code ([download here](https://docs.claude.com/claude-code))
- API keys:
  - Perplexity API ([get key](https://www.perplexity.ai/settings/api))
  - Murf TTS API ([get key](https://murf.ai/api))

**Optional:**
- Gemini API (for AI-generated images) ([get key](https://aistudio.google.com/apikey))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/educational-video-maker
cd educational-video-maker

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env file and add your API keys
nano .env  # or use your preferred editor
```

### Test with Example Video

```bash
# Compile the example video (uses existing assets)
python scripts/compile_video.py example/Week-1/Video-1

# Watch the output
open example/Week-1/Video-1/final_video.mp4
```

**If successful, you'll see:**
- Video compiled successfully
- Duration: ~209 seconds
- Subtitles: 43 entries
- File size: ~12 MB

---

## Complete Workflow (6 Steps)

### Overview

```
Week N Lecture Content (PDF/PPTX)
          ↓
[1] Planning: Identify 8-10 concepts → plan.md (10 min, Claude Code - once per week)
          ↓
[2] Research: Web search for context → slide_context.md (5 min, Claude Code)
          ↓
[3] Slides: Create frames in Excalidraw → frame_*.png (25 min, Manual)
          ↓
[4] Scripts: Write narration with timing → script.md (10 min, Claude Code)
          ↓
[5] Audio: Generate TTS → audio/frame_*.mp3 (2 min, Automated)
          ↓
[6] Video: Compile final video → final_video.mp4 (1 min, Automated)
```

**Total time:** ~40 minutes per video (after initial planning)
- Step 1 done once per week for all videos (~10 min total)
- Per video: ~3 min automated + ~15 min Claude Code + ~25 min manual

---

### Step 1: Planning Videos (Claude Code - 10 min)

**What you do:**
```
"Claude, parse this weekly lecture content (PDF/PPTX) and describe
the concepts covered. Following templates/plan_template.md, group
concepts under common themes and suggest the number of concept videos
to make and the scope of each video.

Videos should be under 6 minutes each, with about 60 minutes total per
week (~10 videos). For each video, outline 2-3 main takeaways for students.

Save the plan as plan.md in the Week-N folder for my review."
```

**What Claude Code does:**
1. Reads and parses your lecture content (PDF/PPTX)
2. Identifies key concepts and groups them by common themes
3. Suggests video breakdown (titles, durations, scope)
4. Outlines 2-3 key takeaways per video
5. Creates `Week-N/plan.md` following the template structure

**Input:** Lecture PDF/PPTX for the week

**Output:** `Week-N/plan.md`

**Example plan structure:**
```markdown
## Video 1: Risk vs Uncertainty
**Duration:** 4 minutes
**Theme:** Understanding the Difference

### Content Scope:
- Define risk (known probabilities)
- Define uncertainty (unknown probabilities)
- Why the distinction matters

### Key Takeaways:
1. Risk is measurable, uncertainty is not
2. Different strategies required for each
3. Real-world examples: insurance vs black swans
```

**See template:** `templates/plan_template.md`

---

### Step 2: Research Context (Claude Code - 5 min)

**What you do:**
```
"Claude, I need to research context for a video about [topic].
Read docs/perplexity_instructions.md and help me gather quotes,
examples, and visual ideas."
```

**What Claude Code does:**
1. Reads `docs/perplexity_instructions.md` to understand research requirements
2. Crafts 4 targeted searches for your topic:
   - Famous quotes about the concept
   - Educational resources (videos, articles, tools)
   - Visual suggestions (diagrams to recreate)
   - Academic context and definitions
3. Retrieves and organizes content from the web
4. Creates `slide_context.md` with all research findings

**Example interaction:**
```
You: "Claude, research 'Risk vs Uncertainty' for a finance video.
      Use docs/perplexity_instructions.md."

Claude Code:
[Reads perplexity_instructions.md]
[Creates custom Perplexity searches]
[Retrieves quotes from Keynes, Taleb, Knight]
[Finds educational YouTube videos and articles]
[Suggests dice diagrams, black swan illustrations]
[Compiles everything into slide_context.md]

Done! I've created slide_context.md with:
- 5 famous quotes (Keynes, Taleb, Knight, Buffett, Rumsfeld)
- 3 educational resources (videos + articles)
- 8 visual suggestions (diagrams, graphs, examples)
- Academic definitions and context
```

**Output example (slide_context.md):**
```markdown
## Famous Quotes

> "Risk comes from not knowing what you're doing."
> — Warren Buffett

> "The world is divided into things we can predict and things we cannot."
> — Nassim Nicholas Taleb

## Educational Resources

1. **Risk vs Uncertainty Explained** (YouTube, 8 min)
   - Uses dice example for risk, pandemic for uncertainty
   - Clear visual demonstrations

2. **Knight's Uncertainty Framework** (Article)
   - Historical context of the distinction
   - Why it matters for finance

## Visual Suggestions

1. **Risk-Return Scatter Plot**
   - X-axis: Risk level, Y-axis: Expected return
   - Show known probabilities

2. **Black Swan Diagram**
   - Unexpected events outside normal predictions
   - Use swan illustration
```

**See full details:** [docs/perplexity_instructions.md](docs/perplexity_instructions.md)

---

### Step 3: Create Slides (Manual - 25 min)

Design multi-frame slides using Excalidraw for presentations.

**Getting Started:**
- Use [Excalidraw](https://excalidraw.com) (free, web-based)
- Learn about **[Excalidraw for Presentations](https://plus.excalidraw.com/use-cases/presentations)** - Create multi-frame presentations
- Hand-drawn aesthetic matches educational style perfectly

**Process:**
1. Open [Excalidraw](https://excalidraw.com)
2. Review `slide_context.md` for quotes, visuals, examples
3. Create frames using Excalidraw's frame feature (typically 10-12 frames per video)
4. Use hand-drawn style for consistency across all frames
5. Export each frame as PNG

**Export Process from Excalidraw:**

**⚠️ CRITICAL: macOS Users - Export to VSCode, NOT Finder**

1. **Maximize browser zoom:** Increase browser zoom as much as possible (Cmd + multiple times) for highest quality export
2. **Select frame:** Right-click on the frame border
3. **Select all elements:** Click "Select all elements in frame" from context menu
4. **Copy as PNG:** Select "Copy to clipboard as PNG" option
5. **Paste to VSCode:** Open VSCode Explorer and paste (Cmd+V)
   - ⚠️ **DO NOT paste to Finder on macOS** - This doesn't work correctly
   - ✅ Paste into VSCode file explorer, then move file to frames/ directory
6. **Rename immediately:** Rename to `frame_0.png`, `frame_1.png`, etc.
7. **Verify quality:** Check image resolution is 1920x1080 or higher
8. **Verify sequential numbering:** No gaps in numbering
9. **Move to correct location:** Place all frames in `Week-N/Video-M/frames/` directory

**Critical: File naming convention**
```
frames/
├── frame_0.png   # NOT frame_00.png (single digit, no padding)
├── frame_1.png   # NOT frame_01.png
├── frame_2.png
...
├── frame_11.png  # Double digits are fine
```

**Tips:**
- Include quotes, diagrams, examples from your `slide_context.md`
- Use consistent colors and style across all frames
- Keep text minimal - let narration do the explaining

---

### Step 4: Write Scripts (Claude Code - 10 min)

**What you do:**
```
"Claude, write a 4-minute script for [topic]. Use
docs/teaching_style_guide.md for style and slide_context.md
for content. I have 12 frames ready."
```

**What Claude Code does:**
1. Reads `docs/teaching_style_guide.md` to understand your pedagogical approach
2. Reviews `slide_context.md` for quotes, examples, and key concepts
3. Writes conversational, pedagogically-sound narration
4. Calculates proper timing (2.5 words per second)
5. Creates `script.md` with frame-by-frame narration

**Example interaction:**
```
You: "Claude, write a 4-minute script about Risk vs Uncertainty.
      Follow docs/teaching_style_guide.md and use slide_context.md.
      I have 12 frames."

Claude Code:
[Reads teaching_style_guide.md]
[Notes: conversational tone, first principles, use analogies]
[Reads slide_context.md]
[Finds: Keynes quote, dice example, Black Swan concept]
[Calculates: 4 min = 240s = ~600 words at 2.5 words/sec]
[Distributes content across 12 frames]
[Writes script with proper timing]

Done! I've created script.md with:
- Frame 0: Title introduction (15s, 38 words)
- Frames 1-3: Keynes quote reveal (30s, 75 words)
- Frames 4-5: Risk definition + dice example (30s, 75 words)
- Frames 6-7: Uncertainty definition + COVID example (30s, 75 words)
- Frames 8-9: Risk spectrum with examples (45s, 113 words)
- Frames 10-11: Black Swan + closing (60s, 150 words)
Total: 3:30, 526 words
```

**Output format (script.md):**
```markdown
## Frame 0 (0:00-0:15) • 38 words

Here we'll look at risk versus uncertainty. These terms aren't
interchangeable - they're fundamentally different.

---

## Frame 1 (0:15-0:30) • 38 words

John Maynard Keynes had important insights about uncertainty.
[Continue narration...]

---

## Frame 11 (3:00-4:00) • 150 words

[Final frame with closing summary integrated]
```

**Rules:**
- One narration per frame (NO combined frames like "Frame 1-2")
- Target: 2.5 words per second
- Word count: `duration_in_seconds × 2.5`
- Integrate closing into last frame (no separate closing section)

**See full details:** [docs/teaching_style_guide.md](docs/teaching_style_guide.md)

---

### Step 5: Generate Audio (Automated - 2 min)

Convert scripts to narration using Murf TTS API.

**Run:**
```bash
python scripts/generate_tts.py Week-N/Video-M/script.md
```

**What it does:**
- Reads `script.md` and extracts frame narration
- Calls Murf API for each frame
- Generates `audio/frame_0.mp3`, `frame_1.mp3`, etc.
- Verifies timing (target ±2 seconds)
- Reports any frames needing adjustment

**Voice settings:**
- Voice: `en-AU-leyton` (Australian male, professional)
- Style: Narration (clear, educational)
- Rate: -15 (slightly slower for comprehension)

**Example output:**
```
✓ frame_0.mp3: 14.3s (target: 15s) - OK
✓ frame_1.mp3: 9.8s (target: 10s) - OK
...
✓ frame_11.mp3: 58.7s (target: 60s) - OK

Summary: 12 frames generated successfully
Total duration: 3:56 (target: 4:00)
```

**See full details:** [docs/tts_specification.md](docs/tts_specification.md)

---

### Step 6: Compile Video (Automated - 1 min)

Combine frames, audio, and subtitles into final video with AI-corrected subtitles.

**Run:**
```bash
python scripts/compile_video.py Week-N/Video-M
```

**What it does:**

**Phase 1: Video Assembly**
1. Measures actual audio durations (not script estimates)
2. Builds FFmpeg filter graph with actual durations
3. Compiles video with:
   - 0.5s crossfade transitions between frames
   - Synchronized audio (no delays)
   - No subtitles yet (added in Phase 2)

**Phase 2: Subtitle Generation with Alignment Correction**
4. **Whisper transcription:** Transcribes compiled audio for word-level timestamps (~30-40s)
   - Whisper provides precise timing but may misspell technical terms or names (e.g., "Cain" instead of "Keynes")
5. **Alignment correction:** Aligns original script text to Whisper timestamps
   - **Script text** (accurate spelling) + **Whisper timestamps** (precise timing) = Perfect subtitles
   - **Alignment strategy:**
     - If word counts match → Direct 1:1 mapping (works perfectly)
     - If word counts differ → Proportional timing distribution (good enough)
   - Result: **Correct text + Precise timing**
6. Generates `subtitles.srt` with corrected text + Whisper's precise timing
7. Burns subtitles onto video

**If subtitles need manual correction:**
```
You can ask Claude Code to fix any issues:
"Claude, check the script and correct any subtitle errors in subtitles.srt,
then regenerate the video."
```

**Phase 3: Quality Verification**
8. Verifies output quality (duration, resolution, codecs)
9. Generates `compilation_report.txt`

**Output:**
- `final_video.mp4` - Complete video (H.264, 1080p, 30fps)
- `subtitles.srt` - Subtitle file (also burned into video)
- `compilation_report.txt` - Build verification

**Example output:**
```
Video Compilation Report
========================
✓ Script parsed: 12 frames
✓ Images found: 12 PNG files (1920x1080)
✓ Audio found: 12 MP3 files
✓ Subtitles created: 43 entries
✓ Video duration: 209s (matches actual audio: 208.9s)
✓ File size: 12.3 MB
✓ Quality: PASS

STATUS: ✓ COMPILATION SUCCESSFUL
```

**See full details:** [docs/video_compilation_spec.md](docs/video_compilation_spec.md)

---

## Working with Claude Code

### Why Claude Code?

This workflow is designed around Claude Code because it:
- **Reads documentation files** to understand your specific workflow
- **Maintains context** across the entire production process
- **Adapts to your style** by learning from your teaching guidelines
- **Handles both research and writing** seamlessly
- **Customizes on demand** - just ask it to modify any part

### Typical Interactions

**Planning Phase:**
```
You: "Claude, parse this Week 3 lecture PDF and create a plan.md.
      Follow templates/plan_template.md. Suggest 8-10 videos under
      6 minutes each, with ~60 minutes total."

Claude Code:
[Reads and parses Week-3-Lecture.pdf]
[Identifies 12 key concepts]
[Groups concepts by themes: foundations, applications, case studies]
[Proposes 9 videos with durations: 4-8 minutes each]
[Outlines 2-3 key takeaways per video]
[Creates Week-3/plan.md following template]

Done! Created plan.md with 9 videos:
- Video 1: Portfolio Theory Basics (5 min)
- Video 2: Efficient Frontier (6 min)
- Video 3: CAPM Introduction (7 min)
[... 6 more videos]
Total: 58 minutes
```

**Research Phase:**
```
You: "Claude, I need to create a video about portfolio diversification.
      Read docs/perplexity_instructions.md and help me research it."

Claude Code:
[Reads perplexity_instructions.md]
[Understands 4-search structure: quotes, resources, visuals, context]
[Creates custom searches for portfolio diversification]
[Retrieves famous quotes from Markowitz, Bogle, Swensen]
[Finds educational videos and academic papers]
[Suggests efficient frontier diagram, correlation matrix]
[Creates slide_context.md with all findings]

Done! Created slide_context.md with:
- 6 quotes (Markowitz, Bogle, Swensen, Buffett)
- 4 educational resources
- 10 visual suggestions
- Academic definitions and formulas
```

**Script Writing:**
```
You: "Claude, write a 5-minute script about portfolio diversification.
      Use docs/teaching_style_guide.md and slide_context.md.
      I have 10 frames."

Claude Code:
[Reads teaching_style_guide.md]
[Notes: conversational, first principles, use analogies, avoid jargon]
[Reads slide_context.md]
[Finds: Markowitz quote, efficient frontier, correlation examples]
[Calculates: 5 min = 300s = ~750 words at 2.5 words/sec]
[Plans content flow across 10 frames]
[Writes engaging, pedagogically-sound script]

Done! Created script.md with:
- Frame 0: Title (15s)
- Frames 1-2: Markowitz quote + concept intro (30s)
- Frames 3-5: Diversification mechanics (60s)
- Frames 6-8: Efficient frontier with examples (90s)
- Frames 9-10: Practical application + closing (105s)
Total: 5:00, 750 words
```

**Customization:**
```
You: "Claude, I want my teaching style to be more conversational
      and use more real-world examples. Update docs/teaching_style_guide.md."

Claude Code:
[Reads current teaching_style_guide.md]
[Understands existing guidelines]
[Modifies tone to be more conversational]
[Adds emphasis on real-world examples]
[Updates guidelines document]

Done! I've updated teaching_style_guide.md to:
- Use more conversational language ("Let's explore" vs "We will examine")
- Require 2-3 real-world examples per video (not just theoretical)
- Add storytelling elements (anecdotes, case studies)
- Reduce academic jargon by 30%

Would you like me to rewrite any existing scripts with this new style?
```

**Image Generation (Optional):**
```
You: "Claude, I need a hand-drawn diagram of the efficient frontier.
      Read docs/image_fetching_spec.md and create one."

Claude Code:
[Reads image_fetching_spec.md]
[Understands: use Gemini for diagrams, Perplexity for photos]
[Determines: efficient frontier = diagram → use Gemini]
[Creates custom generation script]
[Crafts prompt for hand-drawn style matching Excalidraw]
[Generates image via Gemini API]
[Saves to frames/ directory]

Done! Generated efficient_frontier_diagram.png:
- Hand-drawn style (matches your Excalidraw aesthetic)
- Clear axes labels (Risk/Return)
- Multiple portfolio points
- Efficient frontier curve highlighted
- 1920x1080 resolution
Ready to use in your video!
```

### Why This Approach Works

**Traditional Automation:**
- Scripts blindly execute commands
- No understanding of context
- Breaks when you need customization

**Claude Code Integration:**
- Reads your documentation to understand intent
- Adapts to your teaching style
- Handles edge cases intelligently
- Customizes workflow on demand

**Example of Adaptation:**
```
You: "Claude, this script uses too much jargon. Make it more accessible
      for undergraduate students."

Claude Code:
[Reads script.md]
[Identifies jargon: "stochastic volatility", "heteroskedasticity"]
[Reads teaching_style_guide.md for tone]
[Rewrites using simpler language and analogies]

Updated script.md:
- "stochastic volatility" → "unpredictable price swings"
- "heteroskedasticity" → "risk that changes over time"
- Added analogy: "Like weather - calm some days, stormy others"
```

---

## Example Video Breakdown

### Video 1: Risk vs Uncertainty

**Location:** `example/Week-1/Video-1/`

**Watch the video:** [example/Week-1/Video-1/final_video.mp4](example/Week-1/Video-1/final_video.mp4)

**Structure:**
```
Video-1/
├── slide_context.md          # Research context (quotes, examples, visuals)
├── script.md                 # Frame-by-frame narration (12 frames)
├── frames/                   # Exported Excalidraw frames
│   ├── frame_0.png          # Title: FIN101
│   ├── frame_1.png          # Keynes quote introduction
│   ├── frame_2.png          # Quote reveal
│   ├── frame_3.png          # Quote full text
│   ├── frame_4.png          # Risk definition
│   ├── frame_5.png          # Risk example (dice)
│   ├── frame_6.png          # Uncertainty definition
│   ├── frame_7.png          # Uncertainty example (COVID)
│   ├── frame_8.png          # Risk spectrum
│   ├── frame_9.png          # Spectrum with examples
│   ├── frame_10.png         # Black Swan explanation
│   └── frame_11.png         # Black Swan + closing
├── audio/                    # Generated TTS audio
│   ├── frame_0.mp3 (14.64s)
│   ├── frame_1.mp3 (7.91s)
│   └── ... (12 files, 208.9s total)
├── subtitles.srt             # Whisper-enhanced subtitles (43 entries)
├── final_video.mp4           # Complete video (209s, 12.3 MB)
└── compilation_report.txt    # Build verification
```

**Video details:**
- Duration: 3 minutes 29 seconds
- Resolution: 1920x1080 (Full HD)
- Frame rate: 30 fps
- Codec: H.264 (universal compatibility)
- Audio: AAC, 192 kbps
- Subtitles: Burned-in + separate SRT file
- File size: 12.3 MB

**Content flow:**
1. **Frame 0 (15s):** Title slide introduces topic
2. **Frames 1-3 (30s):** Progressive reveal of Keynes quote
3. **Frames 4-5 (30s):** Define risk + dice example
4. **Frames 6-7 (30s):** Define uncertainty + COVID example
5. **Frames 8-9 (45s):** Risk-uncertainty spectrum with examples
6. **Frames 10-11 (60s):** Black Swan events + closing summary

---

## Scripts Provided

### Core Production Scripts:

**`scripts/compile_video.py`**
- Assembles final video with Whisper-enhanced subtitles
- Synchronizes frames with actual audio durations
- Burns subtitles onto video
- Generates compilation report

**`scripts/generate_tts.py`**
- Converts scripts to narration audio
- Calls Murf API for each frame
- Verifies timing accuracy
- Reports frames needing adjustment

**`scripts/regenerate_frame_audio.py`**
- Fixes single corrupted or failed audio file
- Useful for API timeouts or quality issues

### Example Script (Reference Only):

**`scripts/generate_images_gemini.py`**
- Example of AI image generation for finance content
- This is specific to our finance videos
- Ask Claude Code to create your own version using `docs/image_fetching_spec.md`

---

## Key Documentation Files

When working with Claude Code, reference these files:

### For Script Writing:
**`docs/teaching_style_guide.md`**
- How to write engaging educational narration
- Pedagogical principles (first principles, analogies, examples)
- Tone and pacing guidelines
- Word count calculations

### For Research:
**`docs/perplexity_instructions.md`**
- How to research topics effectively
- 4-search strategy (quotes, resources, visuals, context)
- Output format requirements
- Quality guidelines

### For Images:
**`docs/image_fetching_spec.md`**
- AI-generated vs real photos
- Gemini prompting strategies
- Perplexity image search
- Hand-drawn style matching

### For Technical Details:
**`docs/workflow.md`**
- Complete 6-step workflow guide
- File naming conventions
- Quality checklists

**`docs/tts_specification.md`**
- TTS audio generation specs
- Voice settings and configuration
- Timing verification
- Troubleshooting

**`docs/video_compilation_spec.md`**
- Video assembly process
- Whisper subtitle generation
- FFmpeg filter graph
- Quality verification

---

## Customization

### Change Voice or Accent

Edit `.env`:
```bash
# Australian male (default)
MURF_VOICE_ID=en-AU-leyton

# US female
MURF_VOICE_ID=en-US-sarah

# British male
MURF_VOICE_ID=en-GB-oliver

# See all voices: https://murf.ai/voices
```

### Adjust Speaking Speed

Edit `.env`:
```bash
# Slower (better for complex concepts)
MURF_SPEAKING_RATE=-25

# Default (educational pace)
MURF_SPEAKING_RATE=-15

# Normal conversational
MURF_SPEAKING_RATE=0

# Faster (for reviews)
MURF_SPEAKING_RATE=+10
```

### Modify Teaching Style

Edit `docs/teaching_style_guide.md` or ask Claude Code:

```
"Claude, update my teaching style to be more [conversational/formal/enthusiastic].
Modify docs/teaching_style_guide.md accordingly."
```

Claude will adjust the guidelines and regenerate scripts following your new style.

### Use Different APIs

All API integrations are modular:

**Replace Perplexity:**
- Google Search API
- Bing Search API
- Custom web scraping

**Replace Murf:**
- ElevenLabs TTS
- OpenAI TTS
- Google Cloud TTS

**Replace Whisper:**
- AWS Transcribe
- Google Speech-to-Text
- Azure Speech Services

Just modify the relevant script file or ask Claude Code to do it.

---

## Critical File Naming Rules

**For video compilation to work, file naming must be exact:**

### Frame Images
```
frames/
├── frame_0.png   ✓ Correct
├── frame_1.png   ✓ Correct
├── frame_11.png  ✓ Correct

# ❌ WRONG - These will NOT work:
├── frame_00.png  ❌ No zero-padding
├── frame_01.png  ❌ No zero-padding
├── frame-0.png   ❌ Must use underscore
├── Frame_0.png   ❌ Must be lowercase
```

### Audio Files
```
audio/
├── frame_0.mp3   ✓ Must match frame numbers exactly
├── frame_1.mp3
└── frame_11.mp3
```

### Script Format
```markdown
## Frame 0 (0:00-0:15) • 38 words   ✓ Correct

## Frame 1-2 (0:15-0:30)             ❌ NO combined frames
## Closing (3:45-4:00)               ❌ NO separate closing section
```

**Why this matters:** The compilation script parses filenames to sync frames with audio. Incorrect naming breaks the automation.

---

## Troubleshooting

### Audio Generation Issues

**Problem:** `ModuleNotFoundError: No module named 'requests'`
```bash
pip install -r requirements.txt
```

**Problem:** Murf API returns 401 Unauthorized
```bash
# Check .env file has valid API key
cat .env | grep MURF_API_KEY
```

**Problem:** Audio files too fast/slow
```bash
# Adjust speaking rate in .env
MURF_SPEAKING_RATE=-20  # Slower
MURF_SPEAKING_RATE=-10  # Faster
```

### Video Compilation Issues

**Problem:** FFmpeg not found
```bash
# Install FFmpeg
# macOS:
brew install ffmpeg

# Linux:
sudo apt-get install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

**Problem:** Video compilation fails with "frame not found"
```bash
# Verify all frames exist
ls frames/frame_*.png

# Verify correct naming (frame_0.png not frame_00.png)
```

**Problem:** Subtitles out of sync
```bash
# Should not happen with Whisper timing
# If it does, try recompiling:
python scripts/compile_video.py Week-N/Video-M
```

### Excalidraw Export Quality

**Problem:** Exported frames are low quality/blurry
```bash
# Solution: Zoom browser BEFORE exporting
# 1. Zoom to 200%: Cmd/Ctrl + +
# 2. Export PNG
# 3. Result: Higher resolution (effectively 2x scale)
```

### Script Parsing Errors

**Problem:** TTS script parser not finding frames
```bash
# Check frame header format in script.md:
## Frame 0 (0:00-0:15) • 38 words   ✓ Correct format

# Common mistakes:
## Frame 00 (0:00-0:15)              ❌ No zero-padding
## Frame 1-2 (0:15-0:30)             ❌ No combined frames
## Closing (3:45-4:00)               ❌ NO separate sections
```

### Claude Code Integration

**Problem:** Claude Code doesn't understand my instructions

**Solution:** Point to specific documentation files:
```
"Claude, read docs/teaching_style_guide.md and docs/perplexity_instructions.md
before writing the script."
```

**Problem:** Script quality inconsistent

**Solution:** Update teaching style guide and ask Claude Code to review:
```
"Claude, read docs/teaching_style_guide.md. Does my latest script
follow these guidelines? Suggest improvements."
```

**See complete troubleshooting guide:** [docs/workflow.md#troubleshooting](docs/workflow.md)

---

## Project Structure

```
edu-vid-maker/
│
├── README.md                  # This file
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # How to contribute
├── .env.example               # API key template
├── requirements.txt           # Python dependencies
├── .gitignore                 # Exclude sensitive files
│
├── docs/                      # Documentation for Claude Code
│   ├── workflow.md            # Complete 6-step workflow guide
│   ├── teaching_style_guide.md    # Script writing guidelines
│   ├── perplexity_instructions.md # Research automation details
│   ├── tts_specification.md       # Audio generation specs
│   ├── video_compilation_spec.md  # Video assembly process
│   └── image_fetching_spec.md     # Optional: AI image generation
│
├── scripts/                   # Automation scripts
│   ├── compile_video.py              # Video compilation
│   ├── generate_tts.py               # Audio generation
│   ├── regenerate_frame_audio.py     # Fix single audio file
│   └── generate_images_gemini.py     # Example: AI image generation
│
├── example/                   # Working demonstration
│   └── Week-1/
│       ├── Week-1-Lecture-Notes-SAMPLE.pdf   # Sample lecture content
│       └── Video-1/                  # Complete working example
│           ├── slide_context.md      # Research context
│           ├── script.md             # Narration script
│           ├── frames/               # 12 frame images (1920x1080)
│           ├── audio/                # 12 TTS audio files
│           ├── subtitles.srt         # Generated subtitles
│           ├── final_video.mp4       # Complete video (12.3 MB)
│           └── compilation_report.txt # Build verification
│
└── templates/                 # Starting templates
    ├── plan_template.md       # Video planning template
    └── script_template.md     # Script writing template
```

---

## Advanced Features

### Batch Processing Multiple Videos

```bash
# Generate audio for all videos
for i in {1..10}; do
  python scripts/generate_tts.py Week-1/Video-$i/script.md
done

# Compile all videos
for i in {1..10}; do
  python scripts/compile_video.py Week-1/Video-$i
done
```

### Optional: AI-Generated Images

Use Gemini API to generate hand-drawn style images or search real photos with Perplexity.

**See:** [docs/image_fetching_spec.md](docs/image_fetching_spec.md)

Features:
- Gemini: Generate diagrams, icons, conceptual illustrations
- Perplexity: Find real photos of people, logos, buildings
- Automatic attribution tracking
- Matches Excalidraw hand-drawn style

### Video Quality Settings

Edit `scripts/compile_video.py`:

```python
VIDEO_CRF = 23        # Quality (18=high, 28=low)
VIDEO_PRESET = "medium"  # Speed (ultrafast/fast/medium/slow/veryslow)
VIDEO_FPS = 30        # Frame rate
```

**Trade-offs:**
- Lower CRF = better quality, larger files
- Slower preset = better compression, longer compile time
- Higher FPS = smoother (unnecessary for static slides)

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

**Areas needing help:**
- Additional language support (TTS voices)
- Alternative API integrations (ElevenLabs, etc.)
- More example videos in different subjects
- Documentation improvements
- Bug fixes and optimizations

---

## License

MIT License - See [LICENSE](LICENSE) for details.

**Summary:** Use freely for educational purposes, commercial or non-commercial.

---

## Acknowledgments

Built with these excellent tools:

- **Claude Code** (Anthropic) - AI-powered workflow automation and script generation
- **Perplexity API** - Research and web search automation
- **Murf.ai** - Professional text-to-speech narration
- **Whisper** (OpenAI) - Word-level subtitle generation
- **FFmpeg** - Video processing and compilation
- **Excalidraw** - Hand-drawn style slide design

---

## Support

- **Issues:** Report bugs or request features on GitHub Issues
- **Discussions:** Ask questions or share ideas on GitHub Discussions
- **Documentation:** Check `docs/` folder for detailed guides
- **Claude Code Help:** Ask Claude to read relevant docs and assist

---

## Project Stats

**Status:** Production-ready
**Used for:** Finance education (130+ videos created)
**Average video quality:** 1080p HD, professional narration, perfect subtitle sync
**Time savings:** ~90% reduction vs traditional video production
**Cost savings:** ~$130,000 per semester vs professional production

---

**Last Updated:** November 2024
**Version:** 1.0.0
**Powered by:** Claude Code (Sonnet 4.5)
