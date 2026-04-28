<!doctype html>
<html lang="en" data-density="comfortable" data-font="jb" data-annot="off">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GXW Gallery — 3 variants, 3 components</title>
<link rel="stylesheet" href="./colors_and_type.css">
<link rel="stylesheet" href="./styles.css">
<link rel="stylesheet" href="./gallery.css">
</head>
<body>
<div class="gallery-wrap">

  <header class="masthead">
    <div class="crumbs">
      <span>Leviathan</span><span class="sep"> / </span>
      <span>Design system</span><span class="sep"> / </span>
      <span class="live">GXW Gallery</span>
    </div>
    <h1>Graph <em>&times;</em> World Engine<span class="slash"> — </span><em>3 variants &middot; 3 components</em></h1>
    <p class="lede">
      A parity gallery of three visual <span class="hl">variants</span> of the GXW canvas
      and three extractable <span class="hl">components</span>, each published as a
      standalone <code>here-now</code> URL. QA matrix below.
    </p>
  </header>

  <section class="gallery-section">
    <div class="hd">
      <span class="num">01</span>
      <h2>Variants</h2>
      <span class="lede">3 &times; GXW canvas, same content, different aesthetics</span>
    </div>
    <div class="gallery-grid">
      {{VARIANT_CARDS}}
    </div>
  </section>

  <section class="gallery-section">
    <div class="hd">
      <span class="num">02</span>
      <h2>Components</h2>
      <span class="lede">3 extractable widgets, standalone harnesses</span>
    </div>
    <div class="gallery-grid">
      {{COMPONENT_CARDS}}
    </div>
  </section>

  <section class="gallery-section">
    <div class="hd">
      <span class="num">03</span>
      <h2>QA matrix</h2>
      <span class="lede">Parity &amp; probe results per deliverable</span>
    </div>
    {{PARITY_TABLE}}
  </section>

  <footer class="gallery-footer">
    <span>Generated {{GENERATED_AT}}</span>
    <span>sources: ~/.agents/levnow/gxw-*</span>
  </footer>

</div>
</body>
</html>
