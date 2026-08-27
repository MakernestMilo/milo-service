/* Milo build card — the three artefacts a child builds from, and the same three
   the model reasons with. The netlist and the sketch are data, not decoration:
   they go into Milo's context so it can point at a line the child is looking at.
   Build 01 keeps its hand-drawn circuit; every later build is drawn from its own
   block list by diagram(), so the picture and the netlist can never disagree. */
const B_A={n:"SENSOR A",s:"reads warmth",pin:"A0",w:"YELLOW",pwr:1,c:"the signal, the reading itself"};
const B_B={n:"SENSOR B",s:"a metre away",pin:"A1",w:"YELLOW",pwr:1,c:"the second reading, from somewhere else"};
const B_DIAL={n:"DIAL",s:"you turn it",pin:"DIAL",c:"every number you set"};
const B_SW={n:"SWITCH",s:"magnet near, or not",pin:"SW",c:"one event, or nothing"};
const B_DSP={n:"DISPLAY",s:"shows it",pin:"DSP",c:"the numbers, on their way to be shown"};
const B_RING={n:"RING",s:"the verdict, in colour",pin:"RING",c:"the decision, seen across a room"};
const B_BUZ={n:"BUZZER",s:"heard next door",pin:"BUZ",c:"the decision, heard through a wall"};
const B_LMP={n:"LAMP",s:"on the 1 m lead",pin:"LMP",c:"an output in a room you are not in"};

function diagram(c){
  const I=c.blocks.in,O=c.blocks.out,rows=Math.max(I.length,O.length);
  const H=64+rows*42,y0=n=>84+n*42;
  const wire=(x1,x2,y,col)=>`<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${col}" stroke-width="2.4"/>`;
  const col=w=>w==="YELLOW"?"#B08A15":w==="RED"?"#B03A22":"#191713";
  const box=(b,i,left)=>{const y=y0(i)-17,x=left?8:264;
    return `<rect x="${x}" y="${y}" width="88" height="34" rx="4" fill="none" stroke="#191713" stroke-width="1.6"/>`
    +`<text x="${x+8}" y="${y+15}" class="dl">${b.n}</text><text x="${x+8}" y="${y+27}" class="ds">${b.s}</text>`;};
  let s=`<svg viewBox="0 0 360 ${H}" role="img" aria-label="circuit diagram">`
   +`<rect x="126" y="24" width="108" height="${H-48}" rx="4" fill="none" stroke="#191713" stroke-width="1.6"/>`
   +`<text x="180" y="44" class="dl" text-anchor="middle">BOARD</text>`
   +`<text x="180" y="58" class="ds" text-anchor="middle">microcontroller</text>`;
  I.forEach((b,i)=>{const y=y0(i);s+=box(b,i,1)+wire(96,126,y,col(b.w))
    +`<text x="111" y="${y-6}" class="dw" text-anchor="middle" fill="${col(b.w)}">${b.w||"—"}</text>`
    +`<circle cx="126" cy="${y}" r="3" fill="#191713"/><text x="132" y="${y+4}" class="dp">${b.pin}</text>`;});
  O.forEach((b,i)=>{const y=y0(i);s+=box(b,i,0)+wire(234,264,y,"#191713")
    +`<circle cx="234" cy="${y}" r="3" fill="#191713"/><text x="228" y="${y+4}" class="dp" text-anchor="end">${b.pin}</text>`;});
  s+=`<path d="M180 ${H-24} V${H-6}" fill="none" stroke="#191713" stroke-width="1.6"/>`
   +`<text x="180" y="${H-30}" class="dw" text-anchor="middle">1 M LEAD · USB POWER</text></svg>`;
  return s;
}
function netlistOf(c){
  if(c.netlist)return c.netlist;
  const rows=[];
  c.blocks.in.concat(c.blocks.out).forEach(b=>{
    if(b.pwr){rows.push({w:"red",from:b.n.toLowerCase()+" · V",to:"board · 3V",c:"power out to the sensor"});
      rows.push({w:"black",from:b.n.toLowerCase()+" · G",to:"board · GND",c:"ground back from the sensor"})}
    rows.push({w:(b.w||"\u2014").toLowerCase(),from:b.n.toLowerCase(),to:"board · "+b.pin,c:b.c});
  });
  rows.push({w:"1 m lead",from:"USB socket",to:"board",c:"power in"});
  return c.netlist=rows;
}

