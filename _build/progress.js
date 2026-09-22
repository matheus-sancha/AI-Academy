/* One-time migration of saved progress to the level-free key (tickets #4 and #13).
   Old: aiem:<track>:<MODULE>-<topic>   e.g. aiem:beginner:B1-tokens
   New: aiem:<topic>                    e.g. aiem:tokens
   Topic ids did not change in the re-cut, so dropping the track and the module prefix lands every tick on its topic.
   Loaded before each page's own progress script. Safe to delete a release or two after the re-cut ships. */
(function(){
  var OLD = /^aiem:(beginner|advanced):/;
  try {
    var keys = [];
    for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (OLD.test(k)) keys.push(k); }
    keys.forEach(function(k){
      var rest = k.replace(OLD, ""), cut = rest.indexOf("-"), id = cut > -1 ? rest.slice(cut + 1) : rest;
      if (localStorage.getItem("aiem:" + id) === null) localStorage.setItem("aiem:" + id, localStorage.getItem(k));
      localStorage.removeItem(k);
    });
  } catch(e) {}
})();
