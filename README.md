# PicoSSG

PicoSSG is the world's smallest static site generator:
it turns a collection of Markdown files and Jinja templates into a set of HTML pages.
To run it:

1.  Create and activate a Python virtual environment.
2.  `pip install -r requirements.txt`.
3.  `python picossg.py` or `make build` to turn the source directory `./src` into `./docs`.

## Interview Questions

1.  Open `picossg.py` in your favorite code editor and think aloud as you go through it
    as if you were doing a code review.
    What don't you immediately understand?
    What would you change and why?

2.  You have been asked to modify PicoSSG so that users can specify files to ignore;
    for example,
    `python picossg --ignore datafiles '*.obj'`
    would *not* copy anything in `src/datafiles` or any `.obj` files in `src.
    What changes would you make where?

3.  How would you go about writing unit tests for PicoSSG?
    In particular, how would you handle the fact that it reads and writes files?