const CARD={
"01":{
 netlist:[
  {w:"red",   from:"sensor A · V", to:"board · 3V",  c:"power out to the sensor"},
  {w:"black", from:"sensor A · G", to:"board · GND", c:"ground back from the sensor"},
  {w:"yellow",from:"sensor A · S", to:"board · A0",  c:"the signal, the reading itself"},
  {w:"\u2014",from:"display",      to:"board · DSP", c:"the number, on its way to be shown"},
  {w:"1 m lead",from:"USB socket", to:"board",       c:"power in"}],
 pins:["3V","GND","A0","DSP"],
 svg:`<svg viewBox="0 0 360 252" role="img" aria-label="First Light circuit diagram">
 <rect x="18" y="58" width="88" height="68" rx="4" fill="none" stroke="#191713" stroke-width="1.6"/>
 <text x="28" y="86" class="dl">SENSOR A</text><text x="28" y="102" class="ds">reads warmth</text>
 <text x="112" y="70" class="dp">V</text><text x="112" y="92" class="dp">G</text><text x="112" y="114" class="dp">S</text>
 <rect x="200" y="38" width="142" height="152" rx="4" fill="none" stroke="#191713" stroke-width="1.6"/>
 <text x="332" y="60" class="dl" text-anchor="end">BOARD</text><text x="332" y="74" class="ds" text-anchor="end">microcontroller</text>
 <line x1="106" y1="76" x2="200" y2="76" stroke="#B03A22" stroke-width="2.4"/>
 <line x1="106" y1="98" x2="200" y2="98" stroke="#191713" stroke-width="2.4"/>
 <line x1="106" y1="120" x2="200" y2="120" stroke="#B08A15" stroke-width="2.4"/>
 <text x="152" y="70" class="dw" fill="#B03A22">RED</text>
 <text x="152" y="92" class="dw">BLACK</text>
 <text x="152" y="114" class="dw" fill="#8A6C0F">YELLOW</text>
 <text x="209" y="80" class="dp">3V</text><text x="209" y="102" class="dp">GND</text><text x="209" y="124" class="dp">A0</text>
 <circle cx="200" cy="76" r="3" fill="#191713"/><circle cx="200" cy="98" r="3" fill="#191713"/><circle cx="200" cy="120" r="3" fill="#191713"/>
 <rect x="18" y="176" width="88" height="46" rx="4" fill="none" stroke="#191713" stroke-width="1.6"/>
 <text x="28" y="198" class="dl">DISPLAY</text><text x="28" y="212" class="ds">shows it</text>
 <path d="M106 199 H160 V166 H200" fill="none" stroke="#191713" stroke-width="1.6" stroke-dasharray="4 3"/>
 <circle cx="200" cy="166" r="3" fill="#191713"/><text x="209" y="170" class="dp">DSP</text>
 <path d="M271 190 V228" fill="none" stroke="#191713" stroke-width="1.6"/>
 <path d="M266 222 L271 230 L276 222" fill="none" stroke="#191713" stroke-width="1.6"/>
 <text x="271" y="246" class="dw" text-anchor="middle">1 M LEAD \u00b7 USB POWER</text>
 </svg>`,
 sketch:[
  "const int SENSOR = A0;",
  "Display display;",
  "",
  "void setup() {",
  "  display.begin();",
  "}",
  "",
  "void loop() {",
  "  int raw = analogRead(SENSOR);",
  "  float degrees = toCelsius(raw);",
  "  display.show(degrees, 1);",
  "  delay(2000);",
  "}"],
 sketchnote:"Line 9 is the only line that touches the world. Line 12 is why a reading takes two seconds to change.",
 photo:{id:"built-01",cap:"The finished First Light: board clicked onto the base, sensor A wired to 3V, GND and A0, display lit."}},

"02":{pins:["3V","GND","A0","DSP","DIAL","RING"],
 blocks:{in:[B_A,B_DIAL],out:[B_DSP,B_RING]},
 sketch:[
  "int threshold = 20;   // set on the dial",
  "",
  "void loop() {",
  "  float degrees = readSensor(A0);",
  "  display.show(degrees, 1);",
  "",
  "  if (degrees < threshold) ring.set(ALARM);",
  "  else                     ring.set(NORMAL);",
  "",
  "  delay(2000);",
  "}"],
 sketchnote:"Line 1 is your dial. Line 7 is the whole opinion — and nothing in this sketch knows whether your number is a sensible one.",
 photo:{id:"built-02",cap:"The ring lit in its alarm colour, seen from across a room, with the display showing a reading below the threshold."}},

"03":{pins:["3V","GND","A0","DSP","DIAL","RING","BUZ"],
 blocks:{in:[B_A,B_DIAL],out:[B_DSP,B_RING,B_BUZ]},
 sketch:[
  "int threshold = 20;",
  "",
  "void loop() {",
  "  float degrees = readSensor(A0);",
  "  display.show(degrees, 1);",
  "",
  "  if (degrees < threshold) {",
  "    ring.set(ALARM);  buzzer.on();",
  "  } else {",
  "    ring.set(NORMAL); buzzer.off();",
  "  }",
  "  delay(2000);",
  "}"],
 sketchnote:"Lines 8 and 10 are the same instruction to the board — one is just louder. ALWAYS deletes line 7 and leaves the buzzer on.",
 photo:{id:"built-03",cap:"The machine turned to face into the room, ring glowing normal, buzzer fitted to BUZ."}},

"04":{pins:["3V","GND","A0","DSP","DIAL","RING","BUZ"],
 blocks:{in:[B_A,B_DIAL],out:[B_DSP,B_RING,B_BUZ]},
 sketch:[
  "int startAt = 24;   // your start number",
  "int stopAt  = 22;   // your stop number",
  "bool alarm  = false;",
  "",
  "void loop() {",
  "  float degrees = readSensor(A0);",
  "",
  "  if (!alarm && degrees < startAt) alarm = true;",
  "  if ( alarm && degrees > stopAt ) alarm = false;",
  "",
  "  buzzer.set(alarm);",
  "  delay(2000);",
  "}"],
 sketchnote:"Lines 8 and 9 are two separate decisions. Make lines 1 and 2 the same number and a wobble crosses both of them.",
 photo:{id:"built-04",cap:"A hand held near sensor A but not touching it — the exact gesture that makes the reading hover on the line."}},

"05":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ"],
 blocks:{in:[B_A,B_B,B_DIAL],out:[B_DSP,B_RING,B_BUZ]},
 sketch:[
  "int shoutIfApartBy = 2;   // your gap",
  "int watching = A;         // which one the alarm listens to",
  "",
  "void loop() {",
  "  float a = readSensor(A0);",
  "  float b = readSensor(A1);",
  "  display.showBoth(a, b);",
  "",
  "  if (abs(a - b) > shoutIfApartBy) shout();",
  "  if (readSensor(watching) < startAt) alarm = true;",
  "",
  "  delay(2000);",
  "}"],
 sketchnote:"Line 9 compares the two. Line 10 is the one people forget: the alarm reads whichever sensor line 2 names, not the one you happen to be looking at.",
 photo:{id:"built-05",cap:"Sensor B on the end of its lead held at the bottom of a window, the machine behind it showing two numbers."}},

