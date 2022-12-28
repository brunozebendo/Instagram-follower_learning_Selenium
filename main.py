"""a intenção do código é criar um bot para acessar uma conta no instagram que tenha um tema que seja
parecido com o da sua página, ou seja, que tenha seguidores que podem se interessar pelo seu assunto e
dar follow nesses seguidores, para que algum talvez te seguir de volta"""
"""primeiro, as bibliotecas, webdriver par lidar com o navegador, keys, para pressionar as teclas, exceção
para lidar com a exceção no fluxo de comando e time"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
"""aqui as variáveis constantes padrão, lembrando sempre que variáveis constantes se escreve no maiúsculo. O caminho
do chrome_drive_path no computador, o nome da conta cujos seguidores serão seguidos, nome e senha para acessar o instagram"""
CHROME_DRIVER_PATH = YOUR CHROM DRIVER PATH
SIMILAR_ACCOUNT = "buzzfeedtasty"
USERNAME = YOUR INSTAGRAM USERNAME
PASSWORD = YOUR INSTAGRAM PASSWORD

"""cria-se uma classe que conterá as quatro funções necessárias. Reparar na organização do código"""
class InstaFollower:
"""primeiro o função construtora que serve para guardar o caminho do web driver"""
    def __init__(self, path):
        self.driver = webdriver.Chrome(executable_path=path)
"""depois, a função de login que acha os elementos de login e passa as variáveis para eles, depois pressiona enter"""
    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)

        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        time.sleep(2)
        password.send_keys(Keys.ENTER)
"""aqui, a função para achar seguidores, primeiro acha o nome da página que é o endereço do instagram mais o nome da
página, depois acha o x-path do botão de seguidores, depois vem a função execute_script para scrollar. Pelo que 
pesquisei, há algumas funções que o selenium não consegue fazer diretamente, por isso, ele faz através do javascript,
 e a sintaxe para isso é a abaixo. O elemento scrollHeight vai ler a altura do elemento, incluindo a parte não visível,
 que tem que scrollar para ver. Já o scrollTop é a medida entre o topo do elemento e o seu elemento mais no topo,
 ou seja, pelo que entendi, entre o começo da janela e o elemento que primeiro aparece nela, quando há o scroll. Assim,
 pelo que entendi, o for loop vai iterar pelos 10 elementos, que é o número de seguidores mostrados por vez, 
 então o javascript vai executar no primeiro elemento o que já vai fazer a tela rolar, o primeiro elemento será o elemento
 que está entre a o topo da tela e a altura. Complexo..."""
    def find_followers(self):
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")

        time.sleep(2)
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followers.click()

        time.sleep(2)
        modal = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)
"""aqui o comando para clicar no botão de follow, mas lidar com a exceção caso seja uma pessoa que já se siga"""
    def follow(self):
        all_buttons = self.driver.find_elements_by_css_selector("li button")
        for button in all_buttons:
            try:
                button.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
                cancel_button.click()

"""aqui, as funções são iniciadas"""
bot = InstaFollower(CHROME_DRIVER_PATH)
bot.login()
bot.find_followers()
bot.follow()