import sys
import os

# Add project root to path (cli/ -> root)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from core.engine.transliterator import Transliterator

def main():
    print("Initializing AdorLipi Engine...")
    try:
        engine = Transliterator()
        print("AdorLipi Ready! Type 'exit' to quit.")
        print("-" * 30)
    except Exception as e:
        print(f"Failed to initialize engine: {e}")
        return

    while True:
        try:
            user_input = input("\nEnter text:\n> ")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            
            if not user_input.strip():
                continue
                
            output = engine.transliterate(user_input)
            print(f"\nOutput:\n{output}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
