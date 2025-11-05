
#openrouter_terminal_bot.py
#Terminal chatbot + code generator using OpenRouter (qwen/qwen3-4b:free).
#Set environment variable OPENROUTER_API_KEY or create a .env file with OPENROUTER_API_KEY=sk-...


import os
import sys
import json
import re
import time
from typing import List, Dict, Any
import requests

# Config
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "qwen/qwen3-4b:free"  # model to use
API_KEY = ""#API key 


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # Optional: set user-agent or OpenRouter-specific headers if desired
    "User-Agent": "openrouter-terminal-bot/1.0"
}

CHAT_LOG_PATH = "chat_log.jsonl"

# Basic helpers
def save_chat_line(obj: Dict[str, Any]):
    try:
        with open(CHAT_LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[!] failed to write chat log: {e}")

def call_openrouter(messages, temperature=0.2, max_tokens=1024):
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    for attempt in range(3):  # try up to 3 times
        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        
        if resp.status_code == 429:
            wait_time = 3 + attempt * 3  # backoff: 3s, 6s, 9s
            print(f"\n[rate limited] waiting {wait_time}s...")
            time.sleep(wait_time)
            continue
        
        resp.raise_for_status()
        return resp.json()

    # fallback to a different free model
    fallback_model = "mistralai/Mistral-7B-Instruct:free"
    print(f"\n[switching to fallback model: {fallback_model}]")

    payload["model"] = fallback_model
    resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()




def prompt_save_code_blocks(blocks):
    for i, b in enumerate(blocks, start=1):
        lang = b["lang"] or "txt"
        suggested = f"generated_code_{int(time.time())}_{i}.{lang or 'txt'}"
        print("\n--- Detected code block ---")
        print(f"Language: {lang or '(unspecified)'}")
        print("Preview (first 20 lines):")
        for ln in b["code"].splitlines()[:20]:
            print("   " + ln)
        while True:
            ans = input(f"\nSave this block to file [{suggested}]? (y/n) ").strip().lower()
            if ans in ("y", "yes"):
                fn = input(f"Filename (enter to use {suggested}): ").strip() or suggested
                try:
                    with open(fn, "w", encoding="utf-8") as fh:
                        fh.write(b["code"])
                    print(f"[+] saved to {fn}")
                except Exception as e:
                    print(f"[!] could not save file: {e}")
                break
            if ans in ("n", "no"):
                break
            print("Please answer y or n.")

def nice_print_role(role: str):
    if role == "assistant":
        return "BOT"
    return role.upper()

def main():
    print("OpenRouter terminal chatbot — model:", MODEL_NAME)
    print("Type '/exit' to quit, '/clear' to clear history, '/save' to save history now.")
    messages: List[Dict[str,str]] = [
        {"role": "system", "content": "You are a helpful assistant. When asked to produce code, return code inside fenced code blocks."}
    ]

    while True:
        try:
            user_input = input("\nYou: ").rstrip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd = user_input[1:].strip().lower()
            if cmd == "exit":
                print("Bye.")
                break
            if cmd == "clear":
                messages = [messages[0]]
                print("[history cleared]")
                continue
            if cmd == "save":
                save_chat_line({"ts": time.time(), "action": "manual_save", "messages": messages})
                print(f"[saved to {CHAT_LOG_PATH}]")
                continue
            print("[unknown command]", cmd)
            continue

        # append user message
        messages.append({"role": "user", "content": user_input})
        save_chat_line({"ts": time.time(), "role": "user", "content": user_input})

        # call API
        try:
            print("[sending to OpenRouter...]", end="", flush=True)
            jr = call_openrouter(messages)
            # Logging raw response
            save_chat_line({"ts": time.time(), "role": "assistant_raw", "response": jr})

            # extract assistant reply (OpenAI-style response)
            assistant_text = ""
            if isinstance(jr, dict):
                # typical openrouter response: choices[0].message.content
                try:
                    assistant_text = jr["choices"][0]["message"]["content"]
                except Exception:
                    # fallback: look for other fields
                    assistant_text = jr.get("output") or jr.get("text") or json.dumps(jr)
            else:
                assistant_text = str(jr)

            messages.append({"role": "assistant", "content": assistant_text})
            save_chat_line({"ts": time.time(), "role": "assistant", "content": assistant_text})

            print("\r" + "-"*40)
            print(f"{nice_print_role('assistant')}:")
            print(assistant_text)
            print("-"*40)

            # code block detection & optional save
            
            # keep history size reasonable
            if len(messages) > 30:
                # keep system + last 24 messages
                messages = [messages[0]] + messages[-24:]
        except requests.HTTPError as he:
            print(f"\n[HTTP error] {he} - response: {getattr(he, 'response', None)}")
        except Exception as e:
            print(f"\n[error] {e}")

if __name__ == "__main__":
    main()
