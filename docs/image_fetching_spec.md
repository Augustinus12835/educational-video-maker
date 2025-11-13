# Image Fetching with Attribution - Implementation Specification

## Overview

This specification describes how Claude Code should implement on-demand image fetching using:
1. **Gemini API (Imagen)** for AI-generated conceptual images (hand-drawn, black/white style)
2. **Perplexity API** for real photos of people, logos, and branded content
3. Automatic attribution tracking for all images

---

## Decision Logic: AI-Generated vs Real Photo

### **Use Gemini AI Generation (hand-drawn, black/white style):**
- ✅ Abstract concepts (black swan, dice, question marks)
- ✅ Diagrams and charts (risk matrices, spectrums, flowcharts)
- ✅ Objects and animals (non-specific)
- ✅ Generic illustrations (arrows, icons, symbols)
- ✅ Background elements
- ✅ Conceptual visualizations

### **Use Perplexity Search (real photos):**
- ✅ Real people (Warren Buffett, Charlie Munger, etc.)
- ✅ Company logos and branding
- ✅ Specific buildings or landmarks
- ✅ Historical photographs
- ✅ Authentic data visualizations from sources
- ✅ When authenticity matters more than style consistency

### **Auto-Detection Rules:**

**Triggers for Perplexity (real photo):**
- Request mentions a person's name: "Warren Buffett", "Ray Dalio"
- Request mentions company/brand: "Berkshire Hathaway logo", "Apple headquarters"
- Keywords: "photo of", "portrait of", "real", "authentic"
- User explicitly says: "get me a real photo of..."

**Triggers for Gemini (AI-generated):**
- Abstract concepts: "black swan", "dice", "question mark"
- Diagram requests: "risk matrix", "spectrum diagram", "flowchart"
- Generic objects: "hourglass", "balance scale", "compass"
- Keywords: "illustration", "icon", "symbol", "diagram"
- User explicitly says: "generate an image of..."
- **Default for non-person subjects**

---

## Use Cases

### **Scenario 1: Conceptual Image (AI-Generated)**

**User command:**
> "Claude, I need a black swan image for Week-1/Video-1"

**Expected behavior:**
1. Detects: Abstract concept → Use Gemini
2. Generates hand-drawn, black/white image with Gemini API
3. Saves to `Week-1/Video-1/assets/black_swan_ai_01.png`
4. Adds entry to `attribution.md` (AI-generated, no attribution required)
5. Responds with image path and usage suggestions

### **Scenario 2: Person Photo (Real Photo)**

**User command:**
> "Claude, I need Warren Buffett portrait for Week-1/Video-1"

**Expected behavior:**
1. Detects: Person's name → Use Perplexity
2. Searches Perplexity API for real photos
3. Downloads top 2-3 to `Week-1/Video-1/assets/`
4. Names: `warren_buffett_portrait_01.jpg`, etc.
5. Adds full attribution to `attribution.md`
6. Responds with image paths and licensing info

---

## Command Interface

### **Format:**

User says one of:
- "Get me an image of [subject] for Week-X/Video-Y"
- "I need a [subject] image for Video-Y"
- "Find images of [subject] for this video"
- "Generate [subject] illustration for Video-Y"
- "Get me a real photo of [person] for Video-Y" (forces Perplexity)
- "Generate a [concept] icon for Video-Y" (forces Gemini)

### **Parameters to Extract:**

1. **Subject:** What to search/generate (e.g., "black swan", "Warren Buffett", "risk matrix")
2. **Video folder:** Week-X/Video-Y (infer from context or ask user)
3. **Source preference:** Auto-detect or user-specified (real photo vs AI-generated)
4. **Number of images:** Default 2-3 for Perplexity, 1-2 for Gemini
5. **Style notes:** Any specific styling requests (though default is hand-drawn B&W)

---

## Gemini API Integration (AI Image Generation)

### **API Configuration:**

```
Endpoint: https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:generateImages
API Key: From .env file (GEMINI_API_KEY)
Model: imagen-3.0-generate-001 (or "Nanobanana" endpoint if specific)
```

### **Request Structure:**

```json
{
  "prompt": "[Generated prompt - see below]",
  "numberOfImages": 2,
  "aspectRatio": "16:9",
  "negativePrompt": "color, photorealistic, 3d render, photograph, gradient, shadow",
  "personGeneration": "DONT_ALLOW",
  "safetyFilterLevel": "BLOCK_ONLY_HIGH"
}
```