"06":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ]},
 sketch:[
  "long count = 0;",
  "int settle = 2000;        // your settle time, in ms",
  "long lastCount = 0;",
  "",
  "void loop() {",
  "  if (switchOpened() && millis() - lastCount > settle) {",
  "    count = count + 1;",
  "    lastCount = millis();",
  "  }",
  "  display.show(count);",
  "}"],
 sketchnote:"Line 6 is the whole chapter. Without the second half of it, one slow opening runs line 7 three times.",
 photo:{id:"built-06",cap:"The switch and magnet on a real cupboard, slightly imperfectly aligned, the display reading a count in the low hundreds."}},

"07":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ]},
 sketch:[
  "long writeEvery = 600000;   // your interval, in ms",
  "long lastWrite = 0;",
  "",
  "void loop() {",
  "  float degrees = readSensor(A0);",
  "",
  "  if (millis() - lastWrite > writeEvery) {",
  "    memory.append(now(), degrees);",
  "    lastWrite = millis();",
  "  }",
  "}"],
 sketchnote:"Line 1 is the only decision in this sketch, and it decides everything the chart can show you. Line 8 never runs while a short event is happening.",
 photo:{id:"built-07",cap:"The chart card half filled in by hand, pencil beside it, the machine plugged into a household charger behind."}},

