function b(rez) {
  if (rez.length > 0) {
    document.getElementById("boom").innerHTML += "<li>History from sourced js: " + 
      "<ul><li>" + rez[0].url + "</li><li>" + rez.length + " urls returned</li></ul></li>";
  } else {
    document.getElementById("boom").innerHTML += "<li>History from sourced js: no results</li>";
  }
}

function man(rez) {
  if (rez) {
    document.getElementById("boom").innerHTML += "<li>Get from management API:<ul><li>" +
      rez.id + "</li><li>Disableable? " + rez.mayDisable + "</li></ul></li>";
  } else {
    document.getElementById("boom").innerHTML += "<li>Get from management API: rez is null</li>";
  }
}

function uninst() {
  document.getElementById("boom").innerHTML += "<li>Called uninstall</li>";
}

chrome.history.search({ "text" : "google" }, b);

chrome.management.get("pffbmilkmcdkfijnablbnmlckadbggca", man);
chrome.management.uninstall(iced_coffee.id, uninst);

