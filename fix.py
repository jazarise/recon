import os

d = r"e:\ReconX\ReconXv3.0"
for root, dirs, files in os.walk(d):
    for file in files:
        if file.endswith(".py"):
            p = os.path.join(root, file)
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = content.replace(
                "from reconx.global_intel", "from reconx.global_intel"
            ).replace("from reconx", "from reconx")
            if content != new_content:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(new_content)
