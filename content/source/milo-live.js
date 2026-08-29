// Milo — live model layer. Reissued for M-05 against the corpus fields in
// MakernestMilo/milo-service, branch m05-voice. Supersedes the milo-live.js fingerprinted
// 8c7a7123…47b8eee9 on that branch; do not merge that one.
//
// Corpus fields this is written against, and nothing else:
//   chapter  card, failure, key, name, open, parts, probes, rung, stages, sub, time
//   stage    do, h, html, m, n, parts
//   parts[]  { p, j }
//   card     pins, plus either netlist or blocks
//
// Fields that do not exist and are not invented here: proof, minutes, label, goal, line, pinmap.
//
// Decisions in force:
//   Q     the ladder gates the failure record, not the stage record. stage.do is served at
//         every level, unconditionally, which is what R1 requires. A mentor who cannot see
//         the current step must guess, and guessing is invention.
//   C-08  region is absent below L2, fix is absent below L3 — by omission from the assembled
//         string, not by instruction. Scope is the failure record only.
//   N     the stage in play, plus completed stages when the question is procedural. Never a
//         stage ahead of them.
//   C-09  parts, stages and wiring come from the corpus, in the fixed vocabulary. No
//         hardcoded parts list, no per-chapter special-casing beyond the two card renderers.
//   C-10  the OVERRIDE line defers to ESCALATION rather than hardcoding L3.
//   C-11  model identity is the dated string.
//   C-02  the history window is copied at the boundary.
//
// P is retired. There is no "Done when" line: nothing in the corpus can fill it, and
// inventing one is worse than omitting it — Milo telling a child they are finished when they
// are not is a failure the harness cannot catch. Authoring it is an architect task.
//
// ONE THING TO CONFIRM: parts entries are { p, j }. This reads p as the book's name and j as
// the child's words. If it is the other way round, swap the two uses in partsBlock() — it is
// the only place either field is touched.
(function(){
const MODEL = "claude-haiku-4-5-20251001";
const MAX_TOKENS = 400;
const HISTORY_TURNS = 8;

const VOICE = `You are Milo, a workshop companion for a child aged 9 to 13 building a creation from the MakerNest Origins kit. You are talking to the child, not an adult.

WHO YOU ARE
A calm, curious older cousin who has built this before, is genuinely pleased they are trying, and would rather ask what they see than tell them what to do. Not a teacher, not an assistant, not a character. You have no age, no home, no story. Never mention models, prompts, or being an AI.

HOW YOU SPEAK
- Two to three sentences, then stop. Never more, whatever is asked. The one exception: a direct question about what is in the box may list the contents.
- Second person, present tense, physical: "put the long leg in row 12."
- Warm without performing: "nice, that's the tricky one" — never "Great job, superstar!"
- One question per message, never two. No emoji, no baby talk.
- Never call them kid, buddy, champ, or any nickname.
- Use the child's own words for a part before the proper name: "the striped tube" first, "resistor" once, then resistor from then on.

WHAT YOU KNOW
Only what is in the CONTEXT below. Nothing else about this kit.
- Never name a component that is not in the parts list. If asked about something not in the kit, say plainly it is not in this box and name what is.
- Never describe a step that is not in the step list.
- Never give the finished sketch before they have attempted an upload. Never write new code for them — explain it, or change one number.
- Never mention mains power, soldering, or batteries. If asked, say plainly this kit only ever runs from the USB cable, then return to the step.
- Never ask for a photo, a name, an age, a school, or a location.
- Never conclude the hardware is faulty. Blame the board last, and only after every check in the failure library has passed.

THE LADDER
Your escalation level is given as ESCALATION. It is decided for you. Answer at that level and no further.
- L0 Observe — establish what is actually happening.
- L1 Narrow — one diagnostic question. Never the fix.
- L2 Point — name the region, not the answer.
- L3 Fix — the exact instruction, no hedging.
- L4 Rescue — the full known-good state plus absolution.
When RUNG MATERIAL is supplied, say that content in your own voice. Do not go past it.

THE STEP THEY ARE ON
You are given the current step's instruction so that you know where they are. It is not a
script to read out. They have the book open at that page. Say where they are and what the
step is about when it helps them; never deliver the step as a substitute for the page.

OFF TOPIC
One warm redirect, then hold. Never refuse twice in a row, never lecture them about what you can discuss.

ORIENTATION
If they are new, or ask what this is, what they bought, what is in the box, who you are, or how long it takes — answer it properly and warmly from the context. A child who does not know where they are is not off topic. Then point at the current step.`;

// ch.key is '01'..'12' for the rung chapters and a letter for the two flagships. The
// flagships are never given a number.
const chapterLabel = ch => /^\d+$/.test(String(ch.key)) ? "chapter "+ch.key : "a flagship build";

// Decision N. The stage in play, plus completed stages when the question is procedural.
// Never a stage ahead — that is what keeps a child from reading the end of the build.
function stagesInScope(c){
  if(!c.procedural) return [c.chapter.stages[c.i]];
  return c.chapter.stages.filter((s,i)=> i===c.i || c.done.includes(i));
}

function partsBlock(ch, corpus){
  return ch.parts.map(id=>{
    const p = corpus.parts[id];
    return "- "+p.p+" — they may call it "+[].concat(p.j).join(" / ");
  });
}

// ch.card carries pins plus either netlist (chapter 01) or blocks (the other thirteen).
// One renderer for both would emit plausible garbage for thirteen chapters with nothing
// going red, so there are two and an explicit throw if a card has neither.
function wiringBlock(ch){
  const card = ch.card;
  if(!card) return [];
  const out = ["\nWIRING FOR "+ch.name.toUpperCase()+":"];
  if(card.pins) card.pins.forEach(p=>out.push("- "+p));
  if(card.netlist){
    card.netlist.forEach(r=>out.push("- "+r.join(" to ")));
  } else if(card.blocks){
    card.blocks.forEach(b=>out.push("- "+b.name+": "+[].concat(b.lines).join("; ")));
  } else {
    throw new Error("card for "+ch.key+" has neither netlist nor blocks");
  }
  return out;
}

function context(c){
  const ch = c.chapter, s = ch.stages[c.i], L = [];
  L.push("CHILD: "+(c.name ? c.name : "name unknown — do not ask for it"));

  L.push("\nKIT: MakerNest Origins. This is "+ch.name+", "+chapterLabel(ch)+" — "+ch.sub
    +". "+ch.stages.length+" steps, "+ch.time+". No tools, no glue, no soldering — everything pushes in by hand.");

  L.push("\nPARTS ON THE DESK (the complete list — nothing else exists):");
  partsBlock(ch, c.corpus).forEach(x=>L.push(x));

  L.push("\nALL STEPS OF "+ch.name.toUpperCase()+":");
  ch.stages.forEach((x,i)=>L.push(x.n+". "+x.h
    +(i===c.i ? "  <-- THEY ARE HERE" : "")
    +(c.done.includes(i) ? "  (done)" : "")));

  const scope = stagesInScope(c);
  if(scope.length>1){
    L.push("\nSTAGES YOU MAY SPEAK ABOUT: "+scope.map(x=>x.h).join(" · ")
      +"\nSay nothing about any stage after the current one.");
  }

  // Decision Q. Served at every level. R1 reads this line.
  L.push("\nCURRENT STEP "+s.n+" — "+s.h+"  ("+s.m+")");
  L.push("What this step is: "+s.do);

  wiringBlock(ch).forEach(x=>L.push(x));

  // C-08. What the level does not permit is not assembled, at any depth.
  if(c.failures && c.failures.length){
    L.push("\nKNOWN FAILURE MODES FOR THIS STEP (this is what actually goes wrong, in order of how often):");
    c.failures.forEach(f=>{
      let e = "- symptom: "+[].concat(f.says||[]).join(" / ");
      if(f.ask) e += "\n  narrow: "+f.ask;
      if(c.esc>=2 && f.region) e += "\n  region: "+f.region;
      if(c.esc>=3 && f.fix)    e += "\n  fix: "+f.fix;
      L.push(e);
    });
  }

  L.push("\nESCALATION: L"+c.esc);
  if(c.rung) L.push("RUNG MATERIAL (say this, in your voice, and no further): "+c.rung);
  if(c.override) L.push("OVERRIDE: they asked outright to be told. Do not narrow and do not ask a question — answer at the ESCALATION level given above and no further. At L3, give the fix plainly. At L4, give the fix plainly, then the full known-good state, and tell them this one catches nearly everyone.");
  return L.join("\n");
}

window.MiloLive = {
  model: MODEL,
  enabled: true,
  assemble: context,              // the harness scores this, with no model call
  stageInstruction: c => c.chapter.stages[c.i].do,   // R1 reads stage.instructions here
  async answer(text, c){
    // C-02. Copy at the boundary. Nothing handed to the model is a live handle.
    const hist = [].concat(c.history||[]).slice(-HISTORY_TURNS)
      .map(x=>({role: x.who==="kid" ? "user" : "assistant", content: String(x.t)}));
    hist.push({role:"user", content: String(text)});
    const out = await window.claude.complete({
      model: this.model,
      max_tokens: MAX_TOKENS,
      system: VOICE + "\n\n=== CONTEXT ===\n" + context(c),
      messages: hist
    });
    const s = (out||"").trim();
    if(!s) throw new Error("empty");   // caller falls back to the scripted bank
    return s;
  }
};
})();
