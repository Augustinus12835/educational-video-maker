#!/usr/bin/env python3
"""
Quick script to regenerate a single frame
"""

import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

# API Configuration
MURF_API_KEY = os.getenv('MURF_API_KEY')
MURF_API_ENDPOINT = "https://api.murf.ai/v1/speech/generate"
VOICE_ID = "en-AU-leyton"
VOICE_STYLE = "Narration"
SPEAKING_RATE = -15
OUTPUT_FORMAT = "MP3"
SAMPLE_RATE = 44100

def generate_audio(text, output_path):
    """Generate audio for a single frame"""

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

    print(f"Generating audio...")
    print(f"Text: {text[:60]}...")

    response = requests.post(
        MURF_API_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code == 200:
        result = response.json()

        if 'audioFile' in result:
            audio_url = result['audioFile']
            print(f"Downloading audio from: {audio_url[:50]}...")
            audio_response = requests.get(audio_url, timeout=60)

            with open(output_path, 'wb') as f:
                f.write(audio_response.content)

            print(f"✓ Saved to {output_path}")
            return True
        else:
            print(f"✗ Error: Unexpected response format")
            return False
    else:
        print(f"✗ API error {response.status_code}: {response.text}")
        return False

# Frame 7 text from script.md
text = """Car insurance premiums demonstrate measurable risk. Actuarial tables allow insurance companies to assign probabilities to different accident types using driver age, past accidents, location, and vehicle type.

Your insurer analyzes your profile against millions of data points. They calculate precise accident probabilities for your demographic. Known probabilities mean measurable risk."""

output_path = "/path/to/your/course/Week-1/Video-1/audio/frame_07.mp3"

print("=" * 60)
print("Regenerating Frame 7")
print("=" * 60)

if generate_audio(text, output_path):
    print("\n✓ Frame 7 regenerated successfully!")
else:
    print("\n✗ Failed to regenerate frame 7")
