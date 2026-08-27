/* Прогресс игрока в localStorage: звёзды по темам, выученные слова, настройки.
   Всё обёрнуто в try/catch — в приватном окне хранилище может быть недоступно. */
(function () {
  'use strict';

  var KEY = 'espanol-para-ninos:v1';

  var DEFAULTS = {
    stars: {},        // topicId -> количество звёзд (0..3)
    learned: {},      // "topicId|es" -> true
    xp: 0,
    bestStreak: 0,
    music: false,
    sound: true
  };

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return Object.assign({}, DEFAULTS);
      return Object.assign({}, DEFAULTS, JSON.parse(raw));
    } catch (e) {
      return Object.assign({}, DEFAULTS);
    }
  }

  function write(data) {
    try {
      localStorage.setItem(KEY, JSON.stringify(data));
    } catch (e) {
      /* Хранилище недоступно — играем без сохранения. */
    }
  }

  var state = read();

  window.Progress = {
    get: function (key) {
      return state[key];
    },
    setSetting: function (key, value) {
      state[key] = value;
      write(state);
    },
    starsFor: function (topicId) {
      return state.stars[topicId] || 0;
    },
    awardStars: function (topicId, stars) {
      if (stars > (state.stars[topicId] || 0)) {
        state.stars[topicId] = stars;
        write(state);
      }
    },
    totalStars: function () {
      return window.TOPICS.reduce(function (sum, topic) {
        return sum + (state.stars[topic.id] || 0);
      }, 0);
    },
    isLearned: function (topicId, es) {
      return !!state.learned[topicId + '|' + es];
    },
    markLearned: function (topicId, es, learned) {
      var k = topicId + '|' + es;
      if (learned) state.learned[k] = true;
      else delete state.learned[k];
      write(state);
    },
    learnedInTopic: function (topicId) {
      var topic = window.TOPICS.find(function (t) { return t.id === topicId; });
      if (!topic) return 0;
      return topic.words.filter(function (w) {
        return state.learned[topicId + '|' + w.es];
      }).length;
    },
    totalLearned: function () {
      return Object.keys(state.learned).length;
    },
    addXp: function (amount) {
      state.xp += amount;
      write(state);
      return state.xp;
    },
    recordStreak: function (streak) {
      if (streak > state.bestStreak) {
        state.bestStreak = streak;
        write(state);
      }
    },
    reset: function () {
      var keepMusic = state.music;
      var keepSound = state.sound;
      state = Object.assign({}, DEFAULTS, { music: keepMusic, sound: keepSound });
      write(state);
    }
  };
})();
