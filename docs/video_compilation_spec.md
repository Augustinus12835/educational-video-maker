# Video Compilation Specification
## Automated Video Assembly with Transitions and Subtitles (Whisper-Enhanced)

---

## Overview

**Input Files:**

In each video folder (e.g. teaching/FIN101/Week-1/Video-1)
- `script.md` - Frame timing estimates and narration text (ground truth)
- `frames/frame_*.png` - Frame images (1920x1080), numbered 0-11
- `audio/frame_*.mp3` - Generated TTS audio files, numbered 0-11

**File Naming Convention:**
- Frames: `frame_0.png`, `frame_1.png`, ..., `frame_11.png` (no zero-padding)
- Audio: `frame_0.mp3`, `frame_1.mp3`, ..., `frame_11.mp3` (matches frame numbers)
- Sequential numbering with no gaps
- Each frame has exactly one matching audio file

**Output:**
- `final_video.mp4` - Complete video with transitions and burned-in subtitles
- `subtitles.srt` - Subtitle file with corrected text and Whisper timestamps
- `compilation_report.txt` - Verification report

**Processing Tools:**
- FFmpeg (primary video processing)
- Whisper (word-level timestamp generation)
- Python (orchestration and subtitle alignment)

---

## Corrected Workflow Overview

### **Key Principles**

1. **Use Actual Audio Durations** - Not script estimates
2. **Synchronize Frames and Audio** - Start/end simultaneously, no delays
3. **Generate Subtitles After Video Structure** - Ensures perfect sync
4. **Correct Whisper Transcription** - Use script text, preserve Whisper timing

### **Workflow Steps**

```
Step 1: Parse script.md (timing estimates + ground truth text)
Step 2: Measure actual audio durations → Calculate actual frame times
Step 3: Transcribe audio with Whisper → Get word-level timestamps
Step 4: Align script text to Whisper timestamps → Correct transcription errors
Step 5: Generate subtitles → Corrected text + Whisper timing
Step 6: Build FFmpeg command → Use actual durations, no delays
Step 7: Compile video → Frames sync with audio
Step 8: Verify output → Check duration, resolution, quality
```

---

## Task 1: Generate Subtitle File with Whisper Alignment

### **Subtitle Format (SRT)**

```srt
1
00:00:00,000 --> 00:00:04,733
Here we'll look at risk versus
uncertainty. These terms aren't

2
00:00:04,303 --> 00:00:09,036
interchangeable - they're fundamentally
different. The left shows a probability

3
00:00:08,606 --> 00:00:14,199
distribution - that's risk. The right
shows a black swan - that's uncertainty.
```

### **Subtitle Requirements**

**Timing:**
- Word-level timestamps from Whisper STT
- Split long sentences for readability (max 2 lines per subtitle)
- Max 42 characters per line
- Min 1 second display time per subtitle
- Perfect sync with actual speech

**Text Content:**
- Use actual script.md text (ground truth)
- Corrects Whisper transcription errors (e.g., "Cain" → "Keynes")
- Preserves Whisper's precise timing

**Formatting:**
- Max 2 lines visible at once
- Font: Arial, size 18 (readable, not intrusive)
- Positioned near bottom (MarginV=50)
- Semi-transparent black background for readability

**Text Processing:**
- Align script words to Whisper timestamps
- Proper sentence splitting at natural pauses
- Keep punctuation for readability

---

### **Implementation: Whisper-Enhanced Subtitle Generation**

```python
"""
Generate SRT subtitle file with Whisper timestamps and corrected text

Workflow:
1. Transcribe audio with Whisper → Get word-level timestamps
2. Align script text to Whisper timestamps → Correct transcription errors
3. Group words into subtitle chunks → Max 42 chars/line, 2 lines max
4. Generate SRT format with corrected text + Whisper timing
5. Save as subtitles.srt

Key functions:
- transcribe_audio_with_whisper() - Get word-level timestamps from audio
- align_script_to_whisper_timestamps() - Map script text to Whisper timing
- generate_subtitles_from_corrected_timestamps() - Create SRT with corrections
"""
```

**Critical: Whisper Transcription Correction**

