# Git Commit Convention

> Стандарт оформления коммитов проекта **Campfire**.

---

## 🏕️ Веховые коммиты (Milestones)

Campfire развивается поэтапно, после завершения крупного логического этапа рекомендуется создавать **веховый коммит**.

Такие коммиты помогают быстро ориентироваться в истории проекта и позволяют в любой момент вернуться к важной стадии разработки.

---

### Когда создавать

Веховый коммит создаётся после завершения значимого этапа, например:

* завершён фундамент проекта;
* реализована новая крупная система;
* полностью закончена часть интерфейса;
* достигнута первая рабочая версия функциональности;
* завершён очередной этап Roadmap.

Веховый коммит должен фиксировать **полностью рабочее состояние проекта**.

---

### Формат

```text
🏕️ milestone: <название этапа>
```

---

### Примеры

```text
🏕️ milestone: project foundation completed

🏕️ milestone: first application launch

🏕️ milestone: theme system completed

🏕️ milestone: character ui completed

🏕️ milestone: inventory system completed

🏕️ milestone: first playable build

🏕️ milestone: local network prototype

🏕️ milestone: save system completed

🏕️ milestone: mvp completed
```

---

### Правила

✔ Веховый коммит всегда создаётся после обычных коммитов разработки.

✔ Он не должен содержать незавершённый код.

✔ Его задача - отметить стабильную точку развития проекта.

✔ Веховые коммиты должны быть редкими так как это ориентиры, а не ежедневные коммиты.

---

# Формат

```text
<emoji> <type>: краткое описание

Что сделано:
- ...

Почему:
- ...

Дополнительно:
- ...
```

Описание должно быть коротким и отвечать на вопрос **"Что изменилось?"**.

Текст пишется в настоящем времени.

Хорошо:

```text
✨ feat: add inventory panel
```

Плохо:

```text
Обновил какую-то штуку
```

---

# Типы коммитов

## ✨ feature

Новая функциональность.

Примеры:

```text
✨ feature: add inventory system
✨ feature: implement character editor
✨ feature: create dice panel
```

---

## 🐞 fix

Исправление ошибки.

Примеры:

```text
🐞 fix: inventory scrolling
🐞 fix: hp calculation
🐞 fix: crash on startup
```

---

## ♻️ refactor

Изменение архитектуры без изменения поведения.

Примеры:

```text
♻️ refactor: split SceneManager
♻️ refactor: simplify event dispatch
```

---

## 🎨 style

Изменения интерфейса.

Примеры:

```text
🎨 style: update sidebar spacing
🎨 style: redesign inventory cards
```

---

## 📝 docs

Документация.

Примеры:

```text
📝 docs: update README
📝 docs: add architecture guide
```

---

## ⚡ perf

Оптимизация.

Примеры:

```text
⚡ perf: optimize repaint
⚡ perf: improve save serialization
```

---

## 🧪 test

Добавление или обновление тестов.

Примеры:

```text
🧪 test: add save manager tests
🧪 test: cover event system
```

---

## 🔧 chore

Технические изменения.

Примеры:

```text
🔧 chore: update dependencies
🔧 chore: configure Ruff
🔧 chore: update .gitignore
```

---

## 🔥 remove

Удаление кода.

Примеры:

```text
🔥 remove: delete legacy widgets
🔥 remove: unused assets
```

---

## 🚧 wip

Незавершённая работа.

Используется только в личных ветках.

В ветку `main` такие коммиты не попадают.

---

# Шаблон полного коммита

```text
✨ feat: implement theme system

Что сделано:
- добавлен пакет theme
- создан Colors
- создан Spacing
- создан Typography

Почему:
- централизованное управление стилями

Дополнительно:
- подготовлена база для дизайн-системы
```

---

# Примеры хороших коммитов

```text
✨ feat: create character panel
```

```text
🎨 style: redesign left sidebar
```

```text
♻️ refactor: extract inventory widget
```

```text
🐞 fix: hp value synchronization
```

```text
📝 docs: add CONTRIBUTING guide
```

```text
⚡ perf: cache icon loading
```

---

# Правила

✔ Один коммит = одна логическая задача.

✔ Коммит должен быть понятен без просмотра кода.

✔ Не смешивать исправления, рефакторинг и новую функциональность в одном коммите.

✔ Перед большим рефакторингом желательно сделать отдельный коммит с текущим рабочим состоянием.

✔ История Git должна рассказывать историю развития проекта.
