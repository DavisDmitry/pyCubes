import os

import lazydocs as ld


def main():
    ld.generate_docs(
        ["cubes"],
        output_path="docs/reference",
        src_base_url=(
            f"https://github.com/DavisDmitry/pyCubes/tree/{os.environ['VERSION']}/"
        ),
        remove_package_prefix=True,
        ignored_modules=["abc"],
        watermark=False,
        validate=True,
    )


if __name__ == "__main__":
    main()