```python
def align_script_to_whisper_timestamps(script_text: str, whisper_result: Dict) -> List[Dict]:
    """
    Align actual script text with Whisper word timestamps

    This corrects Whisper transcription errors (e.g., "Cain" -> "Keynes")
    while preserving precise timing information.

    Example:
    - Whisper says: "Cain said..." at timestamp 00:00:25,699
    - Script says: "Keynes said..."
    - Output: "Keynes said..." at timestamp 00:00:25,699 ✓

    Returns:
        List of word dictionaries with corrected text and preserved timestamps
    """
    # Extract Whisper words with timestamps
    whisper_words = []
    for segment in whisper_result.get('segments', []):
        if 'words' in segment:
            whisper_words.extend(segment['words'])

    # Clean and tokenize script text (ground truth)
    script_words = script_text.replace('\n', ' ').split()

    # Align: If word counts match, direct 1:1 mapping
    # Otherwise: Proportional time distribution
    aligned_words = []

    if len(script_words) == len(whisper_words):
        for script_word, whisper_word in zip(script_words, whisper_words):
            aligned_words.append({
                'word': script_word,  # ← Correct text from script
                'start': whisper_word['start'],  # ← Precise timing from Whisper
                'end': whisper_word['end']
            })
    else:
        # Handle mismatched word counts with proportional timing
        total_duration = whisper_words[-1]['end'] - whisper_words[0]['start']
        time_per_word = total_duration / len(script_words)

        current_time = whisper_words[0]['start']
        for script_word in script_words:
            aligned_words.append({
                'word': script_word,
                'start': current_time,
                'end': current_time + time_per_word
            })
            current_time += time_per_word

    return aligned_words
```

**Timestamp Conversion:**

```python
def convert_to_srt_timestamp(seconds: float) -> str:
    """
    Convert seconds to SRT timestamp format: HH:MM:SS,mmm

    Example: 65.5 → 00:01:05,500
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
```

---

## Task 2: Video Compilation with Actual Audio Durations

### **Critical Change: Use Actual Audio Durations, Not Script Estimates**

**Problem with Original Approach:**
- Script.md provides timing estimates: Frame 0 (0:00-0:15) = 15 seconds
- Actual TTS audio might be: 14.64 seconds
- Using script timing causes sync issues and audio cutoff

**Corrected Approach:**
- Measure actual audio duration: `ffprobe -i frame_0.mp3` → 14.64s
- Use actual duration for frame display
- Frames and audio start/end simultaneously
- No artificial delays

**Example Frame Timing Calculation:**

```python
def calculate_actual_frame_times(frames: List[FrameData]) -> None:
    """
    Calculate actual frame start/end times based on measured audio durations

    This replaces script estimates with actual audio lengths.
    Frames and audio will start/end simultaneously.
    """
    current_time = 0.0

    for frame in frames:
        frame.actual_start_time = current_time
        frame.actual_end_time = current_time + frame.actual_audio_duration
        current_time = frame.actual_end_time
```

**Result:**
```
Frame 0:  0.00s - 14.64s (audio: 14.64s, script: 15.00s) ✓
Frame 1: 14.64s - 22.55s (audio:  7.91s, script: 10.00s) ✓
Frame 2: 22.55s - 34.75s (audio: 12.20s, script: 15.00s) ✓
...
Total video: 208.9s (not 240s from script!)
```

### **Video Structure**

```
Frame 0 [14.64s] → Crossfade [0.5s] → Frame 1 [7.91s] → Crossfade [0.5s] → Frame 2 [12.20s] → ...
```

**Transition Type:**

- **Crossfade** (0.5s duration) for all transitions - simple, professional, doesn't distract

---

### **FFmpeg Compilation Strategy**

**Method: Complex Filter Graph**

