import asyncio
from bleak import BleakScanner


async def scan_for_devices():
    print("Стартиране на сканирането за Bluetooth устройства...")
    print("Моля, изчакайте (отнема около 5-10 секунди)...\n")

    # Търсим всички налични BLE устройства в обсег
    devices = await BleakScanner.discover()

    if not devices:
        print("Не са открити Bluetooth устройства наблизо.")
        return

    print("--- Намерени устройства ---")
    for device in devices:
        # Често устройствата нямат зададено име, затова слагаме fallback
        device_name = device.name if device.name else "Неизвестно устройство (Unknown)"
        print(f"Име: {device_name}")
        print(f"MAC Адрес: {device.address}")
        # RSSI показва силата на сигнала (колкото по-близо до 0, толкова по-силен е сигналът)
        # print(f"Сила на сигнала (RSSI): {device.rssi} dBm")
        # print("-" * 30)


if __name__ == "__main__":
    # Стартираме асинхронната функция
    asyncio.run(scan_for_devices())