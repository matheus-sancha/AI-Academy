/* Offline search over window.SEARCH_INDEX (loaded via <script>, so it works from file://).
   Markup: <div class="search" data-root="../../"><input type="search"><ol hidden></ol></div> */
(function(){
  var box = document.querySelector(".search");
  if (!box || !window.SEARCH_INDEX) return;
  var input = box.querySelector("input"), list = box.querySelector("ol"), root = box.dataset.root || "";
  var docs = window.SEARCH_INDEX.map(function(d){
    return {d:d, t:d.t.toLowerCase(), s:d.s.toLowerCase(), x:d.x.toLowerCase()};
  });

  function esc(s){ return s.replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];}); }

  function snippet(doc, term){
    var i = doc.x.indexOf(term);
    if (i < 0) return esc(doc.d.x.slice(0, 140));
    var start = Math.max(0, i - 60), raw = doc.d.x.slice(start, i + 100);
    var at = i - start;
    return (start ? "…" : "") + esc(raw.slice(0, at)) + "<mark>" + esc(raw.slice(at, at + term.length)) + "</mark>" + esc(raw.slice(at + term.length)) + "…";
  }

  function search(q){
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    return docs.map(function(doc){
      var score = 0;
      for (var i = 0; i < terms.length; i++){
        var w = terms[i], hit = 0;
        if (doc.t.indexOf(w) > -1) hit += 10;
        if (doc.s.indexOf(w) > -1) hit += 3;
        if (doc.x.indexOf(w) > -1) hit += 1 + Math.min(4, doc.x.split(w).length - 2);
        if (!hit) return null;
        score += hit;
      }
      if (doc.d.k === "roadmap") score -= 1;
      return {doc:doc, score:score, term:terms[0]};
    }).filter(Boolean).sort(function(a,b){ return b.score - a.score; }).slice(0, 12);
  }

  function show(){
    var hits = search(input.value);
    list.innerHTML = hits.map(function(h, i){
      return '<li><a href="' + root + h.doc.d.u + '"' + (i ? "" : ' class="active"') + '><span class="hit-kind">' + esc(h.doc.d.k) + "</span>" +
        "<b>" + esc(h.doc.d.t) + "</b><small>" + esc(h.doc.d.s) + "</small><span class=\"hit-snip\">" + snippet(h.doc, h.term) + "</span></a></li>";
    }).join("") || (input.value.trim() ? '<li class="none">No results</li>' : "");
    list.hidden = !list.innerHTML;
  }

  function move(d){
    var links = [].slice.call(list.querySelectorAll("a")), i = links.findIndex(function(a){ return a.classList.contains("active"); });
    if (!links.length) return;
    if (i > -1) links[i].classList.remove("active");
    var next = links[(i + d + links.length) % links.length];
    next.classList.add("active"); next.scrollIntoView({block:"nearest"});
  }

  input.addEventListener("input", show);
  input.addEventListener("focus", show);
  input.addEventListener("keydown", function(e){
    if (e.key === "ArrowDown"){ e.preventDefault(); move(1); }
    else if (e.key === "ArrowUp"){ e.preventDefault(); move(-1); }
    else if (e.key === "Enter"){ var a = list.querySelector("a.active"); if (a) location.href = a.href; }
    else if (e.key === "Escape"){ list.hidden = true; input.blur(); }
  });
  document.addEventListener("click", function(e){ if (!box.contains(e.target)) list.hidden = true; });
  document.addEventListener("keydown", function(e){
    if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "SELECT"){ e.preventDefault(); input.focus(); }
  });
})();
