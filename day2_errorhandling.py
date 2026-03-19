# WITH error handling — crash is caught, app continues
# try:
#     score = "high"
#     result = score / 2    # this line fails
#     print("This won't run")
# except TypeError as e:
#     print(f"❌ Type error caught: {e}")

# print("✅ App continues running!")  # this DOES run

# def read_config(filename, key):
#     try:
#         with open(filename, "r") as file:
#             import json
#             config = json.load(file)
#             return config[key]

#     except FileNotFoundError:
#         return "❌ Config file not found"

#     except KeyError:
#         return f"❌ Key '{key}' not found in config"

#     except json.JSONDecodeError:
#         return "❌ Config file is not valid JSON"

# # Test all error types
# print(read_config("missing.json", "model"))        # FileNotFoundError
# print(read_config("sample.txt", "model"))          # JSONDecodeError


# def process_document(filepath):
#     file = None
#     try:
#         file = open(filepath, "r")
#         content = file.read()
#         print(f"✅ Read {len(content)} characters")
#         return content

#     except FileNotFoundError:
#         print(f"❌ File not found: {filepath}")
#         return None

#     finally:
#         # This ALWAYS runs — perfect for cleanup
#         print("🧹 Cleanup complete")
#         if file:
#             file.close()

# process_document("sample.txt")    # exists
# process_document("missing.txt")   # doesn't exist


# def set_temperature(value):
#     if not isinstance(value, (int, float)):
#         raise TypeError(f"Temperature must be a number, got {type(value)}")

#     if value < 0 or value > 2:
#         raise ValueError(f"Temperature must be between 0 and 2, got {value}")

#     return f"✅ Temperature set to {value}"

# # Test it
# try:
#     print(set_temperature(0.7))    # valid
#     print(set_temperature(3.5))    # invalid — too high
# except ValueError as e:
#     print(f"❌ {e}")

# try:
#     print(set_temperature("hot"))  # invalid — wrong type
# except TypeError as e:
#     print(f"❌ {e}")


# import time

# def call_llm_with_retry(prompt, max_retries=7, wait_seconds=2):
#     attempt = 0

#     while attempt < max_retries:
#         try:
#             print(f"🔄 Attempt {attempt + 1} — calling LLM...")

#             # Simulate random API failure
#             import random
#             if random.random() < 0.7:   # 70% chance of failure
#                 raise ConnectionError("API rate limit hit")

#             # Simulate success
#             response = f"Answer to: {prompt}"
#             print(f"✅ Success on attempt {attempt + 1}")
#             return response

#         except ConnectionError as e:
#             print(f"❌ Failed: {e}")
#             attempt += 1

#             if attempt < max_retries:
#                 print(f"⏳ Waiting {wait_seconds}s before retry...")
#                 time.sleep(wait_seconds)

#     return "❌ All retries exhausted — please try again later"


# # Test it
# result = call_llm_with_retry("What is RAG?", max_retries=3)
# print(f"\nFinal result: {result}")


# # Common errors you'll hit in Gen AI work

# try:
#     pass
# except FileNotFoundError:
#     pass   # PDF or config file missing

# except KeyError:
#     pass   # Missing key in API response dict

# except ValueError:
#     pass   # Wrong value — bad temperature, empty prompt

# except TypeError:
#     pass   # Wrong type passed to function

# except ConnectionError:
#     pass   # API unreachable — network issue

# except TimeoutError:
#     pass   # API took too long to respond

# except Exception as e:
#     # Catch-all — use only as last resort
#     print(f"Unexpected error: {e}")


import json
import time

# EXERCISE — Robust LLM config loader
# In production, your app loads an LLM config from a JSON file
# It must handle ALL the things that can go wrong

def load_llm_config(filepath):
    # TASK 1: Try to open and parse the JSON file
    try:
        with open(filepath, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"❌ Config file not found: {filepath}")
        return None

    except json.JSONDecodeError:
        print(f"❌ Config file is not valid JSON: {filepath}")
        return None
    # Catch FileNotFoundError — return None
    # Catch json.JSONDecodeError — return None
    # YOUR CODE HERE

def validate_config(config):
    # TASK 2: Check these 3 things — raise errors if wrong
    
    # a) "model" key must exist — raise KeyError if missing
    if "model" not in config:
        raise KeyError("❌ Config is missing 'model' key")

    # b) "temperature" must be between 0 and 2 — raise ValueError if not
    if not (0 <= config.get("temperature", 0) <= 2):
        raise ValueError("❌ Config 'temperature' must be between 0 and 2")

    # c) "max_tokens" must be a positive integer — raise ValueError if not
    max_tokens = config.get("max_tokens", 0)
    if not isinstance(max_tokens, int):
        raise ValueError("❌ Config 'max_tokens' must be an integer")
    if max_tokens <= 0:
        raise ValueError("❌ Config 'max_tokens' must be a positive integer")

    # If all valid — return "✅ Config is valid"
    return "✅ Config is valid"

def setup_llm(filepath):
    # Load the config
    config = load_llm_config(filepath)
    if config is None:
        return "❌ Failed to load config"

    # Validate it — catch whatever validate_config raises
    try:
        result = validate_config(config)
        return result   # "✅ Config is valid"

    except KeyError as e:
        return f"❌ Missing key: {e}"

    except ValueError as e:
        return f"❌ Invalid value: {e}"

    # Handle all possible errors and return helpful messages
    # YOUR CODE HERE


# Test with these cases
import json

# Create a valid config file
valid = {"model": "claude-3-sonnet", "temperature": 0.7, "max_tokens": 1024}
with open("valid_config.json", "w") as f:
    json.dump(valid, f)

# Create an invalid config file
invalid = {"model": "claude-3-sonnet", "temperature": 5.0, "max_tokens": -1}
with open("invalid_config.json", "w") as f:
    json.dump(invalid, f)

print(setup_llm("valid_config.json"))    # should pass
print(setup_llm("invalid_config.json"))  # should catch ValueError
print(setup_llm("missing_config.json"))  # should catch FileNotFoundError