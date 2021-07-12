let socket = io.connect();

let enviar = function () {
  let data = document.getElementById("msg_text");
  socket.send(data.value);
  data.value = "";
};

socket.on("status_change", function (data) {
  alert(data);
});

let online = function () {
  socket.emit("login", { user: document.getElementById("login_email").value });
};
let offline = function () {
  socket.emit("logout", { username: "{{name}}", id: "{{id}}" });
};
let enviar_tirada = function () {
  let data = document.getElementById("id_tirada");
  socket.emit("tirada", data.value);
  data.value = "";
};
let crear_sala = function () {
  let data = document.getElementById("id_sala");
  socket.emit("crear_sala", data.value);
  data.value = "";
};
