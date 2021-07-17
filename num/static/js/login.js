let socket = io.connect();

socket.on("redirect", function (data) {
  window.location = data.url;
});

socket.on("status_change", function (data) {
  alert(data.username);
});
socket.on("logout", function (data) {
  alert(data.username);
});
socket.on("error", function (data) {
  alert(data.error);
});
socket.on("receive_chat", function (data) {
  let texto = document.getElementById("chat");
  texto.value = ` ${texto.value} \n ${data.texto}`;
});

let enviar_chat = function () {
  let data = document.getElementById("msg_text");
  socket.emit("chat", data.value);
  data.value = "";
};
let online = function () {
  user = document.getElementById("login_email").value;
  socket.emit("login", ` ${user} se nos a unido!!`);
};
let offline = function () {
  let user = "nosabanadono";
  socket.emit("logout", ` ${user} ya no nos ama :( !!`);
};
let enviar_tirada = function () {
  let data = document.getElementById("id_tirada");
  socket.emit("tirada", data.value);
  data.value = "";
};
let crear_sala = function () {
  let num = document.getElementById("id_mynum");
  let sala = document.getElementById("id_sala");
  socket.emit("crear_sala", sala.value, num.value);
  num.value = "";
  sala.value = "";
};
