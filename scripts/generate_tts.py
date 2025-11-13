#!/usr/bin/env python3
"""
TTS Audio Generation Script for Educational Videos
Generates individual MP3 files for each frame using Murf API
"""

import os
import sys
import re
import time
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
from mutagen.mp3 import MP3

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

# API Configuration
MURF_API_KEY = os.getenv('MURF_API_KEY')
MURF_API_ENDPOINT = "https://api.murf.ai/v1/speech/generate"
VOICE_ID = "en-AU-leyton"  # Australian male, professional (supports Narration style)
VOICE_STYLE = "Narration"  # Professional narration for educational content
SPEAKING_RATE = -15        # Slower rate (-50 to 50, negative is slower)
OUTPUT_FORMAT = "MP3"
SAMPLE_RATE = 44100

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

class Frame:
    """Represents a single frame with narration"""
    def __init__(self, number, start_time, end_time, word_count, text):
        self.number = number
        self.start_time = start_time
        self.end_time = end_time
        self.word_count = word_count
        self.text = text
        self.duration = self.calculate_duration()

    def calculate_duration(self):
        """Calculate target duration in seconds from time range"""
        start_parts = self.start_time.split(':')
        end_parts = self.end_time.split(':')

        start_seconds = int(start_parts[0]) * 60 + int(start_parts[1])
        end_seconds = int(end_parts[0]) * 60 + int(end_parts[1])

        return end_seconds - start_seconds

    def __repr__(self):
        return f"Frame {self.number}: {self.duration}s, {self.word_count} words"


def parse_script(script_path):
    """
    Parse script.md file to extract frame information

    Expected format:
    ## Frame X (MM:SS-MM:SS) • NN words

    [narration text]
    """
    frames = []

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script file not found: {script_path}")

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match frame headers
    # ## Frame 0 (0:00-0:15) • 38 words
    pattern = r'## Frame (\d+) \((\d+:\d+)-(\d+:\d+)\) • (\d+) words\n\n(.*?)(?=\n## |\Z)'

    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        frame_num = int(match.group(1))
        start_time = match.group(2)
        end_time = match.group(3)
        word_count = int(match.group(4))
        text = match.group(5).strip()

        # Clean the text - remove markdown formatting
        text = clean_narration_text(text)

        frame = Frame(frame_num, start_time, end_time, word_count, text)
        frames.append(frame)

    return frames


def clean_narration_text(text):
    """Remove markdown formatting and clean narration text"""
    # Remove markdown bold/italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)

    # Remove markdown links [text](url)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

    # Remove excess whitespace
    text = ' '.join(text.split())

    return text


