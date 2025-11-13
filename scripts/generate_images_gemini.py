#!/usr/bin/env python3
"""
EXAMPLE SCRIPT: AI Image Generation with Gemini

This script is provided as an ILLUSTRATION ONLY. It's specific to our finance course content.

For your own course:
1. Ask Claude Code to read docs/image_fetching_spec.md
2. Describe what images you need for your subject area
3. Claude Code will create a custom version of this script for your content

This demonstrates how to:
- Generate hand-drawn style images using Gemini (Imagen)
- Create conceptual diagrams in Excalidraw-compatible style
- Fetch real photos using Perplexity API when needed
"""

import os
import requests
import json
import time
import base64
from datetime import datetime
from pathlib import Path

# Load API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Add it to your .env file.")

# Gemini API endpoint for image generation
GEMINI_MODEL = "gemini-2.5-flash-image"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Base style descriptor for all images
BASE_STYLE = """Hand-drawn illustration in Excalidraw style, black and white line art,
simple sketch, minimalist, clean lines, no shading, no color,
white background. NO TEXT, NO LABELS, NO ANNOTATIONS, NO WORDS, NO NUMBERS, NO DIAGRAMS.
Pure visual illustration only."""

# Negative prompt to enforce style
NEGATIVE_PROMPT = """text, labels, annotations, words, letters, numbers, explanations, diagrams, charts,
color, colors, colorful, photorealistic, photograph, realistic lighting,
3d render, gradient, shadow, shading, texture, complex details,
gray tones, watercolor, painting style"""

def generate_image_gemini(subject, context_modifier="", num_images=2):
    """
    Generate images using Gemini Imagen API

    Args:
        subject: What to generate (e.g., "black swan", "dice")
        context_modifier: Additional context (e.g., "side view", "showing probability")
        num_images: Number of images to generate

    Returns:
        List of image data (base64 or URLs)
    """
    # Construct full prompt
    full_prompt = f"{BASE_STYLE} {subject}"
    if context_modifier:
        full_prompt += f", {context_modifier}"

    print(f"\nGenerating {num_images} image(s) for: {subject}")
    print(f"Style: Hand-drawn, black & white, Excalidraw-compatible")

    url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    # Gemini 2.5 Flash uses generateContent format
    # Request image generation by asking in the prompt
    # Include negative prompt explicitly in the text
    full_request = f"""Generate an image: {full_prompt}

IMPORTANT:
- Do NOT include any text, labels, annotations, words, letters, or numbers in the image
- Pure visual illustration only
- Clean image without explanations or captions

Avoid: {NEGATIVE_PROMPT}"""

    data = {
        "contents": [{
            "parts": [{
                "text": full_request
            }]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "topK": 32,
            "topP": 1,
            "maxOutputTokens": 8192
        }
    }

    try:
        print(f"  Calling Gemini API...")
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()

        # Extract generated images from candidates
        candidates = result.get('candidates', [])

        if not candidates:
            print(f"  ✗ No images generated")
            return []

        generated_images = []
        for candidate in candidates:
            content = candidate.get('content', {})
            parts = content.get('parts', [])

            for part in parts:
                # Check for inline_data (images are returned as inline_data)
                if 'inline_data' in part or 'inlineData' in part:
                    inline = part.get('inline_data') or part.get('inlineData')
                    if inline and 'data' in inline:
                        generated_images.append({
                            'data': inline['data'],
                            'format': 'base64',
                            'mime_type': inline.get('mime_type', 'image/png')
                        })

        print(f"  ✓ Generated {len(generated_images)} image(s)")
        return generated_images

    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error calling Gemini API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response: {e.response.text}")
        return []
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return []

def save_image(image_data, filename, assets_folder):
    """Save base64 image data to file"""
    try:
        filepath = assets_folder / filename

        # Decode base64 and save
        image_bytes = base64.b64decode(image_data['data'])

        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        # Verify file was saved
        if os.path.getsize(filepath) > 0:
            size_kb = os.path.getsize(filepath) / 1024
            return True, size_kb
        else:
            os.remove(filepath)
            return False, 0

    except Exception as e:
        print(f"  Error saving {filename}: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False, 0

def clean_filename(subject):
    """Convert subject to clean filename"""
    filename = subject.lower()
    filename = filename.replace(' ', '_')
    filename = ''.join(c for c in filename if c.isalnum() or c == '_')
    return filename[:50]

def create_attribution_entry(filename, subject, prompt, generation_date):
    """Create attribution entry for AI-generated image"""
    entry = f"""
### {filename}

**Source:** AI-generated (Gemini Imagen 3.0)
**Generation Date:** {generation_date}
**Prompt:** "{prompt}"
**License:** User owns rights (No copyright)
**Attribution Required:** No

**Usage in Video:**
- (To be filled in when used)

**Note:** AI-generated image for conceptual illustration

---
"""
    return entry

def main():
    """Test generation of black swan and dice images"""

    video_folder = '/path/to/your/course/Week-1/Video-1'
    assets_folder = Path(video_folder) / 'assets'
    assets_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Generating AI Images with Gemini 2.5 Flash (Imagen)")
    print("Style: Hand-drawn, Black & White, Excalidraw-compatible")
    print("=" * 70)

    all_attributions = []

    # 1. Generate black swan images
    images_to_generate = [
        {
            'subject': 'black swan',
            'context': 'A black swan bird, simple silhouette, elegant, clean visual only',
            'num': 2
        },
        {
            'subject': 'dice',
            'context': 'Two six-sided dice, simple geometric cubes with dots, clean visual only',
            'num': 2
        }
    ]

    for img_config in images_to_generate:
        subject = img_config['subject']
        context = img_config['context']
        num_images = img_config['num']

        # Generate images
        generated_images = generate_image_gemini(subject, context, num_images)

        if not generated_images:
            print(f"  ⚠ No images generated for {subject}, skipping...")
            continue

        # Save images
        clean_name = clean_filename(subject)
        for i, img_data in enumerate(generated_images, 1):
            filename = f"{clean_name}_ai_{i:02d}.png"

            print(f"  Saving {filename}...", end=' ')
            success, size_kb = save_image(img_data, filename, assets_folder)

            if success:
                print(f"✓ ({size_kb:.0f} KB)")

                # Create attribution info
                full_prompt = f"{BASE_STYLE} {subject}, {context}"
                attribution = {
                    'filename': filename,
                    'subject': subject,
                    'prompt': full_prompt[:100] + "...",  # Truncate for readability
                    'date': datetime.now().strftime('%Y-%m-%d')
                }
                all_attributions.append(attribution)
            else:
                print("✗ Failed")

        time.sleep(2)  # Rate limiting

    # Print summary
    print("\n" + "=" * 70)
    print(f"✓ Successfully generated {len(all_attributions)} AI images")
    print(f"Images saved to: {assets_folder}")
    print("=" * 70)

    # Print attribution info for manual update
    if all_attributions:
        print("\n\nAttribution entries for attribution.md:")
        print("-" * 70)
        for attr in all_attributions:
            entry = create_attribution_entry(
                attr['filename'],
                attr['subject'],
                attr['prompt'],
                attr['date']
            )
            print(entry)

if __name__ == '__main__':
    main()
