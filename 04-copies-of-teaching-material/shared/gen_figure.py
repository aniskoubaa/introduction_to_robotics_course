#!/usr/bin/env python3
"""
Generate a lecture figure with Gemini 3 Pro Image.

    python3 gen_figure.py <out.png> <prompt-file.txt>

The prompt file is kept beside the image (`<name>.prompt.txt`) so any figure in
this course can be regenerated or restyled consistently -- same standing rule as
the SE 100 decks.

Requires GEMINI_API_KEY in the environment.
"""
import base64, json, os, sys, urllib.request

MODEL = "gemini-3-pro-image"
HOUSE = (
    " Editorial illustration for a university engineering lecture slide. "
    "Restrained, professional, no text, no logos, no watermarks, no brand marks, "
    "no identifiable real people. Palette built on deep navy (#0A2540), indigo "
    "(#635BFF) and cyan (#00D4FF) against a light neutral background. Clean, "
    "well-lit, uncluttered composition with clear negative space. 16:9."
)

def main(out, prompt_file):
    prompt = open(prompt_file).read().strip() + HOUSE
    key = os.environ["GEMINI_API_KEY"]
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{MODEL}:generateContent?key={key}")
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "16:9"},
        },
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)

    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline:
                open(out, "wb").write(base64.b64decode(inline["data"]))
                print(f"OK  {out}  ({os.path.getsize(out)//1024} KB)")
                return
    print("NO IMAGE RETURNED:", json.dumps(data)[:600], file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
