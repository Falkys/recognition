def main():
    # код который будет выполнятся
    return "Привет 😊" # ответ который будет выводится в консоль

names = ["Привет", "Здраствуй"] # тут комманды на которые будет отзыватся бот
sounds = ["./hello.wav"] # тут звуки которые будут производится при успешном выполнении кода
type = "" # default = "onCalling", "always", "onEvent"
event = "" # default = none, its required on type = "onEvent"
interval = "" # default = "1000", interval in ms between executions