### **Style Prompt Template:**

**Base style descriptor (prepend to all prompts):**
```
"Hand-drawn illustration in Excalidraw style, black and white line art, 
simple sketch, minimalist, clean lines, no shading, no color, 
white background, educational diagram style"
```

**Full prompt construction:**
```
[Base style descriptor] + [User's subject] + [Context-specific modifiers]

Examples:

Subject: "black swan"
Full prompt: "Hand-drawn illustration in Excalidraw style, black and white 
line art, simple sketch, minimalist, clean lines, no shading, no color, 
white background, educational diagram style. A black swan bird on water, 
side view, elegant pose, suitable for finance education."

Subject: "risk matrix"
Full prompt: "Hand-drawn illustration in Excalidraw style, black and white 
line art, simple sketch, minimalist, clean lines, no shading, no color, 
white background, educational diagram style. A 2x2 risk matrix diagram with 
four quadrants, clear labels, arrows, professional business diagram."

Subject: "dice showing probability"
Full prompt: "Hand-drawn illustration in Excalidraw style, black and white 
line art, simple sketch, minimalist, clean lines, no shading, no color, 
white background, educational diagram style. Two six-sided dice showing 
different numbers, isometric view, simple geometric shapes."
```

### **Negative Prompt (what to avoid):**

Always include to enforce black/white hand-drawn style:
```
"color, colors, colorful, photorealistic, photograph, realistic lighting, 
3d render, gradient, shadow, shading, texture, complex details, 
gray tones, watercolor, painting style"
```

### **Context-Specific Modifiers:**

Add based on subject type:

**For objects/animals:**
- "side view" or "front view" (for consistency)
- "simple geometric shapes"
- "clear silhouette"

**For diagrams:**
- "clear labels and text spaces"
- "professional business diagram"
- "grid aligned"

**For icons/symbols:**
- "centered composition"
- "scalable vector style"
- "bold outlines"

### **Response Parsing:**

Gemini returns:
```json
{
  "generatedImages": [
    {
      "imageUri": "https://generativelanguage.googleapis.com/...",
      "mimeType": "image/png"
    }
  ]
}
```

Download image from `imageUri` and save to assets folder.

---

## Perplexity API Integration (Real Photos Only)

### **When to Use:**
Only for real people, logos, brands, or when authenticity is required over style consistency.

### **API Configuration:**

```
Endpoint: https://api.perplexity.ai/chat/completions
Model: sonar
API Key: From .env file (PERPLEXITY_API_KEY)
```

### **Request Parameters:**

```json
{
  "model": "sonar",
  "messages": [
    {
      "role": "system",
      "content": "You are an image search assistant. Find high-quality, properly licensed real photos suitable for educational use."
    },
    {
      "role": "user",
      "content": "[Generated prompt - see below]"
    }
  ],
  "temperature": 0.2,
  "search_recency_filter": "month",
  "return_images": true,
  "return_citations": true
}
```

### **Prompt Construction for Real Photos:**

**For portraits/people (PRIMARY USE CASE):**
```
Find 2-3 professional photos of [person name] suitable for educational use.
Prioritize:
1. Wikimedia Commons (Creative Commons or Public Domain)
2. Official photos from company websites or press kits
3. Clear, high-quality headshots or professional portraits
4. Appropriate for academic context
5. Verifiable licensing information

For each image provide:
- Direct image URL
- Source (Wikimedia Commons, official website, etc.)
- Specific license type (CC-BY-SA 4.0, CC0, Fair Use, etc.)
- Required attribution text (exact wording)
- Image resolution and quality notes
```

**For logos/brands:**
```
Find official [company/brand] logo or trademark image from authoritative sources.
Prioritize:
1. Official company website or press kit
2. Wikimedia Commons (if available)
3. High resolution, ideally transparent background
4. Vector format (SVG) if available

For each image provide:
- Image URL
- Official source
- Usage guidelines
- Trademark notice requirements
```

---

## Response Parsing

### **Gemini Response (AI-Generated):**

```json
{
  "generatedImages": [
    {
      "imageUri": "https://generativelanguage.googleapis.com/v1/...",
      "mimeType": "image/png"
    }
  ]
}
```

**Processing:**
1. Extract `imageUri` from each generated image
2. Download PNG file
3. Save with `_ai_` infix: `black_swan_ai_01.png`
4. No attribution required (AI-generated)

### **Perplexity Response (Real Photos):**