def call_murf_api(text, retry_count=0):
    """
    Call Murf API to generate audio from text

    Returns:
        bytes: Audio file content
    """
    if not MURF_API_KEY:
        raise ValueError("MURF_API_KEY not found in environment variables")

    headers = {
        'api-key': MURF_API_KEY,
        'Content-Type': 'application/json'
    }

    payload = {
        'text': text,
        'voiceId': VOICE_ID,
        'style': VOICE_STYLE,
        'rate': SPEAKING_RATE,
        'format': OUTPUT_FORMAT,
        'sampleRate': SAMPLE_RATE,
        'modelVersion': 'GEN2'
    }

    try:
        response = requests.post(
            MURF_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            # Parse the response
            result = response.json()

            # Murf API returns an audio URL in the 'audioFile' field
            if 'audioFile' in result:
                audio_url = result['audioFile']
                audio_response = requests.get(audio_url, timeout=30)
                return audio_response.content
            else:
                raise Exception(f"Unexpected API response format: {result}")

        elif response.status_code == 429:  # Rate limit
            if retry_count < MAX_RETRIES:
                wait_time = RETRY_DELAY * (2 ** retry_count)
                print(f"  Rate limited. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
                return call_murf_api(text, retry_count + 1)
            else:
                raise Exception(f"Rate limit exceeded after {MAX_RETRIES} retries")

        else:
            raise Exception(f"API error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        if retry_count < MAX_RETRIES:
            print(f"  Request failed. Retrying ({retry_count + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
            return call_murf_api(text, retry_count + 1)
        else:
            raise Exception(f"Failed after {MAX_RETRIES} retries: {str(e)}")


def get_audio_duration(file_path):
    """Get duration of MP3 file in seconds"""
    try:
        audio = MP3(file_path)
        return audio.info.length
    except Exception as e:
        print(f"  Warning: Could not read audio duration: {e}")
        return None


def generate_audio_for_frames(frames, output_dir):
    """
    Generate audio files for all frames

    Returns:
        list: Report entries for each frame
    """
    results = []

    # Create audio directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for frame in frames:
        frame_filename = f"frame_{frame.number}.mp3"
        output_path = os.path.join(output_dir, frame_filename)

        print(f"\nProcessing Frame {frame.number}...")
        print(f"  Target duration: {frame.duration}s")
        print(f"  Word count: {frame.word_count}")
        print(f"  Text preview: {frame.text[:60]}...")

        try:
            # Generate audio
            audio_data = call_murf_api(frame.text)

            # Save to file
            with open(output_path, 'wb') as f:
                f.write(audio_data)

            print(f"  ✓ Saved to {frame_filename}")

            # Verify duration
            actual_duration = get_audio_duration(output_path)

            if actual_duration:
                difference = actual_duration - frame.duration

                result = {
                    'frame': frame.number,
                    'filename': frame_filename,
                    'target': frame.duration,
                    'actual': actual_duration,
                    'difference': difference,
                    'status': 'success'
                }

                # Check if timing is acceptable (within 2 seconds)
                if abs(difference) > 2:
                    result['warning'] = True
                    suggested_speed = SPEAKING_RATE * (actual_duration / frame.duration)
                    result['suggested_speed'] = round(suggested_speed, 2)
                else:
                    result['warning'] = False

                results.append(result)
                print(f"  Duration: {actual_duration:.1f}s (diff: {difference:+.1f}s)")
            else:
                results.append({
                    'frame': frame.number,
                    'filename': frame_filename,
                    'target': frame.duration,
                    'status': 'success',
                    'warning': False,
                    'note': 'Could not verify duration'
                })

        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
            results.append({
                'frame': frame.number,
                'filename': frame_filename,
                'target': frame.duration,
                'status': 'failed',
                'error': str(e)
            })

        # Small delay between frames to avoid rate limiting
        time.sleep(1)

    return results


def print_report(results):
    """Print final generation report"""
    print("\n" + "=" * 60)
    print("TTS Generation Complete")
    print("=" * 60)
    print()

    successful = 0
    failed = 0
    needs_adjustment = 0
    total_actual_duration = 0
    total_target_duration = 0

    for result in results:
        if result['status'] == 'success':
            successful += 1

            if 'actual' in result:
                total_actual_duration += result['actual']
                total_target_duration += result['target']

                if result.get('warning', False):
                    needs_adjustment += 1
                    print(f"⚠ {result['filename']}: {result['actual']:.1f}s (target: {result['target']}s) - "
                          f"{abs(result['difference']):.1f}s {'short' if result['difference'] < 0 else 'long'} - "
                          f"consider speed {result['suggested_speed']}x")
                else:
                    print(f"✓ {result['filename']}: {result['actual']:.1f}s (target: {result['target']}s) - OK")
            else:
                print(f"✓ {result['filename']}: Saved ({result.get('note', '')})")
        else:
            failed += 1
            print(f"✗ {result['filename']}: FAILED - {result['error']}")

    print()
    print("Summary:")
    print(f"- Total frames: {len(results)}")
    print(f"- Successful: {successful}")
    print(f"- Need adjustment: {needs_adjustment}")
    print(f"- Failed: {failed}")

    if total_actual_duration > 0:
        print(f"- Total audio duration: {format_time(total_actual_duration)} "
              f"(target: {format_time(total_target_duration)})")

    print()
    if failed == 0 and needs_adjustment == 0:
        print("✓ All frames generated successfully!")
        print("Next step: Run video compilation")
    elif failed == 0:
        print(f"⚠ Review {needs_adjustment} frame(s) with timing issues")
    else:
        print(f"✗ {failed} frame(s) failed. Review errors above.")


def format_time(seconds):
    """Format seconds as MM:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Usage: python generate_tts.py <path_to_script.md>")
        print()
        print("Example:")
        print("  python generate_tts.py Week-1/Video-1/script.md")
        print("  python generate_tts.py ../Week-2/Video-3/script.md")
        sys.exit(1)

    script_path = sys.argv[1]

    # Determine output directory (same directory as script, in 'audio' subfolder)
    script_dir = os.path.dirname(script_path)
    audio_dir = os.path.join(script_dir, 'audio')

    print("=" * 60)
    print("Murf TTS Audio Generator")
    print("=" * 60)
    print(f"Script: {script_path}")
    print(f"Output: {audio_dir}")
    print(f"Voice: {VOICE_ID}")
    print(f"Rate: {SPEAKING_RATE} (-50=slow, 0=normal, 50=fast)")
    print("=" * 60)

    # Verify API key
    if not MURF_API_KEY:
        print("\n✗ Error: MURF_API_KEY not found in environment")
        print("  Please check your .env file")
        sys.exit(1)

    try:
        # Parse script
        print("\nParsing script...")
        frames = parse_script(script_path)
        print(f"✓ Found {len(frames)} frames")

        # Generate audio
        results = generate_audio_for_frames(frames, audio_dir)

        # Print report
        print_report(results)

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
