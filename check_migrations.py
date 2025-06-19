import os
import sys

def check_migrations_structure():
    """
    Check if the migrations directory structure is correct and print debug information
    """
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # List all directories in the current path
    print("\nDirectories in current path:")
    for item in os.listdir(current_dir):
        if os.path.isdir(os.path.join(current_dir, item)):
            print(f"- {item}")
    
    # Check if migrations directory exists
    migrations_path = os.path.join(current_dir, 'migrations')
    print(f"\nChecking migrations path: {migrations_path}")
    if os.path.exists(migrations_path):
        print("Migrations directory exists")
        
        # Check migrations contents
        print("\nContents of migrations directory:")
        for item in os.listdir(migrations_path):
            item_path = os.path.join(migrations_path, item)
            if os.path.isdir(item_path):
                print(f"- {item}/ (directory)")
            else:
                print(f"- {item} (file)")
                
        # Check specifically for env.py
        env_path = os.path.join(migrations_path, 'env.py')
        if os.path.exists(env_path):
            print("\nenv.py exists")
            print(f"env.py size: {os.path.getsize(env_path)} bytes")
            print(f"env.py permissions: {oct(os.stat(env_path).st_mode)[-3:]}")
        else:
            print("\nenv.py DOES NOT EXIST")
            
        # Check versions directory
        versions_path = os.path.join(migrations_path, 'versions')
        if os.path.exists(versions_path):
            print("\nVersions directory exists")
            print("Contents of versions directory:")
            for item in os.listdir(versions_path):
                print(f"- {item}")
        else:
            print("\nVersions directory DOES NOT EXIST")
    else:
        print("Migrations directory DOES NOT EXIST")
    
    # Print Python path
    print("\nPython path:")
    for path in sys.path:
        print(f"- {path}")

if __name__ == "__main__":
    check_migrations_structure()
    
    # Try to import the env module to see if it works
    print("\nAttempting to import migrations.env:")
    try:
        import migrations.env
        print("Successfully imported migrations.env")
    except ImportError as e:
        print(f"Failed to import migrations.env: {e}")
    except AttributeError as e:
        print(f"Attribute error in migrations.env: {e}")
        print("This may be due to version incompatibility with alembic. We'll fix this in the next step.")

    # Also try the direct import
    print("\nAttempting to import env from migrations directory:")
    sys.path.insert(0, os.path.join(os.getcwd(), 'migrations'))
    try:
        import env
        print("Successfully imported env")
    except ImportError as e:
        print(f"Failed to import env: {e}")
    except AttributeError as e:
        print(f"Attribute error in env: {e}")
        print("This may be due to version incompatibility with alembic. We'll fix this in the next step.")