```bash
# Pseudo-structure (Claude Code will implement properly)
ffmpeg -i audio/frame_00.mp3 -i audio/frame_01.mp3 ... \
       -loop 1 -t 15 -i assets/frame_01.png \
       -loop 1 -t 10 -i assets/frame_02.png \
       ... \
       -filter_complex "
           [2:v]fade=t=in:d=0.3,fade=t=out:st=14.5:d=0.5[v0];
           [3:v]fade=t=in:d=0.5,fade=t=out:st=9.5:d=0.5[v1];
           [v0][v1]concat=n=2:v=1:a=0[vout];
           [0:a][1:a]concat=n=2:v=0:a=1[aout]
       " \
       -map "[vout]" -map "[aout]" \
       -i subtitles.srt -c:v libx264 -preset medium \
       -crf 23 -pix_fmt yuv420p -c:a aac -b:a 192k \
       -vf "subtitles=subtitles.srt:force_style='Fontsize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=2,Shadow=1,MarginV=30'" \
       final_video.mp4
```

---

### **Detailed Compilation Steps**

**Step 1: Prepare Frame Videos**

For each frame:
1. Take static image (frame_XX.png)
2. Calculate display duration from script.md
3. Add fade-in at start (0.5s)
4. Add fade-out at end (0.5s)
5. Total duration = target time from script

```python
def create_frame_video_segment(
    frame_num: int,
    image_path: str,
    duration: float,
    fade_duration: float = 0.5
) -> str:
    """
    Create video segment from static frame with fades
    
    Returns: FFmpeg filter string for this frame
    """
    fade_in = f"fade=t=in:st=0:d={fade_duration}"
    fade_out = f"fade=t=out:st={duration - fade_duration}:d={fade_duration}"
    
    return f"[{frame_num}:v]{fade_in},{fade_out},scale=1920:1080[v{frame_num}]"
```

**Step 2: Concatenate Frame Segments**

Chain all frame video segments:

```python
def build_concat_filter(num_frames: int) -> str:
    """
    Build FFmpeg concat filter for all frames
    
    [v0][v1][v2]...[vN]concat=n=N:v=1:a=0[video]
    """
    inputs = ''.join([f"[v{i}]" for i in range(num_frames)])
    return f"{inputs}concat=n={num_frames}:v=1:a=0[video]"
```

**Step 3: Concatenate Audio**

Chain all audio files:

```python
def build_audio_concat(num_frames: int) -> str:
    """
    Build FFmpeg concat filter for audio
    
    [0:a][1:a][2:a]...[N:a]concat=n=N:v=0:a=1[audio]
    """
    inputs = ''.join([f"[{i}:a]" for i in range(num_frames)])
    return f"{inputs}concat=n={num_frames}:v=0:a=1[audio]"
```

**Step 4: Burn Subtitles**

Apply subtitle overlay with styling:

```python
subtitle_style = (
    "Fontname=Arial,Fontsize=24,Bold=1,"
    "PrimaryColour=&HFFFFFF,OutlineColour=&H000000,"
    "BackColour=&H80000000,BorderStyle=4,"
    "Outline=2,Shadow=1,MarginV=30,Alignment=2"
)

# Add to filter chain
subtitle_filter = f"subtitles=subtitles.srt:force_style='{subtitle_style}'"
```

**Step 5: Encode Final Video**

Quality settings:

```bash
# Video encoding
-c:v libx264          # H.264 codec (universal compatibility)
-preset medium        # Encoding speed/quality balance
-crf 23               # Quality level (18-28, lower=better)
-pix_fmt yuv420p      # Color format (compatibility)

# Audio encoding
-c:a aac              # AAC codec
-b:a 192k             # Bitrate (good quality)

# Resolution
-s 1920x1080          # Full HD
-r 30                 # 30 fps (sufficient for static slides)
```

---

### **Implementation: compile_video.py**

```python
"""
Compile final video with transitions and subtitles (Whisper-Enhanced)

Main workflow:
1. Parse script.md (timing estimates + ground truth text)
2. Measure actual audio durations → Calculate actual frame times
3. Transcribe audio with Whisper → Get word-level timestamps
4. Align script text to Whisper timestamps → Correct transcription errors
5. Generate subtitles.srt (corrected text + Whisper timing)
6. Build FFmpeg filter graph:
   - Load frame images with ACTUAL audio durations
   - Add fade transitions (0.5s crossfade)
   - Concatenate video segments
   - Concatenate audio files (synchronized, no delay)
   - Burn subtitles with corrected text
7. Execute FFmpeg command
8. Verify output quality
9. Generate compilation report

Usage:
    python compile_video.py Week-1/Video-1

Output:
    Week-1/Video-1/final_video.mp4 (actual duration: 208.9s)
    Week-1/Video-1/subtitles.srt (corrected text + Whisper timing)
    Week-1/Video-1/compilation_report.txt

Key Principles:
- Use actual audio durations (not script estimates)
- Frames and audio synchronized (no delay)
- Subtitles generated after video structure finalized
- Script text corrects Whisper transcription errors
"""
```

