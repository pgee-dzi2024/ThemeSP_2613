from django.shortcuts import render
import asyncio
import threading
import queue
from bleak import BleakClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

ROBOT_MAC_ADDRESS = "36:33:AB:AE:EB:AB"
WRITE_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# Опашка, в която уеб сървърът ще пуска командите
command_queue = queue.Queue()


# Асинхронна функция, която работи постоянно на заден фон
async def ble_worker():
    while True:
        try:
            print("Опит за свързване с робота на заден фон...")
            async with BleakClient(ROBOT_MAC_ADDRESS) as client:
                print("--- РОБОТЪТ Е СВЪРЗАН! Готов за мигновени команди. ---")

                # Докато е свързан, проверяваме опашката много бързо (на всеки 50ms)
                while client.is_connected:
                    try:
                        # Взимаме команда от опашката (без да блокираме)
                        cmd = command_queue.get_nowait()

                        # Изпращаме веднага
                        command_bytes = cmd.encode('utf-8')
                        await client.write_gatt_char(WRITE_UUID, command_bytes)
                        print(f"Изпратено към робота: {cmd}")

                    except queue.Empty:
                        # Ако няма нова команда, изчакваме малко и въртим цикъла
                        await asyncio.sleep(0.05)

        except Exception as e:
            print(f"Bluetooth прекъсна или не е намерен ({e}). Нов опит след 2 секунди...")
            await asyncio.sleep(2)


# Функция за стартиране на фоновата нишка
def start_ble_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ble_worker())


# Стартираме нишката само веднъж при зареждане на файла
ble_thread = threading.Thread(target=start_ble_thread, daemon=True)
ble_thread.start()


class RobotControlView(APIView):
    def post(self, request):
        command = request.data.get('command')
        valid_commands = ['F', 'B', 'L', 'R', 'S', '+', '-']

        if command in valid_commands:
            # Вече НЕ се свързваме тук. Просто слагаме командата в опашката.
            # Това отнема 0.0001 секунди и уеб заявката приключва веднага.
            command_queue.put(command)

            return Response(
                {"status": "success", "message": f"Команда {command} изпратена"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "error", "message": "Грешна команда"},
                status=status.HTTP_400_BAD_REQUEST
            )

def index(request):
    return render(request, 'main/index.html')
