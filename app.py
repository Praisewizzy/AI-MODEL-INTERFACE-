import os
import sys
from openai import OpenAI

# File path to save the user's personal API key locally
KEY_FILE = os.path.expanduser("~/.agentrouter_key")

MODELS = {
    "1": ("ChatGPT (GPT-4o)", "gpt-4o"),
    "2": ("Claude 3.7 Sonnet", "claude-sonnet-4-5-20250929"),
    "3": ("Google Gemini 3 Pro", "gemini-3-pro-preview"),
    "4": ("DeepSeek R1", "deepseek-r1"),
}

def get_api_key():
    # 1. Check system environment variables
    api_key = os.getenv("AGENTROUTER_API_KEY")
    if api_key:
        return api_key
    
    # 2. Check local key file
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = f.read().strip()
            if key:
                return key

    # 3. Prompt user for their own key if none found
    print("\n--- FIRST TIME SETUP ---")
    key = input("Please enter YOUR AgentRouter API Key (sk-...): ").strip()
    if not key:
        print("Error: API Key is required to run this program.")
        sys.exit(1)
    
    # Save key locally for future runs
    with open(KEY_FILE, "w") as f:
        f.write(key)
    print("API Key saved locally!\n")
    return key

def main():
    print("=" * 40)
    print("      MULTI-MODEL AI TERMINAL       ")
    print("=" * 40)

    api_key = get_api_key()

    client = OpenAI(
        base_url="https://agentrouter.org/v1",
        api_key=api_key
    )

    print("\nSelect a model to start:")
    for key, (name, _) in MODELS.items():
        print(f"[{key}] {name}")
    
    choice = input("\nEnter choice (1-4, default=1): ").strip() or "1"
    selected_model = MODELS.get(choice, MODELS["1"])[1]
    selected_name = MODELS.get(choice, MODELS["1"])[0]

    print(f"\nConnected to: {selected_name}")
    print("Type 'exit' to quit, 'switch' to change models, or 'reset-key' to update key.\n" + "-" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            elif user_input.lower() == "switch":
                return main()
            elif user_input.lower() == "reset-key":
                if os.path.exists(KEY_FILE):
                    os.remove(KEY_FILE)
                print("Saved key removed. Restarting setup...")
                return main()

            response = client.chat.completions.create(
                model=selected_model,
                messages=[{"role": "user", "content": user_input}]
            )

            answer = response.choices[0].message.content
            print(f"\nAI ({selected_name}):\n{answer}")

        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
