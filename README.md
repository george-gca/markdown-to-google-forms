# Markdown to Google Forms

<a target="_blank" href="https://colab.research.google.com/github/george-gca/markdown-to-google-forms/blob/main/Markdown_to_Google_Forms.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Python script to convert a Markdown style document into Google Apps Script code, which in turn is used to generate a Google Forms.

This is not the best solution possible, but it is a solution. One can probably implement something more robust by using libraries like [marko](https://github.com/frostming/marko) or [mistletoe](https://github.com/miyuchina/mistletoe).

## Usage

Simply call the script giving a markdown file as input. By default it prints the code to stdout, but you can pipe the output to a file:

```python
python3 main.py sample.md > script.js
```

There's also a [jupyter notebook](https://github.com/george-gca/markdown-to-google-forms/blob/main/Markdown_to_Google_Forms.ipynb) and [Google Colab](https://gist.github.com/george-gca/fbc4664dce3e97796d1fa212f769c6bb) version in this repo. In this case, modify the contents of the `markdown_file` variable in the notebook and run all cells.

Then, paste the generated code on a [new project](https://script.google.com/home/projects/create) in Google Apps Script and execute it. On the first run of this new project it will ask for permissions to your Google Drive, which should be conceded so it can create the new form. A new file will be created on your [Google Drive](https://drive.google.com/) with the name you used as title. Note that the form is not ready to use, but at least the basic structure will be done.
