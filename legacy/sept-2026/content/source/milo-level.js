/* ---------------------------------------------------------------------------
   milo-level.js — the port source for M-04.

   Extracted VERBATIM from the runtime block of Milo Beta.html (the section
   commented "runtime: the part that would live on a server"). Nothing here is
   rewritten, reformatted or corrected. Where it looks wrong, it is still the
   definition of correct until the M-04 return says otherwise.

   Note on the blocker raised against the M-04 order: milo-live.js is NOT the
   port source for the ladder. It carries the system prompt and the context
   assembly, and it is the source for M-05. Level resolution never lived there.

   Depends on, and does not define:
     CORPUS[B].failure  — .says, .silence, and .ladder (chapter 11 only)
   State this block owns in the beta, which M-06 moves to the session:
     B, failureSeenAt, directAsks
--------------------------------------------------------------------------- */

let B = "01", stageIdx = 0, failureSeenAt = null, directAsks = 0;

const OVERRIDE = /just tell me|give up|please just say|tell me the answer|say it|i'm crying|im crying/i;

function build(){return CORPUS[B]}

/* NEG — a child reports something wrong in words the author never listed. The clock
   still starts, otherwise the ladder never escalates and Milo is stuck at observe. */
const NEG = /(doesn'?t|does not|won'?t|isn'?t|not) (work|working|change|changing|move|moving|stop|stopping|settle|start|starting|come on|turn on)|blank|dead|broken|stuck|frozen|weird|wrong|nothing (happens|is happening)|no number|no noise|where do i start|keeps? (going|clicking|beeping)|now it doesn'?t|used to work/i;

function matched(txt){
  const f=build().failure,t=txt.toLowerCase();
  return f.says.some(s=>t.includes(s.toLowerCase()))||NEG.test(t);
}

function elapsed(){return failureSeenAt?Math.round((Date.now()-failureSeenAt)/1000):null}

function level(txt){
  const f=build().failure,e=elapsed(),ov=OVERRIDE.test(txt);
  if(ov){directAsks++;
    if(B==="11")return directAsks===1?"L4":"L3";
    return "L3";}
  if(!matched(txt)&&failureSeenAt===null)return "L0";
  if(e===null)return "L0";
  if(B==="11"){const [a,b,c]=f.ladder;if(e<a)return "L0";if(e<b)return "L1";if(e<c)return "L2";return "L2";}
  if(e<f.silence)return "L0";
  return "L1";
}

/* --------------------------------------------------------------------------
   Four properties of the above that the M-03 fake did not have. Port them as
   they are; each one is a line in the M-04 return, not an edit.

   1. L4 exists. Chapter 11, first override only. The M-03 by-level line reads
      L0..L3 because the fake had four rungs; the real resolution has five and
      one of them fires exactly once per session, in one chapter.
   2. The clock alone never reaches L3. L3 and L4 are override-only. Chapter 11's
      third rung returns L2, and so does everything past it.
   3. elapsed() uses a falsy test on failureSeenAt, so a clock that legitimately
      reads 0 is treated as not started. Verbatim, and related to the cold-boot
      negative-clock trap in N6.
   4. The override is tested before matched(), so an override phrase resolves
      L3 even when the clock has never started.

   On property 1 and the nine rules: L4 is a permission, not a new tier of
   disclosure. Decision G of the M-04 order — ctx.fix is legal at L3 and at L4
   and illegal everywhere else, so R3's condition becomes "not L3 and not L4"
   in the same commit as this port. R4's "none supplied" logic applies at L4
   unchanged. No tenth rule; the once-per-session property is already carried
   by directAsks above.
-------------------------------------------------------------------------- */