"08":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW","LMP"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ,B_LMP]},
 sketch:[
  "Step sequence[3];   // yours, set on the dial",
  "",
  "void runSequence() {",
  "  for (int i = 0; i < 3; i++) {",
  "    delay(sequence[i].gapBefore);",
  "    output(sequence[i].what, ON);",
  "    delay(sequence[i].howLong);",
  "    output(sequence[i].what, OFF);",
  "  }",
  "  display.show(\"SEQUENCE DONE\");",
  "}"],
 sketchnote:"Nothing between lines 6 and 8 asks whether anything happened. Line 10 runs whether the lamp was plugged in or not.",
 photo:{id:"built-08",cap:"The lamp lit on a hall floor at the end of its lead, the machine out of frame in another room."}},

"D":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW","LMP"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ,B_LMP]},
 sketch:[
  "void loop() {",
  "  float inside  = readSensor(A0);   // chapter 05",
  "  float outside = readSensor(A1);",
  "",
  "  if (switchOpened() && settled()) count++;   // chapter 06",
  "  logEvery(writeEvery, inside, outside);      // chapter 07",
  "",
  "  if (count > tooMany && !alarm) { alarm = true; runSequence(); }",
  "  if (quietAgain()) alarm = false;            // chapter 04",
  "}"],
 sketchnote:"Every line here is something you wrote in an earlier chapter. Nothing in the Doorkeeper is new, which is why it can be the biggest thing in the box.",
 photo:{id:"built-D",cap:"The finished Doorkeeper mounted at a real front door, leads routed, slightly untidy, obviously living there."}},

"09":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW","LMP"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ,B_LMP]},
 sketch:[
  "void loop() {",
  "  float here = readSensor(A0);",
  "  float there = readSensor(A1);",
  "",
  "  log(here, there);",
  "  decide(here);",
  "}"],
 sketchnote:"Nothing in this sketch says where the machine is standing, and that is the whole chapter. The same six lines answer a different question in a different place.",
 photo:{id:"built-09",cap:"The machine strapped to a pipe in a cold corner of a real house — awkward, correct, and not where anybody would put it for convenience."}},

"10":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW","LMP"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ,B_LMP]},
 sketch:[
  "void loop() {",
  "  float degrees = readSensor(A0);   // whatever is around sensor A",
  "  display.show(degrees, 1);",
  "  decide(degrees);",
  "}"],
 sketchnote:"Line 2 does not know whether sensor A is in the room or shut inside a card box with a warm board. The sketch cannot tell. You can.",
 photo:{id:"built-10",cap:"The two flat die-cut templates, the tape and the four clips, laid out unassembled. There is no photograph of a finished creature anywhere."}},

