import concurrent.futures
import hashlib
import json
import re
import shutil
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

BASE = 'https://prompt-motion.com'
OUT = Path('/Users/jean-patricksmith/.agents/skills/motion-graphics/provenance/prompt-motion')
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'pages').mkdir(exist_ok=True)

def digest(data):
    return hashlib.sha256(data).hexdigest()

class EntryParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.prompt_depth = None
        self.prompt = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in {'br','hr','img','input','link','meta','source','wbr'}:
            self.depth += 1
        if a.get('id') == 'entry-prompt':
            self.prompt_depth = self.depth
        if tag == 'br' and self.prompt_depth is not None:
            self.prompt.append('\n')
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
    def handle_endtag(self, tag):
        if tag in {'br','hr','img','input','link','meta','source','wbr'}:
            return
        if self.prompt_depth == self.depth:
            self.prompt_depth = None
        self.depth -= 1
    def handle_data(self, data):
        if self.prompt_depth is not None:
            self.prompt.append(data)

def collect(entry):
    entry = dict(entry)
    slug = entry['slug']
    path = OUT / 'pages' / (slug + '.html')
    url = BASE + '/' + slug
    try:
        if path.exists():
            raw = path.read_bytes()
        else:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                raw = response.read()
            path.write_bytes(raw)
        parser = EntryParser()
        parser.feed(raw.decode('utf-8'))
        prompt = ''.join(parser.prompt)
        entry.update(page_url=url, source_links=list(dict.fromkeys(
            link for link in parser.links if link.startswith(('https://x.com/','https://github.com/'))
            and link != 'https://x.com/p4nthera_')),
            prompt=prompt or None, raw_path='pages/' + slug + '.html', sha256=digest(raw),
            prompt_sha256=digest(prompt.encode()) if prompt else None,
            retrieval_state='retrieved', media_state='linked_not_downloaded_or_watched')
        if 'prompt' in entry['tags'] and not prompt:
            entry['retrieval_state'] = 'missing_prompt'
        entry.pop('blur', None)
    except Exception as error:
        entry.update(page_url=url, retrieval_state='failed', error=str(error))
    return entry

if __name__ == '__main__':
    # Assert nested markup, entities and line breaks survive extraction.
    check = EntryParser()
    check.feed('<div id="entry-prompt">a &amp; b<span> c</span><br/>d</div><p>outside</p>')
    assert ''.join(check.prompt) == 'a & b c\nd'
    catalog = Path('/tmp/prompt-motion-catalog.html').read_bytes()
    shutil.copyfile('/tmp/prompt-motion-catalog.html', OUT / 'catalog.html')
    entries = json.loads(Path('/tmp/prompt-motion-list.json').read_text())
    links = set(re.findall(r'href="(/[^/"?]+-[0-9a-f]{6})"', catalog.decode()))
    assert links == {'/' + item['slug'] for item in entries}, 'catalog inventory mismatch'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        result = list(pool.map(collect, entries))
    (OUT / 'entries.jsonl').write_text(''.join(json.dumps(item,ensure_ascii=False)+'\n' for item in result))
    failures = [item['slug'] for item in result if item['retrieval_state'] != 'retrieved']
    manifest = dict(retrieved_at=datetime.now(timezone.utc).isoformat(), site_url=BASE,
        catalog_sha256=digest(catalog), catalog_entry_count=len(entries),
        prompt_tag_count=sum('prompt' in item['tags'] for item in entries),
        skill_tag_count=sum('skill' in item['tags'] for item in entries),
        extracted_prompt_count=sum(bool(item.get('prompt')) for item in result),
        failures=failures, entries='entries.jsonl',
        scope='All entry links and metadata in the unfiltered live homepage snapshot; external repositories and videos are links only.',
        rights='Videos and prompts belong to their creators. Local reference archive; no license for reuse inferred.',
        complete=not failures)
    (OUT / 'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    shutil.copyfile(__file__, OUT / 'collector.py')
    print(json.dumps(manifest,indent=2),flush=True)
    if failures:
        raise SystemExit(1)