```json
{
  "choices": [{
    "message": {
      "content": "Text description of found images with URLs and licensing..."
    }
  }],
  "images": [
    "https://commons.wikimedia.org/image1.jpg",
    "https://example.com/image2.jpg"
  ],
  "citations": [
    "https://commons.wikimedia.org/wiki/File:...",
    "https://example.com/about"
  ]
}
```

**Processing:**
1. Extract `images` array: Direct URLs to download
2. Parse `content` text for licensing info
3. Extract attribution requirements
4. Download and save as: `warren_buffett_portrait_01.jpg`
5. Full attribution required in attribution.md

---

## Image Download and Naming

### **Filename Convention:**

**AI-Generated Images (Gemini):**
```
Pattern: [subject]_ai_[number].png

Examples:
- black_swan_ai_01.png
- black_swan_ai_02.png
- risk_matrix_ai_01.png
- dice_probability_ai_01.png
- question_mark_icon_ai_01.png

Always PNG format (Gemini default)
Always includes "_ai_" infix for clear identification
```

**Real Photos (Perplexity):**
```
Pattern: [subject]_[number].[ext]

Examples:
- warren_buffett_portrait_01.jpg
- warren_buffett_portrait_02.jpg
- berkshire_logo_01.png
- nyse_building_01.jpg

Preserves original format (jpg, png, svg, etc.)
No "_ai_" infix
```

