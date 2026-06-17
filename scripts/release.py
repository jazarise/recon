import os
import subprocess
import hashlib


def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def generate_sbom():
    print("Generating SBOM...")
    run_command(["pip-audit", "--format", "cyclonedx-json", "-o", "reconx-sbom.json"])


def generate_checksums(files):
    print("Generating checksums...")
    checksums = {}
    for file in files:
        if os.path.exists(file):
            with open(file, "rb") as f:
                checksums[file] = hashlib.sha256(f.read()).hexdigest()

    with open("checksums.txt", "w") as f:
        for file, sha in checksums.items():
            f.write(f"{sha}  {file}\n")


def main():
    version = "3.0.0"
    print(f"Preparing release for ReconX {version}")

    # Generate SBOM
    generate_sbom()

    # Build package
    run_command(["python", "-m", "build", "--sdist", "--wheel"])

    # Package into a release tar
    release_tar = f"reconx-{version}.tar.gz"
    run_command(["tar", "-czvf", release_tar, "dist/", "reconx-sbom.json"])

    # Checksums
    generate_checksums([release_tar, "reconx-sbom.json"])

    print("Release packaged successfully.")


if __name__ == "__main__":
    main()
