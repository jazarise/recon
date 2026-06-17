import subprocess


def build_executable():
    print("Building ReconX standalone executable using PyInstaller...")
    subprocess.run(
        ["pyinstaller", "--onefile", "--name", "reconx", "src/reconx/main.py"],
        check=True,
    )
    print("Build complete. Artifact located in dist/reconx")


if __name__ == "__main__":
    build_executable()
