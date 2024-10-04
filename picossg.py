"""Convert a pile of Markdown files to HTML."""

import argparse
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from pathlib import Path

from util import SUFFIXES_TXT, find_files, read_file, write_file


def main():
    """Main driver."""
    opt = parse_args()

    env = Environment(loader=FileSystemLoader(opt.templates))

    files = find_files(opt.src)
    for filepath, content in files.items():
        if filepath.suffix == ".md":
            render_markdown(env, opt.dst, opt.src, filepath, content)
        else:
            copy_file(opt.dst, opt.src, filepath, content)


def copy_file(output_dir, source_dir, source_path, content):
    """Copy a file verbatim."""
    output_path = make_output_path(output_dir, source_dir, source_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_file(output_path, content)


def do_markdown_links(doc, source_path):
    """Fix .md links in HTML."""
    for node in doc.select("a[href]"):
        if node["href"].endswith(".md"):
            node["href"] = node["href"].replace(".md", ".html").lower()


def do_root_path_prefix(doc, source_path):
    """Fix @root links in HTML."""
    depth = len(source_path.parents) - 2
    prefix = "./" if (depth == 0) else "../" * depth
    targets = (
        ("a[href]", "href"),
        ("link[href]", "href"),
        ("script[src]", "src"),
    )
    for selector, attr in targets:
        for node in doc.select(selector):
            if "@root/" in node[attr]:
                node[attr] = node[attr].replace("@root/", prefix)


def do_title(doc, source_path):
    """Make sure title element is filled in."""
    doc.title.string = doc.h1.get_text()


def make_output_path(output_dir, source_dir, source_path):
    """Build output path."""
    temp = source_path.relative_to(source_dir)
    temp = Path(str(temp).replace(".md", ".html"))
    return Path(output_dir, temp)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst", type=str, default="docs", help="output directory")
    parser.add_argument("--src", type=str, default="src", help="input directory")
    parser.add_argument("--templates", type=str, default="templates", help="templates directory")
    return parser.parse_args()


def render_markdown(env, output_dir, source_dir, source_path, content):
    """Convert Markdown to HTML."""
    html = markdown(content)
    template = env.get_template("page.html")
    html = template.render(content=html)

    transformers = (
        do_markdown_links,
        do_title,
        do_root_path_prefix,
    )
    doc = BeautifulSoup(html, "html.parser")
    for func in transformers:
        func(doc, source_path)

    output_path = make_output_path(output_dir, source_dir, source_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(str(doc))


if __name__ == "__main__":
    main()