**Naming Rules:**
- Lowercase only
- Replace spaces with underscores
- Remove special characters (!@#$%^&*()+={}[]|;:'",<>?/)
- Keep hyphens in compound words if needed
- Max 50 characters for subject (truncate if longer)
- Sequential numbering starts at 01
- Preserve file extensions from source

### **Download Process:**

**For Gemini (AI-Generated):**
```
1. Construct style-specific prompt
2. Call Gemini API with prompt + negative prompt
3. Extract imageUri from response
4. Download PNG file from Google Cloud Storage URL
5. Generate filename: [subject]_ai_01.png
6. Save to: Week-X/Video-Y/assets/
7. Verify: Check file size > 0, valid PNG header
8. Add entry to attribution.md (AI-generated section)
```

**For Perplexity (Real Photos):**
```
1. Construct search prompt (person/brand specific)
2. Call Perplexity API
3. Extract image URLs from response
4. Download each image
5. Detect format from headers or URL
6. Generate filename: [subject]_01.[ext]
7. Save to: Week-X/Video-Y/assets/
8. Verify: Check file size > 0, valid image file
9. Add full attribution entry to attribution.md
```
- Lowercase
- Replace spaces with underscores
- Remove special characters
- Keep original file extension
- Sequential numbering
- Max filename length: 50 characters (truncate subject if needed)
```

---

## Attribution Tracking

### **File: assets/attribution.md Structure:**

```markdown
# Image Attribution

This file tracks all images used in this video.

---

## AI-Generated Images

### black_swan_ai_01.png

**Source:** AI-generated (Gemini Imagen 3.0)
**Generation Date:** 2024-01-15
**Prompt:** "Hand-drawn illustration in Excalidraw style, black and white line art, A black swan bird on water, side view"
**License:** User owns rights (No copyright)
**Attribution Required:** No

**Usage in Video:**
- Frame 5: Illustrating Black Swan events concept

**Note:** AI-generated image for conceptual illustration

---

### risk_matrix_ai_01.png

**Source:** AI-generated (Gemini Imagen 3.0)
**Generation Date:** 2024-01-15
**Prompt:** "Hand-drawn illustration in Excalidraw style, black and white line art, 2x2 risk matrix diagram"
**License:** User owns rights (No copyright)
**Attribution Required:** No

**Usage in Video:**
- Frame 3: Risk categorization framework

---

## Real Photos & Licensed Images

### warren_buffett_portrait_01.jpg

**Source:** Wikimedia Commons
**URL:** https://commons.wikimedia.org/wiki/File:Warren_Buffett_2011.jpg
**Author:** Mark Hirschey
**License:** CC BY-SA 2.0
**Attribution Required:** Yes

**Attribution Text:**
"Warren Buffett" by Mark Hirschey, licensed under CC BY-SA 2.0, via Wikimedia Commons

**Usage in Video:**
- Frame 1: Opening quote slide

**Date Added:** 2024-01-15

---

### berkshire_logo_01.png

**Source:** Berkshire Hathaway Official Website
**URL:** https://www.berkshirehathaway.com
**Author:** Berkshire Hathaway Inc.
**License:** Fair Use (Educational)
**Attribution Required:** Yes

**Attribution Text:**
Berkshire Hathaway logo used under Fair Use for educational purposes

**Usage in Video:**
- Frame 2: Company example

**Date Added:** 2024-01-15

---

## Video Credits Summary

**For video end credits, include:**

AI-Generated Imagery:
- Select illustrations created with Gemini AI for educational purposes

Image Credits:
- Warren Buffett photo by Mark Hirschey (CC BY-SA 2.0), via Wikimedia Commons
- Berkshire Hathaway logo used under Fair Use

---

*Last updated: 2024-01-15*
```

### **Attribution Entry Templates:**

**For AI-Generated Images:**
```markdown
### [filename]_ai_[number].png

**Source:** AI-generated (Gemini Imagen 3.0)
**Generation Date:** [YYYY-MM-DD]
**Prompt:** [Truncated prompt used]
**License:** User owns rights (No copyright)
**Attribution Required:** No

**Usage in Video:**
- [Frame X: Description]

**Note:** AI-generated image for conceptual illustration
```

**For Real Photos:**
```markdown
### [filename]_[number].[ext]

**Source:** [Platform/Website name]
**URL:** [Direct link]
**Author:** [Creator name]
**License:** [License type]
**Attribution Required:** [Yes/No]

**Attribution Text:**
[Exact attribution wording]

**Usage in Video:**
- [Frame X: Description]

**Date Added:** [YYYY-MM-DD]
```

---

## License Detection

### **License Identification Logic:**

Parse Perplexity response content for keywords:

**Creative Commons:**
- "CC0" or "CC Zero" → Public Domain Dedication
- "CC BY" → Attribution required
- "CC BY-SA" → Attribution + ShareAlike
- "CC BY-ND" → Attribution + NoDerivatives
- "CC BY-NC" → Attribution + NonCommercial

**Other Commons:**
- "Public Domain" → No attribution required (but nice to include)
- "Wikimedia Commons" → Check specific license on page
- "Unsplash" → Unsplash License (free, no attribution required)
- "Pexels" → Pexels License (free, no attribution required)

**Commercial/Restricted:**
- "All Rights Reserved" → Do NOT download, warn user
- "Getty Images" → Do NOT download, warn user
- "Shutterstock" → Do NOT download, warn user
- No license info → Warn user, ask for confirmation before downloading

---

## User Response Format

### **After Successful AI Generation (Gemini):**

```
✓ Generated 2 images for "black swan" in hand-drawn B&W style

Images saved to: Week-1/Video-1/assets/

1. black_swan_ai_01.png (1920x1080, 187 KB)
   Source: AI-generated (Gemini)
   Style: Hand-drawn, black & white, Excalidraw-compatible
   Attribution: Not required
   
2. black_swan_ai_02.png (1920x1080, 192 KB)
   Source: AI-generated (Gemini)
   Style: Alternative angle, same hand-drawn style
   Attribution: Not required

Added to attribution.md: Week-1/Video-1/assets/attribution.md

Usage suggestions:
- black_swan_ai_01.png: Best match for Excalidraw style (side view)
- black_swan_ai_02.png: Alternative composition

To use in Excalidraw:
1. Open diagram file
2. Insert image (Ctrl+Shift+I or drag-and-drop)
3. Image style already matches your hand-drawn frames
4. No attribution needed (AI-generated)

To use in Marp slides:
![Black Swan Concept](assets/black_swan_ai_01.png)
```

### **After Successful Real Photo Download (Perplexity):**

```
✓ Found and downloaded 3 photos of "Warren Buffett"

Images saved to: Week-1/Video-1/assets/

1. warren_buffett_portrait_01.jpg (2400x3000, 456 KB)
   Source: Wikimedia Commons (CC BY-SA 2.0)
   Author: Mark Hirschey
   Attribution: REQUIRED
   Quality: High resolution, professional

2. warren_buffett_portrait_02.jpg (1920x1280, 312 KB)
   Source: Wikimedia Commons (CC BY 3.0)
   Author: Fortune Live Media
   Attribution: REQUIRED
   Quality: Good resolution, recent

3. warren_buffett_portrait_03.jpg (1600x2000, 289 KB)
   Source: Berkshire Hathaway (Fair Use - Educational)
   Attribution: REQUIRED (Fair Use notice)
   Quality: Official company photo

Attribution details added to: Week-1/Video-1/assets/attribution.md

Recommendation: Use warren_buffett_portrait_01.jpg (highest quality, clear licensing)

Attribution text (ready to use):
"Warren Buffett" by Mark Hirschey, licensed under CC BY-SA 2.0, via Wikimedia Commons

To use in Excalidraw:
1. Insert image (Ctrl+Shift+I)
2. Note: Real photo won't match hand-drawn style, but authentic
3. Consider cropping to focus on face

To use in Marp slides:
![Warren Buffett](assets/warren_buffett_portrait_01.jpg)
*Photo: Mark Hirschey (CC BY-SA 2.0)*
```

### **Mixed Request (Multiple Subjects):**

```
✓ Processed 3 image requests for Week-2/Video-4

Images saved to: Week-2/Video-4/assets/

AI-Generated (hand-drawn B&W style):
1. black_swan_ai_01.png (black swan illustration)
2. dice_probability_ai_01.png (dice showing probability)

Real Photos (attribution required):
3. warren_buffett_portrait_01.jpg (Warren Buffett photo)

Summary:
- 2 AI-generated images (no attribution needed)
- 1 real photo (attribution required - see attribution.md)

All details in: Week-2/Video-4/assets/attribution.md
```

---

## Error Handling

### **Common Failure Scenarios:**

**1. No images found**
```
✗ No suitable images found for "obscure technical term"

Suggestions:
- Try a more common search term
- Search for a related concept
- Specify image type: "diagram of obscure technical term"
```

**2. Download failure**
```
⚠ Found 3 images but could only download 1

Downloaded:
- black_swan_01.jpg ✓

Failed:
- URL 2: Access denied (403)
- URL 3: File not found (404)

Successfully downloaded images are available in assets/
```

**3. License unclear**
```
⚠ Found 2 images but license is unclear

black_swan_01.jpg: Downloaded (Wikimedia Commons, CC BY-SA 4.0) ✓
black_swan_02.jpg: NOT downloaded - unclear license

Recommendation: Manually verify license before using image 2
URL: https://example.com/image
```

**4. Video folder not found**
```
✗ Error: Could not find Week-1/Video-1/

Available video folders:
- Week-1/Video-1
- Week-1/Video-2
- Week-1/Video-3

Please specify the correct video folder.
```

---

## Integration with Workflow

### **When User Needs Images:**

**Scenario 1: Conceptual image (AI-generated)**
```
User: "I'm planning frames for the black swan concept video. 
       Get me a black swan image for Week-2/Video-3"

Claude Code:
1. Detects: "black swan" = abstract concept → Use Gemini
2. Generates hand-drawn, B&W image with Gemini API
3. Saves as: black_swan_ai_01.png to Week-2/Video-3/assets/
4. Adds entry to attribution.md (AI-generated section)
5. Response: "Generated image matches your Excalidraw style, no attribution needed"
```

**Scenario 2: Person photo (real photo)**
```
User: "I need Warren Buffett portrait for Week-1/Video-1"

Claude Code:
1. Detects: Person's name → Use Perplexity
2. Searches for real photos (Wikimedia Commons, official sources)
3. Downloads top 2-3 to Week-1/Video-1/assets/
4. Names: warren_buffett_portrait_01.jpg, etc.
5. Adds full attribution entries to attribution.md
6. Response: "Downloaded 3 photos, attribution required. Use portrait_01.jpg (best quality)"
```

**Scenario 3: Mixed request**
```
User: "For Week-1/Video-5 I need:
       - Risk matrix diagram
       - Warren Buffett portrait
       - Dice showing probability"

Claude Code:
1. risk_matrix: AI-generate (Gemini) → risk_matrix_ai_01.png
2. Warren Buffett: Search (Perplexity) → warren_buffett_portrait_01.jpg
3. dice: AI-generate (Gemini) → dice_probability_ai_01.png
4. Updates attribution.md with all entries (separated by type)
5. Response: Summary showing 2 AI-generated (no attribution) + 1 real photo (attribution required)
```

**Scenario 4: Updating attribution later**
```
User: "I used black_swan_ai_01.png in Frame 5 of my video"

Claude Code:
1. Opens assets/attribution.md
2. Finds black_swan_ai_01.png entry under "AI-Generated Images"
3. Updates "Usage in Video" field
4. Confirms update
```

---

## File Organization

### **Assets Folder Structure:**

```
Week-1/
└── Video-1/
    ├── assets/
    │   ├── diagram.excalidraw               # Main diagram source
    │   ├── frame_01.png                     # Exported frames
    │   ├── frame_02.png
    │   ├── black_swan_ai_01.png             # [NEW] AI-generated image
    │   ├── black_swan_ai_02.png             # [NEW] AI-generated alternative
    │   ├── warren_buffett_portrait_01.jpg   # [NEW] Real photo (downloaded)
    │   ├── warren_buffett_portrait_02.jpg   # [NEW] Real photo alternative
    │   └── attribution.md                   # [NEW] Attribution tracking (both types)
    ├── visual_context.md                    # Perplexity context
    ├── script.md                            # Frame timing
    └── final_video.mp4

Week-2/
└── Video-3/
    ├── assets/
    │   ├── risk_matrix_ai_01.png            # AI-generated diagram
    │   ├── dice_probability_ai_01.png       # AI-generated illustration
    │   ├── buffett_munger_photo_01.jpg      # Real photo
    │   └── attribution.md                   # Mixed attribution
    └── ...
```

**Naming pattern makes it clear:**
- `*_ai_*.png` = AI-generated (no attribution needed)
- `*_01.jpg/png` = Real photo (attribution required)


---

## Advanced Features

### **Feature 1: Image Quality Check**

After download, verify:
- Minimum resolution: 1920x1080 (warn if lower)
- File size: 50KB - 10MB (warn if outside range)
- Valid image format (not corrupted)
- Aspect ratio reasonable (not extremely stretched)

```
⚠ black_swan_03.jpg is only 800x600 (below recommended 1920x1080)
   May appear pixelated in video. Consider using black_swan_01.jpg instead.
```

### **Feature 2: Duplicate Detection**

Before downloading, check if similar image already exists:
```
ℹ Similar image already exists: black_swan_01.jpg (downloaded 2024-01-10)
  Download anyway? (y/n)
```

### **Feature 3: Bulk Download**

Support comma-separated requests:
```
User: "Get images of: Warren Buffett, Charlie Munger, Benjamin Graham"

Claude Code downloads 2-3 images of each person
```

### **Feature 4: Citation Export**

Generate formatted citations for video credits:
```
User: "Generate citations for final video credits"

Claude Code outputs:
---
Image Credits:
- Black Swan photo by John Smith (CC BY-SA 4.0), via Wikimedia Commons
- Warren Buffett photo courtesy of Berkshire Hathaway Inc.
- Efficient Frontier diagram adapted from Dr. Jane Doe (CC BY 4.0)
---
```

---

## Safety & Copyright

### **Critical Rules:**

1. **NEVER download images without license information**
   - If license unclear, WARN USER and skip download
   - Better to skip than to violate copyright

2. **Prioritize free/open licenses**
   - CC0, Public Domain first
   - CC-BY, CC-BY-SA second
   - Fair Use (educational) third
   - Never download commercial/All Rights Reserved

3. **Always provide attribution**
   - Even when not required (except CC0)
   - Give proper credit to creators
   - Include license type

4. **Verify source authenticity**
   - Wikimedia Commons > random blogs
   - Official websites > third-party aggregators
   - Reputable stock photo sites > unknown sources

5. **Educational use disclaimer**
   - All images used under Fair Use (educational purposes)
   - Non-commercial context
   - Transformative (explained in context of finance education)

---

## Example Interactions

### **Example 1: AI-Generated Image (Default for Concepts)**

```
User: I need a black swan image for Video 3

Claude Code:
Detected: Abstract concept → Generating with Gemini AI
Style: Hand-drawn, black & white, Excalidraw-compatible

✓ Generated 2 images

Saved to: Week-1/Video-3/assets/

1. black_swan_ai_01.png (1920x1080, 189 KB)
   Style: Side view, simple line art, matches your Excalidraw frames
   Attribution: Not required (AI-generated)
   
2. black_swan_ai_02.png (1920x1080, 194 KB)
   Style: Alternative angle, same hand-drawn aesthetic
   Attribution: Not required (AI-generated)

Added to attribution.md (AI-generated section)

Recommendation: Use black_swan_ai_01.png - best fits Excalidraw style
```

---

### **Example 2: Real Photo (Person)**

```
User: Find me a high-quality portrait of Warren Buffett for the opening frame

Claude Code:
Detected: Person's name → Searching for real photos via Perplexity

Searching Wikimedia Commons and official sources...
✓ Found 3 suitable photos

Downloaded to: Week-1/Video-1/assets/

1. warren_buffett_portrait_01.jpg (2400x3000, 456 KB)
   Source: Wikimedia Commons
   License: CC BY-SA 2.0
   Author: Mark Hirschey
   Attribution: REQUIRED ✓
   
2. warren_buffett_portrait_02.jpg (1920x1280, 312 KB)
   Source: Wikimedia Commons
   License: CC BY 3.0
   Author: Fortune Live Media
   Attribution: REQUIRED ✓

3. warren_buffett_portrait_03.jpg (1600x2000, 289 KB)
   Source: Official Berkshire Hathaway
   License: Fair Use (Educational)
   Attribution: REQUIRED ✓

All attribution details added to: attribution.md

Recommendation: Use portrait_01.jpg (highest quality, clear CC license)

Attribution text (ready to use):
"Warren Buffett" by Mark Hirschey (CC BY-SA 2.0), via Wikimedia Commons
```

---

### **Example 3: Mixed Request (AI + Real Photos)**

```
User: Get me images for Week-2/Video-4: 
      - Risk matrix diagram
      - Warren Buffett portrait
      - Dice showing probability

Claude Code:
Processing 3 image requests...

[1/3] Risk matrix diagram (abstract concept → AI-generate)
✓ Generated with Gemini
  - risk_matrix_ai_01.png (hand-drawn B&W style)
  - No attribution needed

[2/3] Warren Buffett portrait (person → real photo)
✓ Found 2 photos via Perplexity
  - warren_buffett_portrait_01.jpg (Wikimedia, CC BY-SA 2.0)
  - Attribution REQUIRED

[3/3] Dice showing probability (abstract → AI-generate)
✓ Generated with Gemini
  - dice_probability_ai_01.png (hand-drawn B&W style)
  - No attribution needed

Saved to: Week-2/Video-4/assets/

Summary:
- 2 AI-generated images (hand-drawn style, no attribution)
- 1 real photo (professional quality, attribution required)

All details in: Week-2/Video-4/assets/attribution.md

Usage suggestions:
- Frames 2-3: risk_matrix_ai_01.png (matches your diagram style)
- Frame 1: warren_buffett_portrait_01.jpg (opening quote)
- Frame 4: dice_probability_ai_01.png (probability concept)
```

---

## Testing Checklist

### **Implementation Complete When:**

**Core Functionality:**
- ✅ Can detect whether to use Gemini (AI) or Perplexity (real photo)
- ✅ Constructs appropriate Gemini prompts with hand-drawn B&W style
- ✅ Constructs appropriate Perplexity prompts for people/brands
- ✅ Generates images with Gemini API successfully
- ✅ Downloads real photos from Perplexity results
- ✅ Generates correct filenames (_ai_ infix for AI-generated)
- ✅ Creates/updates attribution.md with separate sections
- ✅ Handles both types in mixed requests

**Quality & Safety:**
- ✅ AI-generated images match Excalidraw hand-drawn B&W style
- ✅ Detects and warns about license issues for real photos
- ✅ Never generates people's likenesses with AI
- ✅ Quality checks for resolution and file size
- ✅ Handles errors gracefully (API failures, download issues)
- ✅ Provides clear, actionable user feedback
- ✅ Supports multiple images per request

---

## Priority Implementation Order

1. **Phase 1 (Core - Gemini AI):**
   - Set up Gemini API connection (GEMINI_API_KEY from .env)
   - Implement hand-drawn B&W style prompt construction
   - Test image generation with sample subjects
   - Implement download from Gemini storage URLs
   - Create attribution.md entries for AI-generated images

2. **Phase 2 (Core - Perplexity Real Photos):**
   - Set up Perplexity API connection (PERPLEXITY_API_KEY from .env)
   - Implement person/brand detection logic
   - Implement real photo search and download
   - Create attribution.md entries for real photos with full licensing

3. **Phase 3 (Integration):**
   - Implement auto-detection (AI vs real photo)
   - Handle mixed requests (multiple subjects, different types)
   - Unified attribution.md with both sections
   - Filename conventions (_ai_ infix vs standard)

4. **Phase 4 (Quality & UX):**
   - License detection and warnings for real photos
   - Image quality checks (resolution, file size)
   - Better error messages and suggestions
   - Bulk requests support

5. **Phase 5 (Polish):**
   - Duplicate detection
   - Citation export for video credits
   - Usage tracking in attribution.md
   - Style consistency checks for AI-generated images

---

## Configuration

### **Settings (in .env file):**

```bash
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Gemini Settings
GEMINI_MODEL=imagen-3.0-generate-001
GEMINI_IMAGES_PER_REQUEST=2
GEMINI_ASPECT_RATIO=16:9

# Image Quality Settings
MIN_IMAGE_WIDTH=1920
MIN_IMAGE_HEIGHT=1080
MAX_FILE_SIZE_MB=10

# License Preferences (for Perplexity downloads)
LICENSE_PRIORITY=CC0,Public Domain,CC-BY,CC-BY-SA,Fair Use

# Attribution Settings
ATTRIBUTION_FILE=attribution.md
ALWAYS_ATTRIBUTE_REAL_PHOTOS=true
INCLUDE_AI_DISCLOSURE=true
```

---

## Notes for Claude Code

**Critical Implementation Points:**

1. **Always check if subject is a person/brand FIRST**
   - If yes → Use Perplexity (real photo)
   - If no → Use Gemini (AI-generated)

2. **Gemini prompts MUST include hand-drawn B&W style descriptor**
   - Base prompt: "Hand-drawn illustration in Excalidraw style, black and white line art..."
   - Never skip this - style consistency is critical

3. **Never AI-generate people's likenesses**
   - Use `"personGeneration": "DONT_ALLOW"` in Gemini request
   - Even if user asks, redirect to real photo search

4. **Attribution is different for each type:**
   - AI-generated: Simple note, no legal requirement
   - Real photos: Full attribution with license details

5. **Filenames must be distinguishable:**
   - `*_ai_*.png` = AI-generated
   - `*_01.jpg` = Real photo

6. **Error handling priorities:**
   - Gemini API failure → Inform user, suggest manual creation
   - Perplexity API failure → Suggest alternative search terms
   - Download failure → Report specific URLs that failed

7. **This is on-demand, not automated:**
   - User triggers when needed during frame creation
   - Focus on reliability over speed
   - Clear communication > automation complexity

---

## Configuration

### **Settings (can be in .env or config file):**

```
# Image search settings
DEFAULT_IMAGE_COUNT=3
MIN_IMAGE_WIDTH=1920
MIN_IMAGE_HEIGHT=1080
MAX_FILE_SIZE_MB=10
PREFERRED_FORMATS=jpg,png,svg,webp

# License preferences (priority order)
LICENSE_PRIORITY=CC0,Public Domain,CC-BY,CC-BY-SA,Unsplash,Fair Use

# Attribution settings
ATTRIBUTION_FILE=attribution.md
ALWAYS_ATTRIBUTE=true
```

---

## Notes for Claude Code

- This is an **on-demand feature**, not part of automated weekly workflow
- User will request images **when needed during frame creation**
- Focus on **reliability and copyright safety** over speed
- **Always prefer free/open licenses** to minimize legal risk
- **Clear error messages** are critical (user needs to know why download failed)
- **Suggest alternatives** when primary search doesn't work well

---

## Summary

### **Dual-Source Approach:**

**Gemini AI (Default for Concepts):**
- ✅ Generates hand-drawn, black & white images
- ✅ Matches Excalidraw aesthetic perfectly
- ✅ No attribution required (user owns rights)
- ✅ Instant generation, unlimited variations
- ✅ Perfect for: diagrams, icons, animals, objects, abstract concepts

**Perplexity Search (For People & Brands):**
- ✅ Finds real, authentic photos
- ✅ Proper licensing from Wikimedia Commons, official sources
- ✅ Higher trust and recognition
- ✅ Full attribution tracking
- ✅ Perfect for: Warren Buffett, company logos, historical photos

### **Key Benefits:**

1. **Style consistency:** AI-generated images match your hand-drawn Excalidraw frames
2. **Legal safety:** Real photos have clear licenses, AI-generated have no copyright issues
3. **Efficiency:** AI generation is instant, no need to search/download for concepts
4. **Quality:** Real photos for people ensure authenticity and trust
5. **Attribution clarity:** Separate tracking for AI vs real photos

### **Typical Usage:**

```
Week-1/Video-1:
✓ Black swan concept → AI-generated (black_swan_ai_01.png)
✓ Warren Buffett quote → Real photo (warren_buffett_portrait_01.jpg)
✓ Risk matrix diagram → AI-generated (risk_matrix_ai_01.png)
✓ Dice illustration → AI-generated (dice_probability_ai_01.png)

Result: 3 AI-generated (no attribution) + 1 real photo (attribution required)
Time saved: ~15 minutes vs manual search for all 4 images
Style: Consistent hand-drawn aesthetic throughout video
```

---

*End of Specification*
