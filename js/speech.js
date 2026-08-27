/* Произношение слов на испанском через Web Speech API.
   Если синтеза нет — кнопки озвучки прячутся. */
(function () {
  'use strict';

  var synth = window.speechSynthesis;
  var voice = null;

  function pickVoice() {
    if (!synth) return;
    var voices = synth.getVoices();
    if (!voices.length) return;
    voice = voices.find(function (v) { return /^es[-_]ES/i.test(v.lang); })
      || voices.find(function (v) { return /^es/i.test(v.lang); })
      || null;
  }

  if (synth) {
    pickVoice();
    if (typeof synth.onvoiceschanged !== 'undefined') {
      synth.addEventListener('voiceschanged', pickVoice);
    }
  }

  window.Speech = {
    supported: !!synth,
    say: function (text) {
      if (!synth) return;
      try {
        synth.cancel();
        var utter = new SpeechSynthesisUtterance(text);
        utter.lang = voice ? voice.lang : 'es-ES';
        if (voice) utter.voice = voice;
        utter.rate = 0.85;
        utter.pitch = 1.05;
        synth.speak(utter);
      } catch (e) {
        /* Озвучка недоступна — не мешаем игре. */
      }
    }
  };
})();
