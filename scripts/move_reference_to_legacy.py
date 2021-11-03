import os
import re


def main():
    with open("pyproject.toml", "r") as file:
        version = (
            re.findall(r"version = \"+\d\.+\d\.+\d\"", file.read())[0]
            .replace('"', "")
            .replace("version = ", "")
        ).split(".")[:2]
    files = os.listdir("docs/reference")
    os.rename("docs/reference", f"docs/legacy/{'_'.join(version)}")
    with open("mkdocs.yml", "a") as file:
        lines = []
        lines.append(f"    - '{'.'.join(version)}':\n")
        for file_name in files:
            lines.append(
                f"      - {file_name.replace('.md', '')}: "
                f"legacy/{'_'.join(version)}/{file_name}\n"
            )
        file.writelines(lines)


if __name__ == "__main__":
    main()
