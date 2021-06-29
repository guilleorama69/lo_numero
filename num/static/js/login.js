let socket = io.connect();

let enviar = function () {
  let data = document.getElementById("msg_text");
  console.log(data.value);
  socket.send(data.value);
  data.value = "";
};
socket.on("message", function (data) {
  console.log("Status changed: ", data);
});

let online = function () {
  socket.send("login", { user: document.getElementById("login_email").value });
};
// let offline = function () {
//   socket.emit("logout", { username: "{{name}}", id: "{{id}}" });
// };
socket.on("message");
let enviar_tirada = function () {
  let data = document.getElementById("id_tirada");
  console.log(data.value);
  socket.emit("message", { data: data.value });
  data.value = "";
};
