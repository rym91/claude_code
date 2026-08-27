/* Словарь приложения: темы и слова.
   У каждого слова: es — испанское написание, ru — перевод, emoji — картинка. */
window.TOPICS = [
  {
    id: 'saludos',
    title: 'Приветствия',
    titleEs: 'Saludos',
    emoji: '👋',
    color: '#ff8fab',
    words: [
      { es: 'hola',          ru: 'привет',           emoji: '👋' },
      { es: 'adiós',         ru: 'пока',             emoji: '🙋' },
      { es: 'buenos días',   ru: 'доброе утро',      emoji: '🌅' },
      { es: 'buenas noches', ru: 'спокойной ночи',   emoji: '🌙' },
      { es: 'gracias',       ru: 'спасибо',          emoji: '🙏' },
      { es: 'por favor',     ru: 'пожалуйста',       emoji: '🥺' },
      { es: 'sí',            ru: 'да',               emoji: '✅' },
      { es: 'no',            ru: 'нет',              emoji: '❌' },
      { es: '¿cómo estás?',  ru: 'как дела?',        emoji: '😊' },
      { es: 'mucho gusto',   ru: 'очень приятно',    emoji: '🤝' },
      { es: 'lo siento',     ru: 'извини',           emoji: '😔' },
      { es: 'me llamo',      ru: 'меня зовут',       emoji: '🏷️' }
    ]
  },
  {
    id: 'animales',
    title: 'Животные',
    titleEs: 'Animales',
    emoji: '🐶',
    color: '#7bd389',
    words: [
      { es: 'el perro',   ru: 'собака',   emoji: '🐶' },
      { es: 'el gato',    ru: 'кот',      emoji: '🐱' },
      { es: 'el pájaro',  ru: 'птица',    emoji: '🐦' },
      { es: 'el pez',     ru: 'рыба',     emoji: '🐟' },
      { es: 'el caballo', ru: 'лошадь',   emoji: '🐴' },
      { es: 'la vaca',    ru: 'корова',   emoji: '🐮' },
      { es: 'el cerdo',   ru: 'свинья',   emoji: '🐷' },
      { es: 'el conejo',  ru: 'кролик',   emoji: '🐰' },
      { es: 'el oso',     ru: 'медведь',  emoji: '🐻' },
      { es: 'el león',    ru: 'лев',      emoji: '🦁' },
      { es: 'la rana',    ru: 'лягушка',  emoji: '🐸' },
      { es: 'la abeja',   ru: 'пчела',    emoji: '🐝' }
    ]
  },
  {
    id: 'colores',
    title: 'Цвета',
    titleEs: 'Colores',
    emoji: '🎨',
    color: '#ffc65c',
    words: [
      { es: 'rojo',     ru: 'красный',     emoji: '🔴' },
      { es: 'azul',     ru: 'синий',       emoji: '🔵' },
      { es: 'verde',    ru: 'зелёный',     emoji: '🟢' },
      { es: 'amarillo', ru: 'жёлтый',      emoji: '🟡' },
      { es: 'negro',    ru: 'чёрный',      emoji: '⚫' },
      { es: 'blanco',   ru: 'белый',       emoji: '⚪' },
      { es: 'naranja',  ru: 'оранжевый',   emoji: '🟠' },
      { es: 'morado',   ru: 'фиолетовый',  emoji: '🟣' },
      { es: 'rosa',     ru: 'розовый',     emoji: '🌸' },
      { es: 'marrón',   ru: 'коричневый',  emoji: '🟤' }
    ]
  },
  {
    id: 'numeros',
    title: 'Числа',
    titleEs: 'Números',
    emoji: '🔢',
    color: '#6ec6ff',
    words: [
      { es: 'uno',    ru: 'один',    emoji: '1️⃣' },
      { es: 'dos',    ru: 'два',     emoji: '2️⃣' },
      { es: 'tres',   ru: 'три',     emoji: '3️⃣' },
      { es: 'cuatro', ru: 'четыре',  emoji: '4️⃣' },
      { es: 'cinco',  ru: 'пять',    emoji: '5️⃣' },
      { es: 'seis',   ru: 'шесть',   emoji: '6️⃣' },
      { es: 'siete',  ru: 'семь',    emoji: '7️⃣' },
      { es: 'ocho',   ru: 'восемь',  emoji: '8️⃣' },
      { es: 'nueve',  ru: 'девять',  emoji: '9️⃣' },
      { es: 'diez',   ru: 'десять',  emoji: '🔟' }
    ]
  },
  {
    id: 'comida',
    title: 'Еда',
    titleEs: 'Comida',
    emoji: '🍎',
    color: '#ff9f68',
    words: [
      { es: 'la manzana', ru: 'яблоко',     emoji: '🍎' },
      { es: 'el plátano', ru: 'банан',      emoji: '🍌' },
      { es: 'el pan',     ru: 'хлеб',       emoji: '🍞' },
      { es: 'la leche',   ru: 'молоко',     emoji: '🥛' },
      { es: 'el queso',   ru: 'сыр',        emoji: '🧀' },
      { es: 'el huevo',   ru: 'яйцо',       emoji: '🥚' },
      { es: 'la naranja', ru: 'апельсин',   emoji: '🍊' },
      { es: 'el agua',    ru: 'вода',       emoji: '💧' },
      { es: 'la sopa',    ru: 'суп',        emoji: '🍲' },
      { es: 'el helado',  ru: 'мороженое',  emoji: '🍦' },
      { es: 'la fresa',   ru: 'клубника',   emoji: '🍓' },
      { es: 'el pastel',  ru: 'торт',       emoji: '🍰' }
    ]
  },
  {
    id: 'familia',
    title: 'Семья',
    titleEs: 'Familia',
    emoji: '👨‍👩‍👧',
    color: '#c79bff',
    words: [
      { es: 'la madre',   ru: 'мама',      emoji: '👩' },
      { es: 'el padre',   ru: 'папа',      emoji: '👨' },
      { es: 'el hermano', ru: 'брат',      emoji: '👦' },
      { es: 'la hermana', ru: 'сестра',    emoji: '👧' },
      { es: 'el abuelo',  ru: 'дедушка',   emoji: '👴' },
      { es: 'la abuela',  ru: 'бабушка',   emoji: '👵' },
      { es: 'el bebé',    ru: 'малыш',     emoji: '👶' },
      { es: 'el tío',     ru: 'дядя',      emoji: '🧔' },
      { es: 'la tía',     ru: 'тётя',      emoji: '👩‍🦱' },
      { es: 'la familia', ru: 'семья',     emoji: '👨‍👩‍👧‍👦' }
    ]
  },
  {
    id: 'cuerpo',
    title: 'Тело',
    titleEs: 'Cuerpo',
    emoji: '🖐️',
    color: '#5ddad1',
    words: [
      { es: 'la mano',     ru: 'рука',     emoji: '🖐️' },
      { es: 'el pie',      ru: 'нога',     emoji: '🦶' },
      { es: 'la cabeza',   ru: 'голова',   emoji: '👤' },
      { es: 'el ojo',      ru: 'глаз',     emoji: '👁️' },
      { es: 'la nariz',    ru: 'нос',      emoji: '👃' },
      { es: 'la boca',     ru: 'рот',      emoji: '👄' },
      { es: 'la oreja',    ru: 'ухо',      emoji: '👂' },
      { es: 'el pelo',     ru: 'волосы',   emoji: '💇' },
      { es: 'el diente',   ru: 'зуб',      emoji: '🦷' },
      { es: 'el corazón',  ru: 'сердце',   emoji: '❤️' }
    ]
  },
  {
    id: 'ropa',
    title: 'Одежда',
    titleEs: 'Ropa',
    emoji: '👕',
    color: '#ffb3c6',
    words: [
      { es: 'la camiseta',    ru: 'футболка',   emoji: '👕' },
      { es: 'el pantalón',    ru: 'брюки',      emoji: '👖' },
      { es: 'el vestido',     ru: 'платье',     emoji: '👗' },
      { es: 'los zapatos',    ru: 'ботинки',    emoji: '👟' },
      { es: 'el sombrero',    ru: 'шляпа',      emoji: '👒' },
      { es: 'la chaqueta',    ru: 'куртка',     emoji: '🧥' },
      { es: 'los calcetines', ru: 'носки',      emoji: '🧦' },
      { es: 'la bufanda',     ru: 'шарф',       emoji: '🧣' },
      { es: 'los guantes',    ru: 'перчатки',   emoji: '🧤' },
      { es: 'la blusa',       ru: 'блузка',     emoji: '👚' }
    ]
  },
  {
    id: 'transporte',
    title: 'Транспорт',
    titleEs: 'Transporte',
    emoji: '🚗',
    color: '#8ec5ff',
    words: [
      { es: 'el coche',       ru: 'машина',     emoji: '🚗' },
      { es: 'el autobús',     ru: 'автобус',    emoji: '🚌' },
      { es: 'el tren',        ru: 'поезд',      emoji: '🚆' },
      { es: 'el avión',       ru: 'самолёт',    emoji: '✈️' },
      { es: 'la bicicleta',   ru: 'велосипед',  emoji: '🚲' },
      { es: 'el barco',       ru: 'корабль',    emoji: '🚢' },
      { es: 'la moto',        ru: 'мотоцикл',   emoji: '🏍️' },
      { es: 'el camión',      ru: 'грузовик',   emoji: '🚚' },
      { es: 'el helicóptero', ru: 'вертолёт',   emoji: '🚁' },
      { es: 'el cohete',      ru: 'ракета',     emoji: '🚀' }
    ]
  }
];

/* Плоский список всех слов — для режима «Всё вперемешку». */
window.ALL_WORDS = window.TOPICS.reduce(function (acc, topic) {
  topic.words.forEach(function (word) {
    acc.push(Object.assign({ topicId: topic.id }, word));
  });
  return acc;
}, []);