"11":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW","LMP"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ,B_LMP]},
 sketch:[
  "void loop() {",
  "  // 1 power    — none of this runs without it",
  "  float degrees = readSensor(A0);   // 2 sensor",
  "  bool cold = decide(degrees);      // 3 rule",
  "  buzzer.set(cold);                 // 4 output",
  "  if (cold) runSequence();          // 5 sequence",
  "}"],
 sketchnote:"The five tests are the five lines, in the order they run. A test only tells you something if the line above it already passed.",
 photo:{id:"built-11",cap:"The five sealed fault tabs at the back of the book, four still sealed and one torn open."}},

"12":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW","LMP"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ,B_LMP]},
 sketch:[
  "// It should ____________ when ____________,",
  "// and I will know it worked if ____________.",
  "",
  "void loop() {",
  "  // only the capabilities your sentence actually needs",
  "}"],
 sketchnote:"The comment is written before the code, and the code is cut until it fits in one evening. What you delete is the part worth writing down.",
 photo:{id:"built-12",cap:"Eleven filled-in cards spread out on a table in a child's handwriting, with the chart card among them."}},

"G":{pins:["3V","GND","A0","A1","DSP","DIAL","RING","BUZ","SW","LMP"],
 blocks:{in:[B_A,B_B,B_SW,B_DIAL],out:[B_DSP,B_RING,B_BUZ,B_LMP]},
 sketch:[
  "// In their words:",
  "// ____________ annoys me, it happens when ____________,",
  "// and I would know it was fixed if ____________.",
  "",
  "void loop() {",
  "  // built to their sentence, not yours",
  "}"],
 sketchnote:"The specification at the top of this sketch was dictated by somebody else. The one revision you get comes from them too, not from you.",
 photo:{id:"built-G",cap:"An older person's hands using the machine, unaided, in their own kitchen. The child is not in the frame."}}
};

let cardOpen=null;
function cardTab(t){
  const c=CARD[B];if(!c)return;
  const w0=document.getElementById("cardbody");
  if(cardOpen===t){cardOpen=null;w0.hidden=true;document.querySelectorAll(".ct").forEach(b=>b.setAttribute("aria-selected","false"));return}
  cardOpen=t;w0.hidden=false;
  document.querySelectorAll(".ct").forEach(b=>b.setAttribute("aria-selected",b.dataset.t===t));
  const w=document.getElementById("cardbody");
  if(t==="d")w.innerHTML=`<div class="dia">${c.svg||(c.svg=diagram(c))}</div>`
    +`<table class="net"><tbody>${netlistOf(c).map(n=>`<tr><td class="nw">${n.w}</td><td>${n.from} <span>\u2192</span> ${n.to}</td></tr>`).join("")}</tbody></table>`;
  if(t==="s")w.innerHTML=`<pre class="sk">${c.sketch.map((l,i)=>`<span class="ln">${String(i+1).padStart(2," ")}</span>${l.replace(/[<>&]/g,m=>({"<":"&lt;",">":"&gt;","&":"&amp;"}[m]))}`).join("\n")}</pre>`
    +`<p class="skn">${c.sketchnote}</p>`;
  if(t==="p")w.innerHTML=`<div class="ph"><div class="phi"><b>Photograph goes here</b><span>${c.photo.cap}</span></div></div>`;
}
function renderCard(){
  const host=document.getElementById("card"),c=CARD[B];
  if(!c){host.innerHTML=`<p class="skn" style="padding:14px 20px;margin:0">No build card drawn for this build yet. First Light is the reference.</p>`;return}
  host.innerHTML=`<div class="cth"><button class="ct" data-t="d">Circuit</button><button class="ct" data-t="s">Sketch</button><button class="ct" data-t="p">Built</button></div><div id="cardbody" hidden></div>`;
  host.querySelectorAll(".ct").forEach(b=>b.onclick=()=>cardTab(b.dataset.t));
  /* the card is rebuilt on every build change; keep whichever tab was open open, so
     stepping through the chapters does not close the circuit on the reader. */
  const was=cardOpen;cardOpen=null;if(was)cardTab(was);
}