---

## Task 3: Quality Verification

### **Post-Compilation Checks**

**1. Duration Verification**

```python
def verify_video_duration(video_path: str, expected_duration: float):
    """
    Verify final video matches expected duration from script.md
    
    Tolerance: ±2 seconds
    """
    cmd = ['ffprobe', '-i', video_path, 
           '-show_entries', 'format=duration',
           '-v', 'quiet', '-of', 'csv=p=0']
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    actual = float(result.stdout.strip())
    
    diff = abs(actual - expected_duration)
    
    if diff <= 2.0:
        return "✓ Duration OK"
    else:
        return f"⚠ Duration off by {diff:.1f}s"
```

**2. Subtitle Sync Check**

```python
def verify_subtitle_sync(video_path: str, srt_path: str):
    """
    Verify subtitles are properly synced with audio
    
    Sample check:
    - Frame 0 subtitle starts at 00:00:00
    - Frame 5 subtitle starts at expected time
    - Last subtitle ends with video
    """
    # Parse SRT
    with open(srt_path) as f:
        lines = f.readlines()
    
    # Extract first and last timestamps
    first_time = parse_srt_timestamp(lines[1].split(' --> ')[0])
    last_time = parse_srt_timestamp(lines[-2].split(' --> ')[1])
    
    # Compare to video duration
    # ... verification logic
```

**3. Video Quality Check**

```python
def analyze_video_quality(video_path: str):
    """
    Check video quality metrics
    
    - Resolution: 1920x1080
    - Frame rate: 30 fps
    - Video codec: H.264
    - Audio codec: AAC
    - Audio bitrate: 192k
    - File size: Reasonable (~10-20 MB for 4 min video)
    """
    cmd = ['ffprobe', '-v', 'error', 
           '-select_streams', 'v:0',
           '-show_entries', 'stream=width,height,codec_name,r_frame_rate',
           '-of', 'json', video_path]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    # Verify specs...
```

---

## Task 4: Generate Compilation Report

### **Report Format**

```
Video Compilation Report
========================
Video: Week-2/Video-1/final_video.mp4
Generated: 2025-11-12 14:30:25

INPUT VERIFICATION
------------------
✓ Script parsed: 12 frames
✓ Images found: 12 PNG files (1920x1080)
✓ Audio found: 12 MP3 files
✓ Total expected duration: 4:00 (240 seconds)

SUBTITLE GENERATION
-------------------
✓ Subtitles created: 45 subtitle entries
✓ Average display time: 5.3 seconds
✓ Max line length: 42 characters
✓ Format: SRT with styling

VIDEO COMPILATION
-----------------
✓ Frame transitions: Crossfade (0.5s)
✓ Video codec: H.264 (libx264, CRF 23)
✓ Audio codec: AAC (192 kbps)
✓ Resolution: 1920x1080 @ 30fps
✓ Subtitles: Burned-in with styling

OUTPUT VERIFICATION
-------------------
✓ Video duration: 4:02 (242s) - target: 4:00
✓ File size: 15.2 MB
✓ Audio/video sync: OK
✓ Subtitle sync: OK
✓ Quality metrics: PASS

FILES CREATED
-------------
✓ final_video.mp4 (15.2 MB)
✓ subtitles.srt (3.1 KB)
✓ compilation_report.txt (this file)

STATUS: ✓ COMPILATION SUCCESSFUL

Next step: Review video, then upload or distribute
```

---

## Complete FFmpeg Command Template

### **Actual Working Command Structure**

