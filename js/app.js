/* Точка входа: маршрутизация между экранами и игровые режимы. */
(function () {
  'use strict';

  var root = document.getElementById('app');
  var liveRegion = document.getElementById('live');

  /* ---------- Мелкие помощники ---------- */

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (key) {
      var value = attrs[key];
      if (key === 'class') node.className = value;
      else if (key === 'text') node.textContent = value;
      else if (key === 'html') node.innerHTML = value;
      else if (key.indexOf('on') === 0) node.addEventListener(key.slice(2), value);
      else if (value !== null && value !== undefined) node.setAttribute(key, value);
    });
    (children || []).forEach(function (child) {
      if (child) node.appendChild(child);
    });
    return node;
  }

  function shuffle(items) {
    var copy = items.slice();
    for (var i = copy.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = copy[i];
      copy[i] = copy[j];
      copy[j] = tmp;
    }
    return copy;
  }

  function announce(message) {
    liveRegion.textContent = message;
  }

  function starsForRatio(ratio) {
    if (ratio >= 0.9) return 3;
    if (ratio >= 0.7) return 2;
    if (ratio >= 0.5) return 1;
    return 0;
  }

  function starRow(count, size) {
    return el('div', { class: 'stars ' + (size || '') }, [0, 1, 2].map(function (i) {
      return el('span', { class: 'star' + (i < count ? ' star--on' : ''), text: i < count ? '⭐' : '☆' });
    }));
  }

  function speakButton(text, extraClass) {
    if (!window.Speech.supported) return null;
    return el('button', {
      class: 'btn btn--speak ' + (extraClass || ''),
      type: 'button',
      'aria-label': 'Послушать: ' + text,
      onclick: function (event) {
        event.stopPropagation();
        window.Speech.say(text);
      }
    }, [el('span', { text: '🔊', 'aria-hidden': 'true' })]);
  }

  function backButton(onBack, label) {
    return el('button', {
      class: 'btn btn--ghost btn--back',
      type: 'button',
      onclick: function () { window.Sfx.click(); onBack(); }
    }, [el('span', { text: '←　' + (label || 'Назад') })]);
  }

  /* Набор слов темы; id 'all' — все слова вперемешку. */
  function wordsOf(topicId) {
    if (topicId === 'all') return window.ALL_WORDS;
    var topic = window.TOPICS.find(function (t) { return t.id === topicId; });
    return topic ? topic.words : [];
  }

  function topicOf(topicId) {
    if (topicId === 'all') {
      return { id: 'all', title: 'Всё вперемешку', titleEs: 'Todo', emoji: '🎲', color: '#ffd166' };
    }
    return window.TOPICS.find(function (t) { return t.id === topicId; });
  }

  /* Варианты-обманки: сперва из той же темы, при нехватке — из общего списка. */
  function distractors(correct, count, pool, field) {
    var candidates = pool.filter(function (w) { return w[field] !== correct[field]; });
    var picked = shuffle(candidates).slice(0, count);
    if (picked.length < count) {
      var extra = shuffle(window.ALL_WORDS).filter(function (w) {
        return w[field] !== correct[field] && !picked.some(function (p) { return p[field] === w[field]; });
      });
      picked = picked.concat(extra.slice(0, count - picked.length));
    }
    return picked;
  }

  /* ---------- Шапка ---------- */

  function refreshHeader() {
    document.getElementById('stat-stars').textContent = window.Progress.totalStars();
    document.getElementById('stat-words').textContent = window.Progress.totalLearned();
    document.getElementById('stat-xp').textContent = window.Progress.get('xp');
  }

  /* ---------- Экран: список тем ---------- */

  function screenHome() {
    var grid = el('div', { class: 'grid' });

    window.TOPICS.forEach(function (topic) {
      var learned = window.Progress.learnedInTopic(topic.id);
      grid.appendChild(el('button', {
        class: 'topic-card',
        type: 'button',
        style: '--topic-color:' + topic.color,
        onclick: function () { window.Sfx.click(); render('topic', { topicId: topic.id }); }
      }, [
        el('span', { class: 'topic-card__emoji', text: topic.emoji, 'aria-hidden': 'true' }),
        el('span', { class: 'topic-card__title', text: topic.title }),
        el('span', { class: 'topic-card__subtitle', text: topic.titleEs }),
        starRow(window.Progress.starsFor(topic.id), 'stars--sm'),
        el('span', { class: 'topic-card__count', text: learned + ' / ' + topic.words.length + ' выучено' })
      ]));
    });

    var mixed = topicOf('all');
    grid.appendChild(el('button', {
      class: 'topic-card topic-card--wide',
      type: 'button',
      style: '--topic-color:' + mixed.color,
      onclick: function () { window.Sfx.click(); render('topic', { topicId: 'all' }); }
    }, [
      el('span', { class: 'topic-card__emoji', text: mixed.emoji, 'aria-hidden': 'true' }),
      el('span', { class: 'topic-card__title', text: mixed.title }),
      el('span', { class: 'topic-card__subtitle', text: window.ALL_WORDS.length + ' слов из всех тем' })
    ]));

    return el('section', { class: 'screen' }, [
      el('h2', { class: 'screen__title', text: 'Выбери тему' }),
      grid,
      el('button', {
        class: 'btn btn--ghost btn--reset',
        type: 'button',
        onclick: function () {
          if (window.confirm('Сбросить весь прогресс?')) {
            window.Progress.reset();
            refreshHeader();
            render('home');
          }
        }
      }, [el('span', { text: 'Сбросить прогресс' })])
    ]);
  }

  /* ---------- Экран: выбор режима ---------- */

  function screenTopic(params) {
    var topic = topicOf(params.topicId);
    var words = wordsOf(params.topicId);

    var modes = [
      { id: 'cards',  emoji: '🃏', title: 'Карточки',  hint: 'Смотри, слушай, запоминай' },
      { id: 'quiz',   emoji: '❓', title: 'Викторина', hint: 'Выбери правильный перевод' },
      { id: 'listen', emoji: '👂', title: 'На слух',   hint: 'Послушай и угадай слово' },
      { id: 'memory', emoji: '🧩', title: 'Мемори',    hint: 'Найди пары слов' }
    ].filter(function (mode) {
      return mode.id !== 'listen' || window.Speech.supported;
    });

    var list = el('div', { class: 'modes' }, modes.map(function (mode) {
      return el('button', {
        class: 'mode-card',
        type: 'button',
        onclick: function () { window.Sfx.click(); render(mode.id, { topicId: params.topicId }); }
      }, [
        el('span', { class: 'mode-card__emoji', text: mode.emoji, 'aria-hidden': 'true' }),
        el('span', { class: 'mode-card__body' }, [
          el('span', { class: 'mode-card__title', text: mode.title }),
          el('span', { class: 'mode-card__hint', text: mode.hint })
        ]),
        el('span', { class: 'mode-card__arrow', text: '▶', 'aria-hidden': 'true' })
      ]);
    }));

    return el('section', { class: 'screen', style: '--topic-color:' + topic.color }, [
      backButton(function () { render('home'); }, 'К темам'),
      el('div', { class: 'topic-head' }, [
        el('span', { class: 'topic-head__emoji', text: topic.emoji, 'aria-hidden': 'true' }),
        el('div', {}, [
          el('h2', { class: 'screen__title', text: topic.title }),
          el('p', { class: 'screen__subtitle', text: topic.titleEs + ' · ' + words.length + ' слов' })
        ]),
        starRow(window.Progress.starsFor(topic.id))
      ]),
      list
    ]);
  }

  /* ---------- Режим: карточки ---------- */

  function screenCards(params) {
    var topic = topicOf(params.topicId);
    var words = shuffle(wordsOf(params.topicId));
    var index = 0;
    var flipped = false;

    var cardHost = el('div', { class: 'card-host' });
    var counter = el('p', { class: 'counter' });
    var knowBtn = el('button', { class: 'btn btn--primary', type: 'button' });

    function currentTopicId(word) {
      return word.topicId || params.topicId;
    }

    var innerEl = null;

    function refreshKnowButton() {
      var word = words[index];
      var learned = window.Progress.isLearned(currentTopicId(word), word.es);
      knowBtn.textContent = learned ? '\u2705 \u0412\u044b\u0443\u0447\u0435\u043d\u043e' : '\u042f \u0437\u043d\u0430\u044e \u044d\u0442\u043e \u0441\u043b\u043e\u0432\u043e';
      knowBtn.classList.toggle('btn--done', learned);
    }

    function draw() {
      var word = words[index];
      counter.textContent = (index + 1) + ' / ' + words.length;

      var inner = el('div', { class: 'flashcard__inner' }, [
        el('div', { class: 'flashcard__face flashcard__face--front' }, [
          el('span', { class: 'flashcard__emoji', text: word.emoji, 'aria-hidden': 'true' }),
          el('span', { class: 'flashcard__word', text: word.es }),
          speakButton(word.es),
          el('span', { class: 'flashcard__hint', text: 'Нажми, чтобы увидеть перевод' })
        ]),
        el('div', { class: 'flashcard__face flashcard__face--back' }, [
          el('span', { class: 'flashcard__emoji', text: word.emoji, 'aria-hidden': 'true' }),
          el('span', { class: 'flashcard__word', text: word.ru }),
          el('span', { class: 'flashcard__hint', text: word.es })
        ])
      ]);

      var card = el('div', {
        class: 'flashcard',
        role: 'button',
        tabindex: '0',
        'aria-label': 'Карточка ' + word.es + '. Нажми, чтобы перевернуть.',
        onclick: flip,
        onkeydown: function (event) {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            flip();
          }
        }
      }, [inner]);

      cardHost.innerHTML = '';
      cardHost.appendChild(card);
      innerEl = inner;
      refreshKnowButton();
    }

    /* Переворачиваем классом, а не перерисовкой — иначе пропадёт анимация. */
    function flip() {
      flipped = !flipped;
      innerEl.classList.toggle('is-flipped', flipped);
      window.Sfx.flip();
      if (flipped) window.Speech.say(words[index].es);
    }

    function step(delta) {
      var next = index + delta;
      if (next < 0 || next >= words.length) return;
      index = next;
      flipped = false;
      window.Sfx.click();
      draw();
    }

    knowBtn.addEventListener('click', function () {
      var word = words[index];
      var tid = currentTopicId(word);
      var learned = !window.Progress.isLearned(tid, word.es);
      window.Progress.markLearned(tid, word.es, learned);
      if (learned) {
        window.Progress.addXp(2);
        window.Sfx.correct();
        announce('Слово ' + word.es + ' отмечено как выученное');
      }
      refreshHeader();
      refreshKnowButton();
      if (learned && index < words.length - 1) window.setTimeout(function () { step(1); }, 350);
    });

    draw();

    return el('section', { class: 'screen', style: '--topic-color:' + topic.color }, [
      backButton(function () { render('topic', params); }, topic.title),
      counter,
      cardHost,
      el('div', { class: 'row' }, [
        el('button', {
          class: 'btn btn--ghost', type: 'button', 'aria-label': 'Предыдущее слово',
          onclick: function () { step(-1); }
        }, [el('span', { text: '◀' })]),
        knowBtn,
        el('button', {
          class: 'btn btn--ghost', type: 'button', 'aria-label': 'Следующее слово',
          onclick: function () { step(1); }
        }, [el('span', { text: '▶' })])
      ])
    ]);
  }

  /* ---------- Режимы «Викторина» и «На слух» ---------- */

  function screenQuestions(params, mode) {
    var topic = topicOf(params.topicId);
    var pool = wordsOf(params.topicId);
    var total = Math.min(10, pool.length);
    var questions = shuffle(pool).slice(0, total);
    var index = 0;
    var correctCount = 0;
    var streak = 0;
    var bestStreak = 0;
    var locked = false;

    var counter = el('p', { class: 'counter' });
    var scoreLine = el('p', { class: 'counter counter--score' });
    var promptHost = el('div', { class: 'prompt' });
    var optionsHost = el('div', { class: 'options' });
    var bar = el('div', { class: 'progressbar__fill' });

    function drawQuestion() {
      locked = false;
      var word = questions[index];
      /* В викторине чередуем направление перевода, на слух — всегда с испанского. */
      var ruToEs = mode === 'quiz' ? index % 2 === 0 : false;
      var field = ruToEs ? 'es' : 'ru';

      counter.textContent = 'Вопрос ' + (index + 1) + ' из ' + total;
      scoreLine.textContent = 'Верно: ' + correctCount + (streak > 1 ? ' · серия ' + streak + ' 🔥' : '');
      bar.style.width = (index / total * 100) + '%';

      promptHost.innerHTML = '';
      if (mode === 'listen') {
        promptHost.appendChild(el('button', {
          class: 'listen-btn', type: 'button',
          onclick: function () { window.Speech.say(word.es); }
        }, [
          el('span', { class: 'listen-btn__icon', text: '🔊', 'aria-hidden': 'true' }),
          el('span', { class: 'listen-btn__label', text: 'Послушай ещё раз' })
        ]));
        window.Speech.say(word.es);
      } else {
        promptHost.appendChild(el('span', { class: 'prompt__emoji', text: word.emoji, 'aria-hidden': 'true' }));
        promptHost.appendChild(el('span', { class: 'prompt__word', text: ruToEs ? word.ru : word.es }));
        promptHost.appendChild(el('span', {
          class: 'prompt__hint',
          text: ruToEs ? 'Как это по-испански?' : 'Что это значит?'
        }));
        if (!ruToEs) {
          var speak = speakButton(word.es);
          if (speak) promptHost.appendChild(speak);
        }
      }

      var options = shuffle([word].concat(distractors(word, 3, pool, field)));
      optionsHost.innerHTML = '';
      options.forEach(function (option) {
        var label = mode === 'listen'
          ? option.emoji + '  ' + option.ru
          : option[field];
        var button = el('button', {
          class: 'option', type: 'button',
          onclick: function () { answer(button, option, word, options); }
        }, [el('span', { text: label })]);
        optionsHost.appendChild(button);
      });
    }

    function answer(button, option, word, options) {
      if (locked) return;
      locked = true;
      var isCorrect = option.es === word.es;

      Array.prototype.forEach.call(optionsHost.children, function (node, i) {
        node.disabled = true;
        if (options[i].es === word.es) node.classList.add('option--correct');
      });

      if (isCorrect) {
        correctCount++;
        streak++;
        if (streak > bestStreak) bestStreak = streak;
        window.Progress.addXp(5);
        window.Sfx.correct();
        announce('Верно! ' + word.es + ' — ' + word.ru);
      } else {
        streak = 0;
        button.classList.add('option--wrong');
        window.Sfx.wrong();
        announce('Неверно. ' + word.es + ' — ' + word.ru);
      }
      if (mode !== 'listen') window.Speech.say(word.es);
      refreshHeader();

      window.setTimeout(function () {
        index++;
        if (index >= total) finish();
        else drawQuestion();
      }, isCorrect ? 850 : 1500);
    }

    function finish() {
      window.Progress.recordStreak(bestStreak);
      var stars = starsForRatio(correctCount / total);
      window.Progress.awardStars(params.topicId, stars);
      refreshHeader();
      render('result', {
        topicId: params.topicId,
        mode: mode,
        stars: stars,
        summary: 'Правильных ответов: ' + correctCount + ' из ' + total,
        bestStreak: bestStreak
      });
    }

    drawQuestion();

    return el('section', { class: 'screen', style: '--topic-color:' + topic.color }, [
      backButton(function () { render('topic', params); }, topic.title),
      el('div', { class: 'progressbar' }, [bar]),
      counter,
      scoreLine,
      promptHost,
      optionsHost
    ]);
  }

  /* ---------- Режим: мемори ---------- */

  function screenMemory(params) {
    var topic = topicOf(params.topicId);
    var pool = wordsOf(params.topicId);
    var pairsCount = Math.min(6, pool.length);
    var pairs = shuffle(pool).slice(0, pairsCount);

    var deck = shuffle(pairs.reduce(function (acc, word, i) {
      acc.push({ key: i, side: 'es', word: word });
      acc.push({ key: i, side: 'ru', word: word });
      return acc;
    }, []));

    var opened = [];
    var matched = 0;
    var moves = 0;
    var locked = false;

    var movesLine = el('p', { class: 'counter' });
    var board = el('div', { class: 'memory' });

    function updateCounter() {
      movesLine.textContent = 'Пар найдено: ' + matched + ' из ' + pairsCount + ' · ходов: ' + moves;
    }

    deck.forEach(function (item, position) {
      var face = item.side === 'es'
        ? el('span', { class: 'memory__word', text: item.word.es })
        : el('span', { class: 'memory__word' }, [
            el('span', { class: 'memory__emoji', text: item.word.emoji, 'aria-hidden': 'true' }),
            el('span', { text: item.word.ru })
          ]);

      var card = el('button', {
        class: 'memory__card',
        type: 'button',
        'aria-label': 'Закрытая карточка ' + (position + 1),
        onclick: function () { open(card, item); }
      }, [
        el('span', { class: 'memory__back', text: '🇪🇸', 'aria-hidden': 'true' }),
        el('span', { class: 'memory__front' }, [face])
      ]);
      board.appendChild(card);
    });

    function open(card, item) {
      if (locked || card.classList.contains('is-open') || card.classList.contains('is-matched')) return;
      card.classList.add('is-open');
      card.setAttribute('aria-label', item.side === 'es' ? item.word.es : item.word.ru);
      window.Sfx.flip();
      if (item.side === 'es') window.Speech.say(item.word.es);
      opened.push({ card: card, item: item });

      if (opened.length < 2) return;
      moves++;
      updateCounter();

      var first = opened[0];
      var second = opened[1];
      opened = [];

      if (first.item.key === second.item.key) {
        matched++;
        first.card.classList.add('is-matched');
        second.card.classList.add('is-matched');
        window.Progress.addXp(4);
        window.Sfx.correct();
        refreshHeader();
        updateCounter();
        announce('Пара найдена: ' + first.item.word.es + ' — ' + first.item.word.ru);
        if (matched === pairsCount) window.setTimeout(finish, 700);
      } else {
        locked = true;
        window.Sfx.wrong();
        window.setTimeout(function () {
          [first, second].forEach(function (entry) {
            entry.card.classList.remove('is-open');
            entry.card.setAttribute('aria-label', 'Закрытая карточка');
          });
          locked = false;
        }, 900);
      }
    }

    function finish() {
      /* Идеальная игра — ровно по одному ходу на пару. */
      var stars = moves <= pairsCount + 2 ? 3 : moves <= pairsCount + 6 ? 2 : 1;
      window.Progress.awardStars(params.topicId, stars);
      refreshHeader();
      render('result', {
        topicId: params.topicId,
        mode: 'memory',
        stars: stars,
        summary: 'Все ' + pairsCount + ' пар найдены за ' + moves + ' ходов'
      });
    }

    updateCounter();

    return el('section', { class: 'screen', style: '--topic-color:' + topic.color }, [
      backButton(function () { render('topic', params); }, topic.title),
      movesLine,
      board
    ]);
  }

  /* ---------- Экран: результат ---------- */

  function screenResult(params) {
    var topic = topicOf(params.topicId);
    if (params.stars >= 2) window.Sfx.win();

    var praise = params.stars === 3 ? '¡Excelente! Великолепно!'
      : params.stars === 2 ? '¡Muy bien! Очень хорошо!'
      : params.stars === 1 ? '¡Bien! Уже неплохо!'
      : 'Попробуй ещё разок!';

    return el('section', { class: 'screen screen--center', style: '--topic-color:' + topic.color }, [
      el('div', { class: 'result' }, [
        el('span', { class: 'result__emoji', text: params.stars >= 2 ? '🎉' : '💪', 'aria-hidden': 'true' }),
        el('h2', { class: 'screen__title', text: praise }),
        starRow(params.stars, 'stars--lg'),
        el('p', { class: 'result__summary', text: params.summary }),
        params.bestStreak > 2
          ? el('p', { class: 'result__streak', text: 'Лучшая серия: ' + params.bestStreak + ' подряд 🔥' })
          : null,
        el('div', { class: 'row' }, [
          el('button', {
            class: 'btn btn--primary', type: 'button',
            onclick: function () { window.Sfx.click(); render(params.mode, { topicId: params.topicId }); }
          }, [el('span', { text: 'Ещё раз' })]),
          el('button', {
            class: 'btn btn--ghost', type: 'button',
            onclick: function () { window.Sfx.click(); render('topic', { topicId: params.topicId }); }
          }, [el('span', { text: 'Другой режим' })])
        ])
      ])
    ]);
  }

  /* ---------- Маршрутизация ---------- */

  var screens = {
    home: screenHome,
    topic: screenTopic,
    cards: screenCards,
    quiz: function (params) { return screenQuestions(params, 'quiz'); },
    listen: function (params) { return screenQuestions(params, 'listen'); },
    memory: screenMemory,
    result: screenResult
  };

  function render(name, params) {
    var build = screens[name] || screens.home;
    root.innerHTML = '';
    root.appendChild(build(params || {}));
    root.scrollTop = 0;
    window.scrollTo(0, 0);
  }

  /* ---------- Переключатели звука ---------- */

  function setupToggles() {
    var musicBtn = document.getElementById('toggle-music');
    var soundBtn = document.getElementById('toggle-sound');

    function paintMusic() {
      var on = window.Progress.get('music');
      musicBtn.setAttribute('aria-pressed', String(on));
      musicBtn.textContent = on ? '🎵' : '🔇';
      musicBtn.title = on ? 'Выключить музыку' : 'Включить музыку';
    }

    function paintSound() {
      var on = window.Progress.get('sound');
      soundBtn.setAttribute('aria-pressed', String(on));
      soundBtn.textContent = on ? '🔔' : '🔕';
      soundBtn.title = on ? 'Выключить звуки' : 'Включить звуки';
    }

    musicBtn.addEventListener('click', function () {
      var on = !window.Progress.get('music');
      window.Progress.setSetting('music', on);
      window.Sfx.setMusic(on);
      paintMusic();
    });

    soundBtn.addEventListener('click', function () {
      var on = !window.Progress.get('sound');
      window.Progress.setSetting('sound', on);
      paintSound();
      if (on) window.Sfx.click();
    });

    paintMusic();
    paintSound();

    /* Музыку можно запустить только после первого клика — таково правило браузеров. */
    if (window.Progress.get('music')) {
      var resume = function () {
        window.Sfx.setMusic(true);
        document.removeEventListener('pointerdown', resume);
      };
      document.addEventListener('pointerdown', resume);
    }
  }

  setupToggles();
  refreshHeader();
  render('home');
})();
