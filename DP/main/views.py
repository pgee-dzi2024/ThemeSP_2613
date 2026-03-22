from django.shortcuts import render
import asyncio
from bleak import BleakClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Дефинираме константите за нашия Bluetooth модул
ROBOT_MAC_ADDRESS = "36:33:AB:AE:EB:AB"
WRITE_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"


# Асинхронна функция за свързване и изпращане на командата
async def send_ble_command(cmd_string):
    # Създаваме връзка с модула
    async with BleakClient(ROBOT_MAC_ADDRESS) as client:
        # Проверяваме дали сме свързани
        if client.is_connected:
            # bleak очаква данни в байтове, затова енкодваме стринга (напр. 'F' -> b'F')
            command_bytes = cmd_string.encode('utf-8')
            # Изпращаме командата към характеристиката
            await client.write_gatt_char(WRITE_UUID, command_bytes)
            print(f"Успешно изпратена команда: {cmd_string}")
        else:
            raise Exception("Неуспешно свързване с Bluetooth модула.")


class RobotControlView(APIView):
    def post(self, request):
        # Взимаме командата от POST заявката
        command = request.data.get('command')
        valid_commands = ['F', 'B', 'L', 'R', 'S']

        if command in valid_commands:
            try:
                # Изпълняваме асинхронната Bluetooth функция в синхронния Django изглед
                asyncio.run(send_ble_command(command))

                return Response(
                    {"status": "success", "message": f"Command {command} executed"},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                # Ако роботът е изключен или извън обхват, връщаме грешка
                print(f"Грешка при Bluetooth комуникация: {e}")
                return Response(
                    {"status": "error", "message": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {"status": "error", "message": "Invalid command"},
                status=status.HTTP_400_BAD_REQUEST
            )
def index(request):
    return render(request, 'main/index.html')
