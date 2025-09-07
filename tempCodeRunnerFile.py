
import os
import sys
import subprocess

def setup_project():
    """Setup the weather project environment with pandas"""
    print("Setting up Weather Application Project with Pandas...")
    print("=" * 50)
    
    # Check if virtual environment exists
    env_name = "weather_pandas_env"
    if not os.path.exists(env_name):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", env_name])
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")
    
    # Activate and install dependencies
    if os.name == 'nt':  # Windows
        activate_script = f"{env_name}\\Scripts\\activate"
        pip_path = f"{env_name}\\Scripts\\pip"
    else:  # Unix/Linux/MacOS
        activate_script = f"{env_name}/bin/activate"
        pip_path = f"{env_name}/bin/pip"
    
    print("Installing dependencies...")
    try:
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        subprocess.run([pip_path, "install", "pandas", "requests", "python-dotenv"], check=True)
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("Setup complete! To get started:")
    print(f"1. Activate environment: source {activate_script}")
    print("2. Run weather analysis: python weather_analysis.py")
    print("3. Or run main app: python main.py")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    setup_project()
