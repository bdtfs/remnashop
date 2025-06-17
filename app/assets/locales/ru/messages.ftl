msg-plan-detail =
    <blockquote>
    { $type ->
    [devices]
    • Количество устройств: { $current_devices } / { $max_devices }
    • Заканчивается через: { $expiry_time }
    *[traffic]
    • Трафик: { $current_traffic } / { $max_traffic }
    • Заканчивается через: { $expiry_time }
    }
    </blockquote>

# Menu
msg-menu-subscription =
    <b>💳 Подписка:</b>
    { $status ->
    [active]
    { $plan }
    [expired]
    <blockquote>
    • Срок действия истёк.
    • Чтобы продлить перейдите в меню "💳 Подписка"
    </blockquote>
    *[none]
    <blockquote>
    • У вас нет подписки

    Для оформления перейдите в меню "💳 Подписка"
    </blockquote>
    }

msg-menu-profile =
    <b>👤 Профиль:</b>
    <blockquote>
    • ID: <code>{ $id }</code>
    • Имя: { $name }
    </blockquote>


# Dashboard
msg-dashboard = <b>🛠 Панель управления:</b>
msg-dashboard-statistics = <b>📊 Статистика:</b>
msg-dashboard-users = <b>👥 Пользователи:</b>
msg-dashboard-broadcast = <b>📢 Рассылка:</b>
msg-dashboard-promocodes = <b>🎟 Промокоды:</b>

msg-dashboard-maintenance =
    <b>🚧 Режим обслуживания:</b>
    
    Статус: { $status ->
    [global] 🔴 Включен (глобальный)
    [purchase] 🟠 Включен (платежи)
    *[off] ⚪ Выключен
    }

# Users
msg-users-search =
    <b>🔍 Поиск пользователя:</b>

    Введите ID пользователя или перешлите любое его сообщение

msg-users-user = 
    <b>📝 Информация о пользователе:</b>

    👤 Профиль:
    <blockquote>
    • ID: <code>{ $id }</code>
    • Имя: { $name }
    • Роль: { role }
    </blockquote>

    💳 Подписка:
    { $has_subscription ->
    [True]
    { $plan }
    *[False]
    <blockquote>
    • Нет оформленной подписки
    </blockquote>
    }

msg-users-user-role = <b>👮‍♂️ Изменить роль:</b>

msg-users-blacklist =
    <b>🚫 Черный список:</b>

    Заблокировано: { $count_blocked } / { $count_users } ({ $percent }%)

msg-users-unblock-all =
    <b>🚫 Черный список:</b>

    Вы уверены, что хотите разблокировать всех пользователей?


# RemnaWave
msg-remnawave =
    <b>🌊 RemnaWave:</b>
    
    🖥️ Система:
    <blockquote>
    • ЦПУ: { $cpu_cores } { $cpu_cores ->
        [one] ядро
        [few] ядра
        *[other] ядер
    } { $cpu_threads } { $cpu_threads ->
        [one] поток
        [few] потока
        *[other] потоков
    }
    • ОЗУ: { $ram_used } / { $ram_total } ({ $ram_used_percent }%)
    • Аптайм: { $uptime }
    </blockquote>

msg-remnawave-users =
    <b>👥 Пользователи:</b>

    📊 Статистика:
    <blockquote>
    • Всего: { $users_total }
    • Активные: { $users_active }
    • Отключённые: { $users_disabled }
    • Ограниченные: { $users_limited }
    • Истёкшие: { $users_expired }
    </blockquote>

    🟢 Онлайн:
    <blockquote>
    • За день: { $online_last_day }
    • За неделю: { $online_last_week }
    • Никогда не заходили: { $online_never }
    • Сейчас онлайн: { $online_now }
    </blockquote>

msg-remnawave-host-details =
    { $remark } ({ $status ->
    [on] включен
    *[off] выключен
    }):
    <blockquote>
    • Адрес: <code>{ $address }:{ $port }</code>
    • Инбаунд: <code>{ $inbound_uuid }</code>
    </blockquote>

msg-remnawave-hosts =
    <b>🌐 Хосты:</b>
    
    { $hosts }

msg-remnawave-node-details =
    { $country } { $name } ({ $status ->
    [on] подключено
    *[off] отключено
    }):
    <blockquote>
    • Адрес: <code>{ $address }:{ $port }</code>
    • Аптайм (xray): { $xray_uptime }
    • Пользователей онлайн: { $users_online }
    • Трафик: { $traffic_used } / {$traffic_limit}
    </blockquote>

msg-remnawave-nodes =
    <b>🖥️ Ноды:</b>

    { $nodes }

msg-remnawave-inbound-details =
    🔗 { $tag }
    <blockquote>
    • UUID: <code>{ $uuid }</code>
    • Протокол: { $type } ({ $network })
    • Порт: { $port }
    • Безопасность: { $security } 
    </blockquote>

msg-remnawave-inbounds =
    <b>🔌 Инбаунды:</b>

    { $inbounds }


# RemnaShop
msg-remnashop = <b>🛍 RemnaShop:</b>
msg-remnashop-admins = <b>👮‍♂️ Администраторы:</b>