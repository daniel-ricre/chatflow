(function() {
  var script = document.currentScript;
  var chatbotId = script.getAttribute('data-chatbot') || '1';
  var chatHistory = []; // MEMORIA de la conversación

  var style = document.createElement('style');
  style.textContent = `
    #chatflow-widget { position:fixed; bottom:20px; right:20px; z-index:9999; font-family:Arial,sans-serif; }
    #chatflow-bubble { width:60px; height:60px; background:#4F46E5; border-radius:50%; cursor:pointer; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 12px rgba(0,0,0,0.15); }
    #chatflow-bubble:hover { transform:scale(1.1); }
    #chatflow-bubble svg { width:28px; height:28px; fill:white; }
    #chatflow-window { display:none; position:absolute; bottom:70px; right:0; width:350px; height:450px; background:white; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.15); flex-direction:column; overflow:hidden; }
    #chatflow-window.open { display:flex; }
    #chatflow-header { background:#4F46E5; color:white; padding:15px; font-weight:bold; }
    #chatflow-messages { flex:1; overflow-y:auto; padding:15px; background:#F9FAFB; display:flex; flex-direction:column; }
    .msg { margin-bottom:10px; padding:10px 14px; border-radius:12px; max-width:80%; font-size:14px; line-height:1.4; }
    .msg.bot { background:#E5E7EB; color:#333; align-self:flex-start; }
    .msg.user { background:#4F46E5; color:white; align-self:flex-end; }
    #chatflow-input-area { display:flex; padding:10px; border-top:1px solid #E5E7EB; }
    #chatflow-input { flex:1; padding:10px; border:1px solid #ddd; border-radius:20px; outline:none; font-size:14px; }
    #chatflow-send { margin-left:8px; background:#4F46E5; color:white; border:none; border-radius:20px; padding:10px 18px; cursor:pointer; }
  `;
  document.head.appendChild(style);

  var html = document.createElement('div');
  html.id = 'chatflow-widget';
  html.innerHTML = `
    <div id="chatflow-bubble" onclick="document.getElementById('chatflow-window').classList.toggle('open')">
      <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
    </div>
    <div id="chatflow-window">
      <div id="chatflow-header">💬 Chat</div>
      <div id="chatflow-messages"><div class="msg bot">¡Hola! ¿En qué puedo ayudarte?</div></div>
      <div id="chatflow-input-area">
        <input id="chatflow-input" placeholder="Escribe..." onkeydown="if(event.key==='Enter')sendMsg()">
        <button id="chatflow-send" onclick="sendMsg()">Enviar</button>
      </div>
    </div>
  `;
  document.body.appendChild(html);

  window.sendMsg = async function() {
    var input = document.getElementById('chatflow-input');
    var msg = input.value.trim();
    if (!msg) return;
    var messages = document.getElementById('chatflow-messages');
    messages.innerHTML += '<div class="msg user">' + msg + '</div>';
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    // Guardar en historial local
    chatHistory.push({role: 'user', content: msg});

    try {
      var resp = await fetch('https://chatflow-api-oj45.onrender.com/api/v1/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          chatbot_id: parseInt(chatbotId),
          message: msg,
          history: chatHistory.slice(0, -1) // enviar historial sin el último mensaje
        })
      });
      var data = await resp.json();
      messages.innerHTML += '<div class="msg bot">' + data.response + '</div>';
      chatHistory.push({role: 'assistant', content: data.response});
      messages.scrollTop = messages.scrollHeight;
    } catch(e) {
      messages.innerHTML += '<div class="msg bot">Error</div>';
    }
  };
})();
