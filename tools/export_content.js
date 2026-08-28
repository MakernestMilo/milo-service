const fs = require("fs"), vm = require("vm"), path = require("path");
const src = f => fs.readFileSync(path.join("content/source", f), "utf8");
const ctx = vm.createContext({});
const ctxSrc = src("milo-corpus.js") + "\n" + src("milo-buildcard.js") + "\n" + src("milo-qc.js");
// Both files declare their objects with const, and a top-level const does
// NOT become a property of the context. One appended assignment to an
// undeclared name does, and it runs in the same scope as the declarations.
vm.runInContext(ctxSrc +
  "\n__EXPORT__ = { CORPUS, ALIAS, TEACH, ORDER, CARD, QC_BANK, QC_PARTS, QC_INVENTED };", ctx);
const { CORPUS, ALIAS, TEACH, ORDER, CARD, QC_BANK, QC_PARTS, QC_INVENTED } = ctx.__EXPORT__ || {};
if (!CORPUS || !ORDER || !CARD) throw new Error("captured nothing from the source files");
// A list, in ORDER. Nothing downstream can re-sort a list.
const chapters = ORDER.map(k => ({ key: k, ...CORPUS[k], card: CARD[k] }));
if (chapters.length !== 14) throw new Error("expected 14 chapters");
for (const c of chapters)
  if (!c.name || !c.stages || !c.card) throw new Error("incomplete: " + c.key);
fs.writeFileSync("content/corpus.json",
  JSON.stringify({ order: ORDER, chapters, alias: ALIAS, teach: TEACH }, null, 1));
fs.writeFileSync("content/qc_bank.json", JSON.stringify(
  { bank: QC_BANK, parts: QC_PARTS, invented: QC_INVENTED }, null, 1));
console.log("bank:", QC_BANK.length);
