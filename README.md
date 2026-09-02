# SciRecast

The public site of [SciRecast](https://a85tract.github.io/SciRecast/): the
engine, the first case, and how to contribute.

One page, no build step. `index.html` is the content, `assets/css/site.css`
the design system, `assets/js/site.js` the theme switch, reading progress
and scroll spy. `.nojekyll` tells GitHub Pages to serve the files as they
are. To preview, open `index.html` in a browser, or:

```bash
python3 -m http.server 8000
```

Every component the page names is its own repository, linked from the page;
this repository tracks none of them. Working clones that sit beside these
files for convenience are ignored by `.gitignore`.
