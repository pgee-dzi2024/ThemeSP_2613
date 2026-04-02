import asyncio
from bleak import BleakClient

# Тук слагаме намерения MAC адрес
MAC_ADDRESS = "36:33:AB:AE:EB:AB"


async def explore_device(address):
    print(f"Опит за свързване към робота ({address})...")
    try:
        # Свързваме се с устройството
        async with BleakClient(address) as client:
            print(f"Успешно свързване! Състояние: {client.is_connected}")

            print("\nНалични канали (UUIDs):")
            for service in client.services:
                print(f"\n[Услуга] {service.uuid}")
                for char in service.characteristics:
                    print(f"  ├── [Характеристика] {char.uuid}")
                    print(f"  └── Свойства: {', '.join(char.properties)}")

                    # Проверяваме дали това е канал за изпращане на данни
                    if "write" in char.properties or "write-without-response" in char.properties:
                        print("      ^-- ВЪЗМОЖЕН КАНАЛ ЗА ИЗПРАЩАНЕ НА КОМАНДИ!")

    except Exception as e:
        print(f"Грешка при свързване: {e}")


if __name__ == "__main__":
    asyncio.run(explore_device(MAC_ADDRESS))