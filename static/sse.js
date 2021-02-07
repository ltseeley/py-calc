// This file handles receiving new calculations from the server

// The max number of previous calculations to show
const CALCULATION_LIMIT = 10;

var source = new EventSource("/calculations/stream");
source.onmessage = function(event) {
  let calculations_div = $("#calculations")
  var calculations = calculations_div.children();

  // If the calculations limit has already been reached, remove the oldest
  // one(s)
  if (calculations.length >= CALCULATION_LIMIT) {
    calculations.slice(CALCULATION_LIMIT-1).remove();
  }

  calculations_div.prepend("<p>" + event.data + "</p>");
};
