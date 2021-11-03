import os
import re


def main():
    with open("pyproject.toml", "r") as file:
        text = file.read()
    version_str = re.findall(r"version = \"+\d\.+\d\.+\d\"", text)[0]
    text = text.replace(version_str, f'version = "{os.environ["VERSION"]}"')
    with open("pyproject.toml", "w") as file:
        file.write(text)


if __name__ == "__main__":
    main()
