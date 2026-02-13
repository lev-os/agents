#!/usr/bin/env python3
"""
Groq chat completion using llama-3.3-70b-versatile by default.
"""
import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Groq chat completion")
    parser.add_argument("prompt", nargs="?", help="User prompt (or read from stdin)")
    parser.add_argument("--system", "-s", default="You are a helpful assistant.", help="System prompt")
    parser.add_argument("--model", "-m", default="llama-3.3-70b-versatile", help="Model ID")
    parser.add_argument("--json", "-j", action="store_true", help="Request JSON output")
    parser.add_argument("--temperature", "-t", type=float, default=0.7, help="Temperature (0-2)")
    parser.add_argument("--max-tokens", type=int, default=4096, help="Max tokens in response")
    args = parser.parse_args()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Get prompt from args or stdin
    prompt = args.prompt
    if not prompt:
        if not sys.stdin.isatty():
            prompt = sys.stdin.read().strip()
        else:
            print("Error: No prompt provided", file=sys.stderr)
            sys.exit(1)

    try:
        from groq import Groq
    except ImportError:
        print("Error: groq package not installed. Run: pip install groq", file=sys.stderr)
        sys.exit(1)

    client = Groq(api_key=api_key)

    messages = [
        {"role": "system", "content": args.system},
        {"role": "user", "content": prompt}
    ]

    try:
        kwargs = {
            "model": args.model,
            "messages": messages,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        }

        if args.json:
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        print(content)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
