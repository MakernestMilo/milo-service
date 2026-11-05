// MakerNest Milo · the chapter page. No framework, no tracking, nothing sent except the chat.
(function () {
  "use strict";
  var page = document.body.dataset;
  var level = page.level, chapter = page.chapter;

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  // One random id per browser. It names the conversation and nothing else.
  function sessionId() {
    var id = store("milo.session");
    if (!id || !/^[A-Za-z0-9_-]{16,64}$/.test(id)) {
      var a = new Uint8Array(16);
      (window.crypto || window.msCrypto).getRandomValues(a);
      id = Array.prototype.map.call(a, function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
      store("milo.session", id);
    }
    return id;
  }

  function copyText(text, btn) {
    function done() { var t = btn.textContent; btn.textContent = "Copied"; setTimeout(function () { btn.textContent = t; }, 1600); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(); });
    } else { fallback(); }
    function fallback() {
      var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch (e) { btn.textContent = "Select and copy"; }
      document.body.removeChild(ta);
    }
  }

  // Copy buttons on the page's own code blocks.
  Array.prototype.forEach.call(document.querySelectorAll("[data-copy]"), function (btn) {
    btn.addEventListener("click", function () {
      var el = document.getElementById(btn.getAttribute("data-copy"));
      if (el) copyText(el.textContent, btn);
    });
  });

  // Where the maker says they are. Remembered per chapter in this browser.
  var where = document.getElementById("where");
  var posKey = "milo.pos." + level + "." + chapter;
  if (where) {
    var saved = store(posKey);
    if (saved) { where.value = saved; }
    where.addEventListener("change", function () { store(posKey, where.value); });
  }

  // The chat.
  var chat = document.getElementById("chat"), form = document.getElementById("ask"), box = document.getElementById("ask-text");
  if (!chat || !form) return;
  var sid = sessionId(), busy = false;
  var api = "/api/" + level + "/" + chapter;

  // A reply is plain text with ``` fences for code. Built with textContent only: nothing Milo
  // says is ever parsed as HTML.
  function render(who, text) {
    var div = document.createElement("div");
    div.className = "msg " + (who === "maker" ? "maker" : who === "wait" ? "wait" : "milo-says");
    var parts = String(text).split("```");
    parts.forEach(function (p, i) {
      if (i % 2 === 1) {
        var code = p.replace(/^[a-zA-Z+]*\n/, "");
        var pre = document.createElement("pre"); pre.textContent = code.replace(/\n$/, "");
        div.appendChild(pre);
        var b = document.createElement("button"); b.type = "button"; b.className = "btn copy"; b.textContent = "Copy code";
        b.addEventListener("click", function () { copyText(pre.textContent, b); });
        div.appendChild(b);
      } else if (p.trim()) {
        div.appendChild(document.createTextNode(p.replace(/^\n+|\n+$/g, "")));
      }
    });
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
  }

  function post(url, body) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { j._status = r.status; return j; }); });
  }

  fetch(api + "/history?session=" + encodeURIComponent(sid))
    .then(function (r) { return r.ok ? r.json() : { turns: [] }; })
    .then(function (j) {
      if (!j.turns || !j.turns.length) { render("milo", chat.dataset.hello); return; }
      j.turns.forEach(function (t) { render(t.who, t.said); });
    })
    .catch(function () { render("milo", chat.dataset.hello); });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var text = box.value.trim();
    if (!text || busy) return;
    busy = true; box.value = "";
    render("maker", text);
    var wait = render("wait", "Milo is thinking…");
    post(api + "/turn", { session: sid, text: text, position: where ? where.value || null : null, tab: location.hash.replace("#", "") || null })
      .then(function (j) {
        wait.remove();
        render("milo", j.reply || "I couldn't answer just then. Try again in a minute.");
        if (j.retry && !box.value) { box.value = text; }   // nothing was kept: let them send it again
        if (j.note) { render("wait", j.note); }
      })
      .catch(function () {
        wait.remove();
        if (!box.value) { box.value = text; }
        render("milo", "I can't reach the internet right now. Check the connection and try again. The book has everything you need for this step.");
      })
      .then(function () { busy = false; box.focus(); });
  });

  box.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing && box.value.indexOf("\n") === -1 && box.value.length < 300) {
      e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit"));
    }
  });
})();
