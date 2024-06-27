import webbrowser

def main(patterns): # если name = ['Открой { word: [браузер, гугл]}'] и вы сказали `открой гугл`, то он выведет { word: "гугл"}
    if patterns["word"] == "браузер":
        webbrowser.open("https://") # откроет новую вкладку
    elif patterns["word"] == "гугл":
        webbrowser.open("https://google.com") # откроет определеный сайт
    elif patterns["word"] == "папку с проектами":
        webbrowser.open("C:\projects") # откроет определеную папкув проводнике
    elif patterns["word"] == "проводник":
        webbrowser.open("") # откроет проводник
    return f"Открыто \"{patterns["word"]}\""

names = ["Открой { word: [браузер, гугл, папку с проектами, проводник]}"] # тут комманды на которые будет отзыватся бот
sounds = ["./yes.wav"] # тут звуки которые будут производится при успешном выполнении кода