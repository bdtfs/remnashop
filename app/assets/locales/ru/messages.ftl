# Used to create a blank line between elements
space = {"\u00A0"}

# Units
unit-bytes = Б
unit-kilobytes = КБ
unit-megabytes = МБ
unit-gigabytes = ГБ
unit-terabytes = ТБ

unit-seconds = { $value ->
    [one] секунда
    [few] секунды
    *[other] секунд
}
unit-minutes = { $value ->
    [one] минута
    [few] минуты
    *[other] минут
}
unit-hours = { $value ->
    [one] час
    [few] часа
    *[other] часов
}
unit-days = { $value ->
    [one] день
    [few] дня
    *[other] дней
}

# Menu
msg-menu-subscription =
    <b>
    💳 Подписка:
    </b>
    { $status ->
    [active]
    <blockquote>
    • Количество устройств: { $devices } / { $max_devices }
    • Заканчивается через: { $expiry_time }
    </blockquote>
    [expired]
    <blockquote>
    • Срок действия истёк.
    • Чтобы продлить нажмите кнопку "💳 Подписка"
    </blockquote>
    *[none]
    <blockquote>
    • У вас нет подписки
    • Чтобы купить нажмите кнопку "💳 Подписка"
    </blockquote>
    }

msg-menu-profile =
    <b>
    👤 Профиль:
    </b>
    <blockquote>
    • ID: { $id }
    • Имя: { $name }
    • Баланс: { $balance }
    </blockquote>


# Dashboard
msg-dashboard = <b>🛠 Панель управления:</b>
msg-dashboard-statistics = <b>📊 Статистика:</b>

msg-dashboard-users = <b>👥 Пользователи:</b>
msg-dashboard-banlist = <b>🚫 Черный список:</b>
msg-dashboard-broadcast = <b>📢 Рассылка:</b>
msg-dashboard-promocodes = <b>🎟 Промокоды:</b>

msg-dashboard-maintenance =
    <b>
    🚧 Режим обслуживания:
    </b>
    <blockquote>
    { $status ->
    [global] 🔴 Включен (глобальный)
    [purchase] 🟠 Включен (платежи)
    *[off] ⚪ Выключен
    }
    </blockquote>

msg-remnawave =
    <b>
    🌊 RemnaWave:
    </b>
    
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
    <b>
    👥 Пользователи:
    </b>

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
    • Адрес: { $address }:{ $port }
    • Инбаунд: { $inbound_uuid }
    </blockquote>

msg-remnawave-hosts =
    <b>
    🌐 Хосты:
    </b>
    
    { $hosts }

msg-remnawave-node-details =
    { $country } { $name } ({ $status ->
    [on] подключено
    *[off] отключено
    }):
    <blockquote>
    • Адрес: { $address }:{ $port }
    • Аптайм (xray): { $xray_uptime }
    • Пользователей онлайн: { $users_online }
    • Трафик: { $traffic_used } / {$traffic_limit}
    </blockquote>

msg-remnawave-nodes =
    <b>
    🖥️ Ноды:
    </b>

    { $nodes }

msg-remnawave-inbound-details =
    🔗 { $tag }
    <blockquote>
    • UUID: { $uuid }
    • Протокол: { $type } ({ $network })
    • Порт: { $port }
    • Безопасность: { $security } 
    </blockquote>

msg-remnawave-inbounds =
    <b>
    🔌 Инбаунды:
    </b>

    { $inbounds }


msg-remnashop = <b>🛍 RemnaShop:</b>

