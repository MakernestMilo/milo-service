// Milo — live model layer. The ladder stays deterministic in buildroom.js;
// this file only turns the current situation into grounded language.
// Falls back to the scripted banks if the call fails.
(function(){
const MODEL = "claude-haiku-4-5";

// The only components that exist. Milo may never name anything outside this list.
const PARTS = [
  ["Arduino Uno R3", 1, "the green board with a silver USB socket"],
  ["USB A-B cable", 1, "the thick cable with a square-ish plug on one end"],
  ["Build Base", 1, "the pegged platform the board sits on"],
  ["Breadboard, 400 point", 1, "the white block full of little holes with a channel down the middle"],
  ["LED, red, 5 mm", 2, "the small clear bulb with two legs, one longer"],
  ["Resistor, 220 ohm", 8, "the tiny tube with red, red and brown stripes"],
  ["Jumper wire, red", 6, "a red wire with a stiff pin at each end"],
  ["Jumper wire, black", 6, "a black wire with a stiff pin at each end"],
  ["Ember shell", 1, "the small folded card shell with one round hole"],
  ["Ember fold-out sheet", 1, "the printed sheet in the lid with the seven steps"],
  ["Ember build card", 1, "the card with the finished light on the front and a QR code"]
];

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

OFF TOPIC
One warm redirect, then hold. Never refuse twice in a row, never lecture them about what you can discuss.

ORIENTATION
If they are new, or ask what this is, what they bought, what is in the box, who you are, or how long it takes — answer it properly and warmly from the context. A child who does not know where they are is not off topic. Then point at the current step.`;

function context(c){
  const s = c.step;
  const L = [];
  L.push("CHILD: "+(c.name ? c.name : "name unknown — do not ask for it"));
  L.push("\nKIT: MakerNest Origins. Ten creations in the box. This is creation 01 of 10, called Ember: make a light blink. Seven steps, twenty to thirty minutes. No tools, no glue, no soldering — everything pushes in by hand.");
  L.push("\nPARTS ON THE DESK (the complete list — nothing else exists):");
  PARTS.forEach(p=>L.push("- "+p[0]+" x"+p[1]+" — "+p[2]));
  L.push("\nALL SEVEN STEPS OF EMBER:");
  c.steps.forEach((x,i)=>L.push((i+1)+". "+x.label+(i===c.i?"  <-- THEY ARE HERE":"")+(c.done.includes(i)?"  (done)":"")));
  L.push("\nCURRENT STEP "+(c.i+1)+" — "+s.label);
  L.push("Goal: "+s.goal);
  L.push("What to do: "+s.action);
  L.push("Done when: "+s.proof);
  L.push("\nWIRING FOR EMBER (only relevant from step 3 on):");
  c.pinmap.forEach(r=>L.push("- "+r[0]+" to "+r[1]+" : "+r[2]));
  if(c.i>=5) L.push("\nTHE SKETCH THEY ARE WORKING WITH:\n"+c.sketch);
  if(c.failures && c.failures.length){
    L.push("\nKNOWN FAILURE MODES FOR THIS STEP (this is what actually goes wrong, in order of how often):");
    c.failures.forEach(f=>L.push("- symptom: "+(f.says||[]).join(" / ")+"\n  narrow: "+(f.ask||"")+"\n  point: "+(f.point||"")+"\n  fix: "+(f.fix||"")));
  }
  L.push("\nESCALATION: L"+c.esc);
  if(c.rung) L.push("RUNG MATERIAL (say this, in your voice, and no further): "+c.rung);
  if(c.override) L.push("OVERRIDE: they asked outright to be told. Go straight to L3 and give the fix plainly.");
  return L.join("\n");
}

window.MiloLive = {
  model: MODEL,
  enabled: true,
  async answer(text, c){
    const msgs = (c.history||[]).slice(-8).map(h=>({role: h.who==="kid"?"user":"assistant", content: h.t}));
    msgs.push({role:"user", content: text});
    const out = await window.claude.complete({
      model: this.model,
      max_tokens: 400,
      system: VOICE + "\n\n=== CONTEXT ===\n" + context(c),
      messages: msgs
    });
    const s = (out||"").trim();
    if(!s) throw new Error("empty");
    return s;
  }
};
})();