```bash
#!/bin/bash
# This is what Claude Code will generate dynamically

ffmpeg -y \
  # Input audio files
  -i audio/frame_00.mp3 \
  -i audio/frame_01.mp3 \
  -i audio/frame_02.mp3 \
  # ... (all audio files)
  
  # Input image files (as video)
  -loop 1 -t 15.0 -i assets/frame_01.png \
  -loop 1 -t 10.0 -i assets/frame_02.png \
  -loop 1 -t 40.0 -i assets/frame_03.png \
  # ... (all frame images with durations)
  
  # Complex filter graph
  -filter_complex "
    # Scale and add fades to each frame
    [12:v]scale=1920:1080,fps=30,fade=t=in:st=0:d=0.5,fade=t=out:st=14.5:d=0.5[v0];
    [13:v]scale=1920:1080,fps=30,fade=t=in:st=0:d=0.5,fade=t=out:st=9.5:d=0.5[v1];
    [14:v]scale=1920:1080,fps=30,fade=t=in:st=0:d=0.5,fade=t=out:st=39.5:d=0.5[v2];
    # ... (all frames)
    
    # Concatenate video frames
    [v0][v1][v2][v3][v4][v5][v6][v7][v8][v9][v10][v11]concat=n=12:v=1:a=0[video];
    
    # Concatenate audio files
    [0:a][1:a][2:a][3:a][4:a][5:a][6:a][7:a][8:a][9:a][10:a][11:a]concat=n=12:v=0:a=1[audio];
    
    # Burn subtitles onto video
    [video]subtitles=subtitles.srt:force_style='Fontname=Arial,Fontsize=24,Bold=1,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BackColour=&H80000000&,BorderStyle=4,Outline=2,Shadow=1,MarginV=30,Alignment=2'[final]
  " \
  
  # Map outputs
  -map "[final]" -map "[audio]" \
  
  # Video encoding settings
  -c:v libx264 \
  -preset medium \
  -crf 23 \
  -pix_fmt yuv420p \
  -r 30 \
  
  # Audio encoding settings
  -c:a aac \
  -b:a 192k \
  -ar 48000 \
  
  # Output file
  final_video.mp4

# Note: Claude Code will generate this dynamically based on script.md
```

---

## Error Handling Requirements

### **Common Issues and Solutions**

**Issue 1: Frame count mismatch**
```
Error: 11 audio files but 12 frames in script.md
Solution: Verify TTS generation completed for all frames
```

**Issue 2: Timing mismatch**
```
Error: Total audio duration (238s) ≠ expected duration (240s)
Solution: Check frame audio durations, regenerate if needed
```

**Issue 3: Subtitle overflow**
```
Error: Subtitle line exceeds 42 characters
Solution: Auto-split long lines at word boundaries
```

**Issue 4: FFmpeg filter error**
```
Error: Invalid filter graph syntax
Solution: Validate filter string before execution
```

**Error Handling Strategy:**

```python
class VideoCompilationError(Exception):
    """Base exception for compilation errors"""
    pass

class FrameMismatchError(VideoCompilationError):
    """Frame count doesn't match"""
    pass

class TimingError(VideoCompilationError):
    """Duration mismatch"""
    pass

class FFmpegError(VideoCompilationError):
    """FFmpeg execution failed"""
    pass

def compile_video_with_error_handling(video_folder: str):
    """
    Compile video with comprehensive error handling
    """
    try:
        # Validate inputs
        validate_input_files(video_folder)
        
        # Generate subtitles
        subtitles = generate_subtitles(video_folder)
        
        # Build FFmpeg command
        ffmpeg_cmd = build_ffmpeg_command(video_folder, subtitles)
        
        # Execute compilation
        execute_ffmpeg(ffmpeg_cmd)
        
        # Verify output
        verify_compilation(video_folder)
        
        # Generate report
        create_report(video_folder)
        
        return "SUCCESS"
        
    except FrameMismatchError as e:
        return f"ERROR: Frame mismatch - {e}"
    except TimingError as e:
        return f"ERROR: Timing issue - {e}"
    except FFmpegError as e:
        return f"ERROR: FFmpeg failed - {e}"
    except Exception as e:
        return f"ERROR: Unexpected error - {e}"
```

---

## Performance Optimization

### **Compilation Speed Tips**

