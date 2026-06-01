import allure
from playwright.sync_api import expect

from config.base import URL_BASE


class BasePage:

    def __init__(self, page_):
        self.page = page_
        # self.page.set_default_timeout(3_000)

    @allure.step("Отрываем страницу {url}")
    def open(self, url=URL_BASE):
        self.page.goto(url)

    @allure.step("проверяем, что открыта страница по url: {url_sub}")
    def expect_to_have_url(self, url_sub: str):
        expect(self.page).to_have_url(URL_BASE + url_sub)

    def create_click_delete_hidden(self, element_id: str = "test-element"):
        """
        1. Создаёт невидимый элемент
        2. Кликает по нему (через JS, т.к. Playwright не кликает по hidden)
        3. Удаляет элемент
        """
        page = self.page

        # 1️⃣ Создаём невидимый элемент через JS
        page.evaluate(f"""
            () => {{
                // Проверяем, нет ли уже такого элемента
                if (document.getElementById('{element_id}')) return;

                const el = document.createElement('div');
                el.id = '{element_id}';

                // Делаем невидимым, но оставляем в DOM
                el.style.cssText = `
                    position: fixed;
                    top: 0px;
                    left: 0px;
                    opacity: 0;
                    pointer-events: auto;  /* Важно: разрешаем клики! */
                    width: 1px;
                    height: 1px;
                `;

                // Добавляем обработчик клика для проверки
                el.addEventListener('click', (e) => {{
                    el.dataset.clicked = 'true';
                }});

                document.body.appendChild(el);
            }}
        """)

        # 2️⃣ Кликаем по элементу
        # Вариант А: через Playwright с force=True (обходит проверку видимости)
        hidden_el = page.locator(f"#{element_id}")
        hidden_el.click(force=True)  # ⚠️ force=True игнорирует visibility-проверки

        # Вариант Б: через чистый JS (если force=True не сработал)
        # page.evaluate(f"document.getElementById('{element_id}').click()")

        # 3️⃣ Проверяем, что клик сработал (опционально)
        was_clicked = page.evaluate(
            f"document.getElementById('{element_id}')?.dataset.clicked")
        assert was_clicked == "true", "Клик не был обработан!"

        # 4️⃣ Удаляем элемент
        page.evaluate(f"""
            () => {{
                const el = document.getElementById('{element_id}');
                if (el) el.remove();
            }}
        """)

        # 5️⃣ Проверяем удаление
        assert hidden_el.count() == 0, "Элемент не был удалён!"

        print(f"✅ Элемент #{element_id}: создан → кликнут → удалён")


    def get_mouse_pos(self):
        self.page.evaluate("""() => {
               window._mousePos = { x: 0, y: 0 };
               document.addEventListener('mousemove', (e) => {
                   window._mousePos = { x: e.clientX, y: e.clientY };
               });
        #    }""")
        self.page.mouse.move(10, 10)
        x, y = self.page.evaluate("() => window._mousePos")
        print(x, y)

    def swipe_screen(self):
        """
        Warning: есть опасения, что mouse.down может нажать на кнопку
        :return:
        """
        height = self.page.viewport_size["height"]
        print(f"{height=}")
        # self.get_mouse_pos()
        self.page.mouse.down()
        self.page.mouse.move(100, height, steps=30)
        self.page.mouse.up()
        self.create_click_delete_hidden()

    def swipe(self, element_selector,
              start_x, start_y, end_x, end_y,
              duration_ms=300):
        """
        Эмулирует swipe-жест на элементе

        :param element_selector: CSS-селектор элемента
        :param start_x, start_y: начальные координаты (относительно viewport)
        :param end_x, end_y: конечные координаты
        :param duration_ms: длительность жеста в миллисекундах
        """
        self.page.evaluate("""
            (params) => {
                const { selector, startX, startY, endX, endY, duration } = params;
                const el = document.querySelector(selector);

                if (!el) {
                    throw new Error(`Element not found: ${selector}`);
                }

                // Вспомогательная функция для создания Touch-объекта
                const createTouch = (x, y, identifier = 1) => {
                    return new Touch({
                        identifier,
                        target: el,
                        clientX: x,
                        clientY: y,
                        radiusX: 20,
                        radiusY: 20,
                        rotationAngle: 0,
                        force: 1
                    });
                };

                // 1️⃣ touchstart
                const startTouch = createTouch(startX, startY);
                const startEvent = new TouchEvent('touchstart', {
                    touches: [startTouch],
                    targetTouches: [startTouch],
                    changedTouches: [startTouch],
                    bubbles: true,
                    cancelable: true
                });
                el.dispatchEvent(startEvent);

                // 2️⃣ touchmove (можно несколько для плавности)
                const midTouch = createTouch(
                    startX + (endX - startX) * 0.5,
                    startY + (endY - startY) * 0.5
                );
                const moveEvent = new TouchEvent('touchmove', {
                    touches: [midTouch],
                    targetTouches: [midTouch],
                    changedTouches: [midTouch],
                    bubbles: true,
                    cancelable: true
                });
                el.dispatchEvent(moveEvent);

                // Небольшая задержка для эмуляции "живого" жеста
                // (в реальном браузере это происходит естественно)

                // 3️⃣ touchend
                const endTouch = createTouch(endX, endY);
                const endEvent = new TouchEvent('touchend', {
                    touches: [],  // Палец убран — массив пустой!
                    targetTouches: [],
                    changedTouches: [endTouch],  // Но последнее положение — в changedTouches
                    bubbles: true,
                    cancelable: true
                });
                el.dispatchEvent(endEvent);
            }
        """, {
            "selector": element_selector,
            "startX": start_x,
            "startY": start_y,
            "endX": end_x,
            "endY": end_y,
            "duration": duration_ms
        })

    # 🔽 Свайп вниз (например, для обновления страницы)
    def swipe_down(self, selector, duration_ms=400):
        self.swipe(selector,
                   start_x=100, start_y=50, end_x=100, end_y=700,
                   duration_ms=duration_ms)

    # 🔼 Свайп вверх (скролл контента)
    def swipe_up(self, selector, duration_ms=400):
        self.swipe(selector,
                   start_x=200, start_y=500, end_x=200, end_y=100,
                   duration_ms=duration_ms)

    # ➡️ Свайп вправо (слайдер, меню)
    def swipe_right(self, selector, distance_px=150, duration_ms=300):
        self.swipe(selector,
                   start_x=100, start_y=200, end_x=100+distance_px, end_y=200,
                   duration_ms=duration_ms)

    # ⬅️ Свайп влево (закрытие, удаление)
    def swipe_left(self, selector, distance_px=150, duration_ms=300):
        self.swipe(selector,
                   start_x=250, start_y=200, end_x=250-distance_px, end_y=200,
                   duration_ms=duration_ms)


    def get_element_center(self, selector):
        """Возвращает центр элемента в координатах viewport"""
        coords = self.page.evaluate("""
            (selector) => {
                const el = document.querySelector(selector);
                if (!el) return null;
                const rect = el.getBoundingClientRect();
                return {
                    x: rect.left + rect.width / 2,
                    y: rect.top + rect.height / 2,
                    width: rect.width,
                    height: rect.height
                };
            }
        """, selector)
        return coords

    def swipe_element(self, selector, direction="left", distance_ratio=0.7,
                      duration_ms=300):
        """
        Свайп по элементу с динамическим расчётом координат

        :param direction: "left", "right", "up", "down"
        :param distance_ratio: доля от размера элемента (0.3 = 30%, 1.0 = 100%)
        """
        coords = self.get_element_center(selector)
        if not coords:
            raise ValueError(f"Element {selector} not found")

        # Определяем смещение в зависимости от направления
        offsets = {
            "left": (-coords["width"] * distance_ratio, 0),
            "right": (coords["width"] * distance_ratio, 0),
            "up": (0, -coords["height"] * distance_ratio),
            "down": (0, coords["height"] * distance_ratio)
        }

        dx, dy = offsets.get(direction, (0, 0))

        self.swipe(
            selector,
            start_x=coords["x"],
            start_y=coords["y"],
            end_x=coords["x"] + dx,
            end_y=coords["y"] + dy,
            duration_ms=duration_ms
        )
