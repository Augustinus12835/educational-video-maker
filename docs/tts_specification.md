# Text-to-Speech (TTS) Specification for FIN101 Videos

## Overview

This document specifies the text-to-speech system used to generate narration audio for FIN101 concept videos. The system uses Murf.ai's professional TTS API to convert frame-by-frame scripts into high-quality Australian English audio.

---

## Purpose

Generate individual MP3 audio files for each video frame with:
- Natural, professional Australian English narration
- Precise timing matching frame durations
- Consistent voice and pacing across all videos
- High audio quality suitable for educational content

---

## Murf API Configuration

### API Details

| Setting | Value | Description |
|---------|-------|-------------|
| **Endpoint** | `https://api.murf.ai/v1/speech/generate` | Main TTS generation endpoint |
| **Authentication** | `api-key` header | Uses API key from `.env` file |
| **Model Version** | `GEN2` | Latest Murf generation model |

### Voice Settings

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Voice ID** | `en-AU-leyton` | Australian male voice |
| **Voice Style** | `Narration` | Professional narration style |
| **Speaking Rate** | `-15` | Slower than normal (range: -50 to +50) |
| **Output Format** | `MP3` | Audio file format |
| **Sample Rate** | `44100` Hz | CD-quality audio |
| **Channels** | `MONO` | Single channel (default) |

### Target Speaking Rate

**2.5 words per second** - achieved through:
- Rate adjustment: `-15` (slower than default)
- Narration style: Professional, clear pacing
- Purpose: Ensures comprehension for educational content

---

## Voice Selection Rationale

### Primary Voice: Leyton (en-AU-leyton)