**1. Use appropriate FFmpeg preset**
```python
PRESETS = {
    "ultrafast": "Fastest encoding, larger files",
    "fast": "Quick encoding, good for drafts",
    "medium": "Balanced (RECOMMENDED)",
    "slow": "Better quality, slower",
    "veryslow": "Best quality, very slow"
}

# For production: use "medium"
# For testing: use "fast"
```

**2. Parallel processing (if generating multiple videos)**
```python
from multiprocessing import Pool

def compile_multiple_videos(video_folders: list):
    """
    Compile multiple videos in parallel
    """
    with Pool(processes=4) as pool:
        results = pool.map(compile_video, video_folders)
    return results
```

**3. Progress monitoring**
```python
def monitor_ffmpeg_progress(process, total_duration: float):
    """
    Monitor FFmpeg progress and display percentage
    """
    pattern = re.compile(r'time=(\d+):(\d+):(\d+\.\d+)')
    
    for line in process.stderr:
        match = pattern.search(line)
        if match:
            h, m, s = match.groups()
            current = int(h) * 3600 + int(m) * 60 + float(s)
            percent = (current / total_duration) * 100
            print(f"\rProgress: {percent:.1f}%", end='')
```

---

## File Structure After Compilation

```
Week-2/Video-1/
├── script.md                      # Input script
├── assets/                        # Frame images
│   ├── frame_01.png
│   ├── frame_02.png
│   └── ... (12 frames)
├── audio/                         # Generated TTS
│   ├── frame_00.mp3
│   ├── frame_01.mp3
│   └── ... (12 audio files)
├── subtitles.srt                  # Generated subtitles
├── final_video.mp4                # ✓ FINAL OUTPUT
├── compilation_report.txt         # Verification report
└── tts_generation_report.txt     # From previous step
```

---

## Usage Instructions for Claude Code

### **Simple Command**

```bash
cd /path/to/your/course
python3 scripts/compile_video.py Week-1/Video-1
```

### **What the Script Does**

1. **Parse script.md**
   - Extract frame timing estimates (for reference)
   - Extract narration text (ground truth for subtitles)

2. **Validate inputs and calculate actual frame times**
   - Check script.md exists
   - Verify 12 frame images in frames/
   - Verify 12 audio files in audio/
   - **Measure actual audio durations** (using ffprobe)
   - **Calculate actual frame start/end times** (based on real audio)
   - Display timing comparison (script vs actual)

3. **Transcribe audio with Whisper**
   - Load Whisper model (small, ~460MB, cached after first use)
   - Transcribe each audio file with word-level timestamps
   - Adjust timestamps to match actual video timeline
   - Takes ~30-40 seconds for 12 frames

4. **Align script text to Whisper timestamps**
   - Map script words to Whisper word timestamps
   - Corrects transcription errors (e.g., "Cain" → "Keynes")
   - Preserves precise Whisper timing
   - Best of both worlds: correct text + precise timing

5. **Generate subtitles**
   - Group words into subtitle chunks (max 42 chars/line, 2 lines)
   - Create subtitles.srt with corrected text + Whisper timing
   - Apply formatting (Arial, size 18, bottom position)

6. **Build FFmpeg command**
   - Dynamic filter graph based on frame count
   - **Use actual audio durations** (not script estimates)
   - Add fade transitions (0.5s crossfade)
   - **Concatenate video and audio (synchronized, no delay)**
   - Burn subtitles with styling
   - Quality settings (H.264, 1080p, 30fps)

7. **Execute compilation**
   - Run FFmpeg command
   - Monitor progress
   - Handle errors gracefully
   - Takes ~25-30 seconds for 4-minute video

8. **Verify output**
   - Check video duration (should match total audio duration)
   - Verify resolution (1920x1080)
   - Check file size (reasonable: ~3-5 MB/minute)
   - Confirm codec (H.264)

9. **Generate report**
   - Create compilation_report.txt
   - Log all steps and results
   - Show timing comparison (script vs actual)
   - Highlight any warnings

10. **Output confirmation**
   ```
   ✓ Video compiled successfully
   ✓ Output: Week-1/Video-1/final_video.mp4
   ✓ Duration: 209s (actual audio: 208.9s, script: 240s)
   ✓ File size: 12.3 MB
   ✓ 43 subtitle entries (corrected text + Whisper timing)
   ✓ Quality: PASS

   Ready for review!
   ```

