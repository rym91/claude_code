/* Звуки успеха/ошибки генерируются через Web Audio — отдельные файлы не нужны.
   Фоновая музыка — mp3 из assets/audio. */
(function () {
  'use strict';

  var ctx = null;

  function audioContext() {
    if (!ctx) {
      var Ctor = window.AudioContext || window.webkitAudioContext;
      if (!Ctor) return null;
      ctx = new Ctor();
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function tone(freq, startAt, duration, type, volume) {
    var ac = audioContext();
    if (!ac) return;
    var osc = ac.createOscillator();
    var gain = ac.createGain();
    osc.type = type || 'sine';
    osc.frequency.value = freq;
    var t0 = ac.currentTime + startAt;
    gain.gain.setValueAtTime(0.0001, t0);
    gain.gain.exponentialRampToValueAtTime(volume || 0.18, t0 + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, t0 + duration);
    osc.connect(gain).connect(ac.destination);
    osc.start(t0);
    osc.stop(t0 + duration + 0.05);
  }

  function play(notes) {
    if (!window.Progress.get('sound')) return;
    notes.forEach(function (n) {
      tone(n[0], n[1], n[2], n[3], n[4]);
    });
  }

  var music = null;

  window.Sfx = {
    correct: function () {
      play([[660, 0, 0.14], [880, 0.1, 0.2]]);
    },
    wrong: function () {
      play([[300, 0, 0.18, 'sawtooth', 0.12], [200, 0.12, 0.25, 'sawtooth', 0.12]]);
    },
    flip: function () {
      play([[520, 0, 0.09, 'triangle', 0.1]]);
    },
    win: function () {
      play([[523, 0, 0.16], [659, 0.14, 0.16], [784, 0.28, 0.18], [1047, 0.44, 0.34]]);
    },
    click: function () {
      play([[440, 0, 0.06, 'triangle', 0.08]]);
    },

    /* Фоновая музыка. Браузер запускает её только после действия пользователя. */
    initMusic: function () {
      if (music) return music;
      music = new Audio('assets/audio/background-music.mp3');
      music.loop = true;
      music.volume = 0.18;
      return music;
    },
    setMusic: function (on) {
      var el = window.Sfx.initMusic();
      if (on) {
        var promise = el.play();
        if (promise && promise.catch) promise.catch(function () { /* автозапуск запрещён */ });
      } else {
        el.pause();
      }
    }
  };
})();