**Why Leyton?**
- ✅ Australian male voice (matches Jane's profile)
- ✅ Supports "Narration" style for educational content
- ✅ Professional, clear delivery
- ✅ Supports 39+ multilingual locales
- ✅ Multiple emotional styles available

**Supported Styles:**
- Narration ⭐ (Current choice)
- Conversational
- Inspirational
- Newscast
- Promo
- Calm
- Angry
- Sad
- Terrified

### Alternative Voice: Mitch (en-AU-mitch)

**Backup option if needed:**
- Australian male voice
- More casual tone
- Styles: Casual, Conversational, Narration, Promo

---

## Script Format Requirements

### Input Format (script.md)

The TTS script parser expects this exact format:

```markdown
## Frame 0 (0:00-0:15) • 38 words

[Narration text here]

---

## Frame 1 (0:15-0:25) • 25 words

[Narration text here]

---

## Frame 11 (3:00-4:00) • 150 words

[Content narration...]

[Closing summary integrated into final frame]
```

### Format Specifications

**Frame Headers:**
- Pattern: `## Frame <number> (<start>-<end>) • <count> words`
- **CRITICAL:** One narration per frame - NO combined frames (e.g., NO "Frame 1-2" or "Frame 3-4")
- **CRITICAL:** No separate Closing/Opening sections - integrate into frames
- Frame numbers start at 0 (not 1)
- Time format: `M:SS` or `MM:SS` (e.g., `0:15`, `1:25`)
- Word count: Integer followed by "words"
- Must include bullet point `•` before word count

**Text Content:**
- Plain text or markdown formatting
- Markdown will be cleaned before TTS:
  - Bold (`**text**`) → text
  - Italic (`*text*`) → text
  - Links (`[text](url)`) → text
- Multiple paragraphs supported
- Punctuation preserved for natural pauses

**Separators:**
- Use `---` between frames
- Required blank line after header
- Blank line before `---` separator

---

## Usage

### Basic Usage

```bash
cd /path/to/your/course
python3 scripts/generate_tts.py Week-X/Video-Y/script.md
```

### What It Does

1. **Parse script.md:**
   - Extracts frame numbers/names
   - Extracts timing information (start/end times)
   - Extracts narration text
   - Calculates target duration for each frame

2. **Process each frame:**
   - Clean markdown formatting from text
   - Call Murf API with configured settings
   - Download generated audio file
   - Save as `frame_N.mp3` in `audio/` subfolder (e.g., frame_0.mp3, frame_1.mp3)

3. **Verify timing:**
   - Read MP3 duration using mutagen
   - Compare to target duration
   - Report discrepancies >2 seconds
   - Suggest rate adjustments if needed

4. **Generate report:**
   - List all frames with status
   - Show timing accuracy
   - Highlight frames needing adjustment
   - Provide summary statistics

---

## Output Format

### File Structure

```
Week-X/Video-Y/
├── script.md                    # Input script
├── audio/                       # Generated audio (created automatically)
│   ├── frame_0.mp3             # Frame 0 audio
│   ├── frame_1.mp3             # Frame 1 audio
│   ├── frame_2.mp3             # Frame 2 audio
│   ├── frame_10.mp3            # Frame 10 audio
│   └── frame_11.mp3            # Frame 11 audio (includes closing)
└── frames/                      # Excalidraw exported images (manual)
    ├── frame_0.png
    ├── frame_1.png
    └── ...
```

### File Naming Convention

**CRITICAL REQUIREMENTS:**
- Pattern: `frame_N.mp3` where N is the frame number
- Frame numbers start at 0 (not 1)
- **NO zero-padding:** Use `frame_0.mp3`, `frame_1.mp3` NOT `frame_00.mp3`, `frame_01.mp3`
- Sequential numbering: `frame_0.mp3`, `frame_1.mp3`, `frame_2.mp3`, ..., `frame_10.mp3`, `frame_11.mp3`
- **NO combined frames:** Each frame number represents exactly one frame
- **NO special closing files:** Closing content integrated into last frame
- Matches PNG frame file naming exactly

### Audio Specifications

| Property | Value |
|----------|-------|
| Format | MP3 |
| Sample Rate | 44100 Hz |
| Bitrate | ~192 kbps (high quality) |
| Channels | Mono |
| Typical Size | 20-30 KB per second of audio |

---

## Timing Verification

### Acceptable Tolerance

**±2 seconds from target duration**
- Within tolerance: Frame marked as "OK" ✓
- Outside tolerance: Frame marked with warning ⚠

### Timing Issues

**If audio is too short/long:**

The script suggests rate adjustments:

```
⚠ frame_11.mp3: 35.2s (target: 60s) - 24.8s short - consider speed -10x
```

**Common Causes:**
1. **Too short:** Text spoken faster than expected
   - Solution: Decrease rate further (e.g., -20, -25)
   - Or: Add more content to script

2. **Too long:** Text spoken slower than expected
   - Solution: Increase rate (e.g., -10, -5, 0)
   - Or: Reduce content in script

### Rate Adjustment Guide

| Rate Value | Effect | Use Case |
|------------|--------|----------|
| -50 | Very slow | Complex technical content |
| -25 | Slow | Detailed explanations |
| **-15** | **Slightly slow** | **Standard (current)** |
| 0 | Normal | Conversational content |
| +15 | Slightly fast | Quick reviews |
| +25 | Fast | Time-constrained content |
| +50 | Very fast | Not recommended |

---

## Error Handling

### API Errors

**401 Unauthorized:**
- Cause: Invalid or missing API key
- Solution: Check `.env` file has correct `murf_api_key`

**400 Bad Request:**
- Cause: Invalid voice ID or parameters
- Solution: Verify voice ID exists (see Voice Selection section)

**404 Not Found:**
- Cause: Incorrect API endpoint
- Solution: Verify endpoint is `https://api.murf.ai/v1/speech/generate`

**429 Rate Limited:**
- Automatic retry with exponential backoff
- Wait times: 2s, 4s, 8s
- Max retries: 3

**Timeout Errors:**
- Increase timeout in script (default: 60s)
- Check internet connection
- Try regenerating individual frame

### File Errors

**Corrupted MP3 (very small file size):**
- Symptom: File <10 KB or "can't sync to MPEG frame" error
- Solution: Delete file and regenerate using `regenerate_frame_audio.py`

**Missing Frames:**
- Check script.md format matches specification
- Verify frame headers have correct pattern
- Look for parsing errors in output

---

## Report Format

### Example Output

```
============================================================
TTS Generation Complete
============================================================

✓ frame_0.mp3: 14.3s (target: 15s) - OK
✓ frame_1.mp3: 9.8s (target: 10s) - OK
✓ frame_2.mp3: 14.7s (target: 15s) - OK
✓ frame_3.mp3: 17.4s (target: 18s) - OK
✓ frame_4.mp3: 13.9s (target: 14s) - OK
✓ frame_5.mp3: 18.2s (target: 18s) - OK
✓ frame_6.mp3: 14.7s (target: 15s) - OK
✓ frame_7.mp3: 24.8s (target: 25s) - OK
✓ frame_8.mp3: 15.1s (target: 15s) - OK
✓ frame_9.mp3: 19.6s (target: 20s) - OK
✓ frame_10.mp3: 14.8s (target: 15s) - OK
✓ frame_11.mp3: 58.7s (target: 60s) - OK

Summary:
- Total frames: 12
- Successful: 12
- Need adjustment: 0
- Failed: 0
- Total audio duration: 3:56 (target: 4:00)

✓ All frames generated successfully!
```

### Status Indicators

| Symbol | Meaning |
|--------|---------|
| ✓ | Success - timing within ±2s |
| ⚠ | Warning - timing off by >2s |
| ✗ | Failed - API or processing error |

---

## Cost Considerations

### Murf API Pricing

- **Plan:** $3000/year for 12M characters
- **Trial:** 14 days available

### Estimated Usage

**Per frame:**
- Average: 50-100 words = 300-600 characters
- Cost: ~$0.0002-0.0005 per frame

**Per video (10 frames):**
- Characters: ~3,000-6,000
- Cost: ~$0.002-0.005

**Per week (10 videos):**
- Characters: ~30,000-60,000
- Cost: ~$0.02-0.05

**Per semester (13 weeks):**
- Characters: ~400,000-800,000
- Cost: ~$0.25-0.65

**Very cost-effective compared to hiring voice talent!**

---

## Regenerating Individual Frames

### When to Regenerate

- Corrupted file (very small size)
- Timing significantly off target
- Need different rate setting
- API timeout during generation

### Method 1: Delete and Re-run

```bash
rm Week-X/Video-Y/audio/frame_N.mp3
python3 scripts/generate_tts.py Week-X/Video-Y/script.md
```

Script will regenerate only missing frames.

**Example:**
```bash
# Regenerate frame 5
rm Week-1/Video-1/audio/frame_5.mp3
python3 scripts/generate_tts.py Week-1/Video-1/script.md
```

### Method 2: Use Regeneration Script

Create a custom script (see `scripts/regenerate_frame_audio.py` as example):

```python
from generate_tts import call_murf_api

text = "Your narration text here"
output_path = "Week-X/Video-Y/audio/frame_N.mp3"  # e.g., frame_5.mp3

audio_data = call_murf_api(text)
with open(output_path, 'wb') as f:
    f.write(audio_data)
```

---

## Quality Checklist

Before finalizing audio:

- [ ] All frames generated successfully
- [ ] No corrupted files (check file sizes >10 KB)
- [ ] Timing within acceptable range (±2s per frame)
- [ ] Total duration matches target video length
- [ ] Audio plays without errors
- [ ] Voice quality is clear and professional
- [ ] Speaking rate feels natural (not too fast/slow)
- [ ] Volume levels consistent across frames

---

## Troubleshooting

### Problem: Script parser not finding frames

**Symptoms:**
- Fewer frames found than expected
- "Found 0 frames" message

**Solutions:**
1. Check frame header format exactly matches specification
2. Ensure blank line after header before text
3. Verify `---` separators between frames
4. Check for typos in "Frame" or "words"

### Problem: Audio too fast or too slow

**Symptoms:**
- Speaking rate doesn't match 2.5 w/s target
- Duration significantly off

**Solutions:**
1. Adjust `SPEAKING_RATE` in `generate_tts.py`:
   - Too fast: decrease rate (e.g., -20, -25)
   - Too slow: increase rate (e.g., -10, -5)
2. Test with single frame first
3. Regenerate all frames with new rate

### Problem: API timeouts

**Symptoms:**
- "ReadTimeout" errors
- Script hangs on API call

**Solutions:**
1. Increase timeout value in script (60s → 90s)
2. Check internet connection stability
3. Try during off-peak hours
4. Regenerate failed frames individually

### Problem: Wrong voice or style

**Symptoms:**
- Voice doesn't sound Australian
- Tone not appropriate for education

**Solutions:**
1. Verify `VOICE_ID = "en-AU-leyton"` in script
2. Verify `VOICE_STYLE = "Narration"` in script
3. Check API documentation for voice changes
4. Test alternative voice: `en-AU-mitch`

---

## Future Enhancements

### Potential Improvements

1. **Batch processing:**
   - Generate audio for all videos in a week
   - Parallel API calls for faster processing

2. **Interactive rate tuning:**
   - Test different rates for single frame
   - Choose best before batch processing

3. **Voice variety:**
   - Use different voices for quotes vs. narration
   - Add emphasis/emotion styles for key points

4. **Quality validation:**
   - Automated audio quality checks
   - Pronunciation verification
   - Background noise detection

5. **Integration with video compilation:**
   - Directly feed audio to video editor
   - Automated syncing with frames
   - One-command video generation

---

## Related Documents

- **concept_video_creation.md** - Overall video workflow (Steps 1-6)
- **teaching_style_guide.md** - Script writing guidelines
- **perplexity_slide_context_instructions.md** - Research context generation
- **scripts/README.md** - Script documentation and usage
- **CLAUDE.md** - Master project documentation

---

## Dependencies

### Python Packages

```bash
pip3 install requests python-dotenv mutagen
```

- **requests** - HTTP API calls to Murf
- **python-dotenv** - Load API key from .env file
- **mutagen** - Read MP3 duration for verification

### Environment Variables

Location: `/path/to/your/project/.env`

```bash
# Murf API Key (get from https://murf.ai/api)
MURF_API_KEY=your_murf_api_key_here
```

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-12 | 1.0 | Initial specification created |
| | | - Murf API integration complete |
| | | - Voice: en-AU-leyton (Narration) |
| | | - Rate: -15 for 2.5 w/s target |
| | | - Timing verification implemented |
| 2025-11-12 | 1.1 | Updated naming conventions |
| | | - **BREAKING:** Changed to frame_N.mp3 (NO zero-padding) |
| | | - **BREAKING:** No combined frames (removed Frame 1-2 support) |
| | | - **BREAKING:** No separate Closing section |
| | | - Frame numbers start at 0 |
| | | - Matches PNG frame file naming |

---

_Last Updated: 2025-11-12_
_Course: FIN101 Introduction to Financial Concepts_
_Coordinator: Dr. Jane Wu_
_Generated with Claude Code assistance_
