import sys
import os

def check_paths():
    """Print important path information for debugging"""
    print("Python Path (sys.path):")
    for p in sys.path:
        print(f"  - {p}")
    
    print("\nCurrent Directory:", os.getcwd())
    
    print("\nEnvironment Variables:")
    for key, value in os.environ.items():
        if key.startswith('PYTHON') or key == 'PATH':
            print(f"  - {key}: {value}")
    
    try:
        import app
        print("\nApp package found at:", app.__file__)
    except ImportError as e:
        print(f"\nError importing app: {e}")
    
    try:
        from app import services
        print("\nServices package found at:", services.__file__)
    except ImportError as e:
        print(f"\nError importing services: {e}")
    
    print("\nDirectory Structure:")
    for root, dirs, files in os.walk('.', topdown=True, followlinks=False):
        level = root.count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if f.endswith('.py'):
                print(f"{sub_indent}{f}")

if __name__ == "__main__":
    check_paths()
