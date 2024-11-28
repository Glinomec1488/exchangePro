# Импорты
from aiogram.filters.callback_data import (
    CallbackData,
)  # Импорт класса CallbackData для создания объектов callback data
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
)  # Импорт InlineKeyboardBuilder для создания клавиатур
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # Импорт AsyncSession для работы с базой данных

from database.function.user_commands import (
    select_allusers,
    update_status,
)  # Импорт функций работы с базой данных

from filters import (
    PrivateChatFilter,
)  # Импорт пользовательского фильтра PrivateChatFilter

from aiogram import Router, F  # Импорт основных модулей и классов из aiogram
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)  # Импорт CallbackQuery, InlineKeyboardMarkup и InlineKeyboardButton

router = Router(name="bans")  # Создание роутера с именем 'bans'


# Определение callback data для кнопки бана пользователя
class Userban(CallbackData, prefix="ban"):
    users_id: int  # Поле для идентификатора пользователя


# Определение callback data для навигации по страницам
class Pagination(CallbackData, prefix="pag"):
    action: str  # Действие
    page: int  # Номер страницы


# Функция для создания клавиатуры с пользователями и кнопками для перелистывания
async def paginator(session: AsyncSession, page: int = 0):
    users = await select_allusers(session=session)  # Получение списка пользователей
    builder = InlineKeyboardBuilder()  # Создание объекта InlineKeyboardBuilder
    start_offset = page * 3  # Вычисление начального смещения на основе номера страницы
    limit = 3  # Определение лимита пользователей на одной странице
    end_offset = start_offset + limit  # Вычисление конечного смещения
    for user in users[
        start_offset:end_offset
    ]:  # Перебор пользователей для текущей страницы
        builder.row(
            InlineKeyboardButton(
                text=f"👤 {user.user_id}",
                callback_data=Userban(users_id=user.user_id).pack(),
            )
        )  # Добавление кнопки для каждого пользователя
    buttons_row = []  # Создание списка кнопок
    if page > 0:  # Проверка, что страница не первая
        buttons_row.append(
            InlineKeyboardButton(
                text="⬅️", callback_data=Pagination(action="prev", page=page - 1).pack()
            )
        )  # Добавление кнопки "назад"
    if end_offset < len(
        users
    ):  # Проверка, что ещё есть пользователи для следующей страницы
        buttons_row.append(
            InlineKeyboardButton(
                text="➡️", callback_data=Pagination(action="next", page=page + 1).pack()
            )
        )  # Добавление кнопки "вперед"
    else:  # Если пользователи закончились
        buttons_row.append(
            InlineKeyboardButton(
                text="➡️", callback_data=Pagination(action="next", page=0).pack()
            )
        )  # Возвращение на первую страницу
    builder.row(*buttons_row)  # Добавление кнопок навигации
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")
    )  # Добавление кнопки "назад"
    return builder.as_markup()  # Возвращение клавиатуры в виде разметки


# Обработчик нажатия на кнопку "бан" для пользователя
@router.callback_query(F.data.startswith("bans"), PrivateChatFilter())
async def add_ban(call: CallbackQuery, session: AsyncSession):
    await call.answer()  # Отправка ответа на запрос
    await call.message.edit_reply_markup(
        reply_markup=await paginator(session=session, page=0)
    )  # Отображение клавиатуры с пользователями и кнопками для перелистывания


# Обработчик нажатия кнопок навигации
@router.callback_query(Pagination.filter(), PrivateChatFilter())
async def pagination_handler(
    call: CallbackQuery, callback_data: Pagination, session: AsyncSession
):
    page = callback_data.page  # Получение номера страницы из callback data
    await call.message.edit_reply_markup(
        reply_markup=await paginator(session=session, page=page)
    )  # Обновление клавиатуры при нажатии кнопок "вперед" или "назад"


# Обработчик нажатия кнопок бана для конкретного пользователя
@router.callback_query(Userban.filter(), PrivateChatFilter())
async def get_ban(call: CallbackQuery, callback_data: Userban, session: AsyncSession):
    await update_status(
        user_id=callback_data.users_id, session=session, status="banned", commit=True
    )  # Обновление статуса пользователя на "забанен" в базе данных
    kb_back = InlineKeyboardBuilder()  # Создание клавиатуры
    kb_back.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")
    )  # Добавление кнопки "назад"
    await call.message.edit_text(
        "✅ Вы успешно забанили пользователя", reply_markup=kb_back.as_markup()
    )  # Отправка сообщения об успешном бане пользователя
