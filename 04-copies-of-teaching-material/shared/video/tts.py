#!/usr/bin/env python3
"""Speaks the narration with Gemini text-to-speech, voice Algenib.

One WAV per line, cached: re-running only synthesises what changed, so a
reworded line costs one request instead of ninety-four.

    GEMINI_API_KEY=... python3 tts.py [--voice Algenib] [--model ...]
"""
import argparse, hashlib, json, os, struct, sys, time, wave

V = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(V, "voice")
RATE = 24000                      # Gemini TTS returns 16-bit mono PCM at 24 kHz

STYLE = ("Read the following as a university lab instructor narrating a "
         "screencast: calm, clear and unhurried, with a short pause at each "
         "full stop. Do not add anything.\n\n")


def pcm_to_wav(pcm, path, rate=RATE):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="Algenib")
    ap.add_argument("--model", default="gemini-2.5-flash-preview-tts")
    ap.add_argument("--only", default=None, help="synthesise one id")
    a = ap.parse_args()

    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("no GEMINI_API_KEY / GOOGLE_API_KEY in the environment")

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=key)

    lines = json.load(open(os.path.join(V, "narration.json")))
    os.makedirs(OUT, exist_ok=True)
    index_path = os.path.join(OUT, "index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else {}

    made = skipped = 0
    for ln in lines:
        if a.only and ln["id"] != a.only:
            continue
        sig = hashlib.sha1(
            (ln["text"] + a.voice + a.model + STYLE).encode()).hexdigest()[:16]
        path = os.path.join(OUT, ln["id"].replace(":", "_") + ".wav")
        if index.get(ln["id"]) == sig and os.path.exists(path):
            skipped += 1
            continue

        for attempt in range(5):
            try:
                r = client.models.generate_content(
                    model=a.model,
                    contents=STYLE + ln["text"],
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=a.voice)))),
                )
                pcm = r.candidates[0].content.parts[0].inline_data.data
                if not pcm:
                    raise RuntimeError("empty audio")
                pcm_to_wav(pcm, path)
                index[ln["id"]] = sig
                made += 1
                secs = len(pcm) / (RATE * 2)
                print(f"  {ln['id']:12} {secs:5.1f}s  {ln['text'][:60]}", flush=True)
                break
            except Exception as e:
                wait = 3 * (attempt + 1)
                print(f"  {ln['id']:12} retry {attempt+1}: {e}", flush=True)
                time.sleep(wait)
        else:
            print(f"  !! {ln['id']} failed")
        json.dump(index, open(index_path, "w"), indent=1)
        time.sleep(0.6)                      # stay under the free-tier rate limit

    # How long each line takes to say. run_demo.py pads each command's pause to
    # fit, and build.py sizes the title cards, so nothing is spoken over a cut.
    durs = {}
    for ln in lines:
        path = os.path.join(OUT, ln["id"].replace(":", "_") + ".wav")
        if not os.path.exists(path):
            continue
        with wave.open(path) as w:
            d = w.getnframes() / float(w.getframerate())
        durs[ln["id"]] = round(d, 2)
        if ln.get("source"):
            durs["src:" + ln["source"]] = round(d, 2)
        durs["txt:" + ln["text"]] = round(d, 2)
    json.dump(durs, open(os.path.join(OUT, "durations.json"), "w"), indent=1)
    total = sum(v for k, v in durs.items() if not k.startswith(("src:", "txt:")))
    print(f"\n{made} synthesised, {skipped} already cached -> {OUT}")
    print(f"total narration {int(total)//60} min {int(total)%60:02d} s")


if __name__ == "__main__":
    main()
