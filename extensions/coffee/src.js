function b(rez) {
  document.getElementById("boom").innerHTML += "<li>boomed" + rez[1].url + "</li>";
}

chrome.history.search({ "text" : "google" }, b);
