window.difyChatbotConfig = {
  token: 'Fih8ltzxZ1A67IG6',
  inputs: {},
  systemVariables: {},
  userVariables: {}
};

(function() {
  // Load Dify embed script
  var script = document.createElement('script');
  script.src = 'https://udify.app/embed.min.js';
  script.id = 'Fih8ltzxZ1A67IG6';
  script.defer = true;
  document.head.appendChild(script);

  // Apply styles
  var style = document.createElement('style');
  style.textContent = [
    '#dify-chatbot-bubble-button { background-color: #1C64F2 !important; }',
    '#dify-chatbot-bubble-window { width: 24rem !important; height: 40rem !important; }'
  ].join(' ');
  document.head.appendChild(style);
})();
