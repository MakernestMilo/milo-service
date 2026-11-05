import corpus
for i, c in enumerate(corpus.CHAPTERS, 1):
    print(f"{i:2} {c['key']:>2} {c['name']:<18} {c['rung']:<12} "
          f"{len(c['stages'])} stages {len(c.get('parts') or [])} parts")
