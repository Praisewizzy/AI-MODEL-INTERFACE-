import os
import sys
import json
import urllib.request
import urllib.error

KEY_FILE = os.path.expanduser("~/.agentrouter_key")

MODELS = {
    "1": ("ChatGPT (GPT-4o)", "gpt-4o"),
    "2": ("Claude 3.7 Sonnet", "claude-sonnet-4-5-20250929"),
    "3": ("Google Gemini 3 Pro", "gemini-3-pro-preview"),
    "4": ("DeepSeek R1", "deepseek-r1"),
}

def get_api_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = f.read().strip()
            if key:
                return key

    print("\n--- FIRST TIME SETUP ---")
    key = input("Enter YOUR AgentRouter API Key (sk-...): ").strip()
    if not key:
        print("API Key is required!")
        sys.exit(1)
    
    with open(KEY_FILE, "w") as f:
        f.write(key)
    print("API Key saved locally!\n")
    return key

def ask_ai(api_key, model_id, prompt):
    url = "https://agentrouter.org/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}]
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return f"HTTP Error {e.code}: {error_body}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("=" * 40)
    print("      MULTI-MODEL AI TERMINAL       ")
    print("=" * 40)

    api_key = get_api_key()

    print("\nSelect a model:")
    for key, (name, _) in MODELS.items():
        print(f"[{key}] {name}")
    
    choice = input("\nEnter choice (1-4, default=1): ").strip() or "1"
    selected_model = MODELS.get(choice, MODELS["1"])[1]
    selected_name = MODELS.get(choice, MODELS["1"])[0]

    print(f"\nConnected to: {selected_name}")
    print("Commands: 'exit' to quit | 'switch' to change model | 'reset-key' to update key\n" + "-" * 40)

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit"]:
            break
        elif user_input.lower() == "switch":
            return main()
        elif user_input.lower() == "reset-key":
            if os.path.exists(KEY_FILE):
                os.remove(KEY_FILE)
            return main()

        print("\nThinking...")
        answer = ask_ai(api_key, selected_model, user_input)
        print(f"\nAI ({selected_name}):\n{answer}")

if __name__ == "__main__":
    main()
