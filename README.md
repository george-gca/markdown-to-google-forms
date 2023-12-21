# Markdown to Google Forms

Python script to convert a Markdown style document into Google Apps Script code, which in turn is used to generate a Google Forms.

This is not the best solution possible, but it is a solution. One can probably implement something more robust by using libraries like [marko](https://github.com/frostming/marko) or [mistletoe](https://github.com/miyuchina/mistletoe).

## Usage

Simply call the script giving a markdown file as input. By default it prints the code to stdout, but you can pipe the output to a file:

```python
python3 main.py sample.md > script.js
```

Then, paste the generated code on a [new project](https://script.google.com/home/projects/create) in Google Apps Script and execute it. A new file will be created on your [Google Drive](https://drive.google.com/) with the name you used as title. Note that the form is not ready to use, but at least the basic structure will be done.
