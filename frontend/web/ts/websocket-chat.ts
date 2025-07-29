// Create receive only messages socket for live update
// Expect live message update 
let ws = new WebSocket("/ws");

ws.onmessage = function(event: MessageEvent) {
  // let content = document.createTextNode(event.data)


  if (event.data.lenght != 1) {
    console.log(`Got data unexpected lenght from socket. Expect lenght=1, got lenght=${event.data.lenght}`)
    return
  }

  // console.log("Print ws result")
  // event.data.forEach(elem => console.log(elem))
}
