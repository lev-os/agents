#!/usr/bin/env python3
"""
Embed text using Ollama nomic-embed-text.
Groq does not support embeddings, so we use local Ollama.
"""
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Embed text using Ollama")
    parser.add_argument("text", nargs="?", help="Text to embed (or read from stdin)")
    parser.add_argument("--model", "-m", default="nomic-embed-text", help="Ollama embedding model")
    parser.add_argument("--host", default="http://localhost:11434", help="Ollama host")
    args = parser.parse_args()

    # Get text from args or stdin
    text = args.text
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            print("Error: No text provided", file=sys.stderr)
            sys.exit(1)

    try:
        import requests
    except ImportError:
        print("Error: requests package not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    try:
        response = requests.post(
            f"{args.host}/api/embeddings",
            json={
                "model": args.model,
                "prompt": text
            },
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        embedding = data.get("embedding", [])

        # Output as JSON array
        print(json.dumps(embedding))

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Ollama. Is it running? (ollama serve)", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Ollama request timed out", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error: Model '{args.model}' not found. Run: ollama pull {args.model}", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
