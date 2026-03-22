#include <AFMotor.h>
#include <SoftwareSerial.h>

// Инициализация на 4-те мотора
AF_DCMotor motorFrontLeft(1);
AF_DCMotor motorBackLeft(2);
AF_DCMotor motorFrontRight(3);
AF_DCMotor motorBackRight(4);

// Инициализация на софтуерен сериен порт за BLE модула
// RX пин на Arduino (свързан към TX на BLE) -> A4
// TX пин на Arduino (свързан към RX на BLE) -> A5
SoftwareSerial ble(A4, A5);

// Глобална променлива за скоростта (от 0 до 255)
int robotSpeed = 200; 

void setup() {
  // Стартиране на серийната комуникация за дебъгване (към компютъра)
  Serial.begin(9600);
  Serial.println("Robot is ready!");

  // Стартиране на комуникацията с BLE модула
  // Повечето BLE модули (като HM-10, AT-09) използват 9600 по подразбиране
  ble.begin(9600);
  
  // Първоначално задаване на скорост и спиране на моторите
  setSpeedAll(robotSpeed);
  stopRobot();
}

void loop() {
  // Проверяваме дали има получени данни от BLE модула
  if (ble.available() > 0) {
    char command = ble.read();
    Serial.print("Received command: ");
    Serial.println(command);
    
    executeCommand(command);
  }
}

// Функция за обработка на командите
void executeCommand(char cmd) {
  switch (cmd) {
    case 'F': // Напред
      moveForward();
      break;
    case 'B': // Назад
      moveBackward();
      break;
    case 'L': // Наляво
      turnLeft();
      break;
    case 'R': // Надясно
      turnRight();
      break;
    case 'S': // Стоп
      stopRobot();
      break;
    if (command == '+') {
      robotSpeed += 25; // Увеличаваме скоростта с 25
      if (robotSpeed > 255) robotSpeed = 255; // Ограничаваме до максимума
      Serial.print("Speed Up: ");
      Serial.println(robotSpeed);
    }
    else if (command == '-') {
      robotSpeed -= 25; // Намаляваме скоростта с 25
      if (robotSpeed < 0) robotSpeed = 0; // Ограничаваме до минимума
      Serial.print("Speed Down: ");
      Serial.println(robotSpeed);
    }      
    default:
      // Игнорираме непознати команди
      break;
  }
}

// Функции за движение
void moveForward() {
  motorFrontLeft.run(FORWARD);
  motorBackLeft.run(FORWARD);
  motorFrontRight.run(FORWARD);
  motorBackRight.run(FORWARD);
}

void moveBackward() {
  motorFrontLeft.run(BACKWARD);
  motorBackLeft.run(BACKWARD);
  motorFrontRight.run(BACKWARD);
  motorBackRight.run(BACKWARD);
}

void turnLeft() {
  // За завой наляво - левите мотори назад, десните напред (завъртане на място)
  motorFrontLeft.run(BACKWARD);
  motorBackLeft.run(BACKWARD);
  motorFrontRight.run(FORWARD);
  motorBackRight.run(FORWARD);
}

void turnRight() {
  // За завой надясно - левите мотори напред, десните назад
  motorFrontLeft.run(FORWARD);
  motorBackLeft.run(FORWARD);
  motorFrontRight.run(BACKWARD);
  motorBackRight.run(BACKWARD);
}

void stopRobot() {
  motorFrontLeft.run(RELEASE);
  motorBackLeft.run(RELEASE);
  motorFrontRight.run(RELEASE);
  motorBackRight.run(RELEASE);
}

void setSpeedAll(int speed) {
  motorFrontLeft.setSpeed(speed);
  motorBackLeft.setSpeed(speed);
  motorFrontRight.setSpeed(speed);
  motorBackRight.setSpeed(speed);
}