---

## Advanced Features (Optional)

### **Feature 1: Multiple Transition Styles**

```python
TRANSITION_STYLES = {
    "crossfade": "xfade=transition=fade:duration=0.5",
    "wipeleft": "xfade=transition=wipeleft:duration=0.5",
    "slidedown": "xfade=transition=slidedown:duration=0.5",
    "fadeblack": "fade=out:st={end-0.5}:d=0.5,fade=in:d=0.5"
}

# Default: crossfade (simple, professional)
# Can be configured per frame if needed
```

### **Feature 2: Custom Subtitle Styling**

```python
SUBTITLE_STYLES = {
    "default": {
        "Fontname": "Arial",
        "Fontsize": "24",
        "PrimaryColour": "&HFFFFFF",
        "OutlineColour": "&H000000",
        "BackColour": "&H80000000"
    },
    "minimal": {
        "Fontname": "Helvetica",
        "Fontsize": "20",
        "PrimaryColour": "&HFFFFFF",
        "OutlineColour": "&H000000",
        "BackColour": "&H00000000"  # Transparent
    }
}
```

### **Feature 3: Intro/Outro Support**

```python
def add_intro_outro(ffmpeg_cmd: str, intro_video: str, outro_video: str):
    """
    Optionally add intro and outro to video
    
    Structure: [Intro 5s] → [Main Content 4min] → [Outro 3s]
    """
    # Concatenate intro + main + outro
    # Adjust subtitle timing accordingly
```

---

## Testing Checklist

**Before Running Full Compilation:**

```
✓ Script parsed correctly (12 frames found)
✓ All frame images exist (1920x1080)
✓ All audio files exist (correct durations)
✓ FFmpeg installed and accessible
✓ Enough disk space (~50 MB)

Run compilation...

✓ Subtitles generated (check first 3 entries)
✓ FFmpeg command built (validate syntax)
✓ Compilation started (progress shown)
✓ Compilation completed (no errors)
✓ Output file created (final_video.mp4)

Post-compilation verification:

✓ Video plays correctly
✓ Audio synced with video
✓ Subtitles visible and readable
✓ Subtitles synced with audio
✓ Transitions smooth (no jarring cuts)
✓ Duration matches target (±2s)
✓ Quality acceptable (no artifacts)

Report generated:

✓ compilation_report.txt created
✓ All checks passed
✓ Ready for distribution
```

---

## Final Notes

**Compilation Time:**
- Single video (4 min): ~60-70 seconds on modern hardware
  - Whisper transcription: ~30-40s (first run downloads model)
  - FFmpeg compilation: ~25-30s
  - Validation & reporting: ~5s
- Subsequent videos: Faster (Whisper model cached)

**File Size:**
- Expected: 3-5 MB per minute
- 4-minute video: ~12-15 MB
- Acceptable range: 10-20 MB

**Quality Settings:**
- CRF 23: Good balance (recommended)
- CRF 18: Higher quality, larger files
- CRF 28: Lower quality, smaller files

**Compatibility:**
- Output format works on: YouTube, Vimeo, LMS platforms, all devices
- Subtitles: Burned-in (always visible), plus separate SRT file

**Key Improvements Over Original Specification:**
1. ✅ Uses actual audio durations (not script estimates)
2. ✅ Frames and audio synchronized (no artificial delays)
3. ✅ Subtitles generated after video structure finalized
4. ✅ Script text corrects Whisper transcription errors
5. ✅ No audio cutoff at frame transitions
6. ✅ Perfect subtitle synchronization with speech

---

## Implementation Priority

**Phase 1 (Essential):**
1. Parse script.md
2. Generate basic subtitles
3. Compile video with crossfade transitions
4. Basic verification

**Phase 2 (Enhanced):**
1. Advanced subtitle formatting
2. Progress monitoring
3. Detailed quality checks
4. Comprehensive reporting

**Phase 3 (Optional):**
1. Multiple transition styles
2. Intro/outro support
3. Batch processing
4. Custom styling options

---

*This specification provides complete instructions for Claude Code to implement automated video compilation with professional transitions and accessible subtitles.*
