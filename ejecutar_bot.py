from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore
from selenium import webdriver
import chromedriver_autoinstaller
import datetime
import random
import pickle
import time
import sys
import os

chromedriver = chromedriver_autoinstaller.install(cwd=True)


class InstagramBot():
    def __init__(self, friends_usernames=None):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])

        self.browser = webdriver.Chrome(chromedriver, options=chrome_options)
        self.friends_usernames = friends_usernames

    def checkLogin(self):
        try:
            WebDriverWait(self.browser, 7).until(lambda d: d.find_element_by_css_selector(
                "textarea[placeholder='Agrega un comentario...']"))
            return True
        except:
            try:
                WebDriverWait(self.browser, 7).until(lambda d: d.find_element_by_css_selector(
                    "textarea[placeholder='Añade un comentario...']"))
                return True
            except:
                return False

    def commentPost(self, tipo_sorteo, parametros):
        inicio_script = time.time()
        lastRandomTime = 0
        comentariosEnviados = 0

        if (tipo_sorteo == 1 or tipo_sorteo == 3):
            cantidadTotalComentarios = len(self.friends_usernames)
        else:
            cantidadTotalComentarios = parametros[1]

        for x in range(cantidadTotalComentarios):
            try:
                WebDriverWait(self.browser, 7).until(lambda d: d.find_element_by_css_selector(
                    "textarea[placeholder='Agrega un comentario...']"))

                self.browser.find_element_by_css_selector(
                    "textarea[placeholder='Agrega un comentario...']").clear()
                self.browser.find_element_by_css_selector(
                    "textarea[placeholder='Agrega un comentario...']").click()

                if (tipo_sorteo == 1):
                    for z in range(parametros[0]):
                        tempUser = self.friends_usernames[x - z]
                        self.browser.find_element_by_css_selector(
                            "textarea[placeholder='Agrega un comentario...']").send_keys(tempUser, ' ')
                        time.sleep(1)

                elif (tipo_sorteo == 2):
                    self.browser.find_element_by_css_selector(
                        "textarea[placeholder='Agrega un comentario...']").send_keys(parametros[0])

                else:
                    for z in range(parametros[0]):
                        tempUser = self.friends_usernames[x - z]
                        self.browser.find_element_by_css_selector(
                            "textarea[placeholder='Agrega un comentario...']").send_keys(tempUser, ' ')
                        time.sleep(1)

                    self.browser.find_element_by_css_selector(
                        "textarea[placeholder='Agrega un comentario...']").send_keys(str(" " + parametros[1]))

                time.sleep(2)

                try:
                    # WebDriverWait(self.browser, 2).until(lambda d: d.find_element_by_css_selector("button[type='submit']"))
                    WebDriverWait(self.browser, 2).until(lambda d: d.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/div[2]/div'
                    ))

                    # self.browser.find_element_by_css_selector("button[type='submit']").click()
                    self.browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/div[2]/div').click()

                    comentariosEnviados += 1

                    if (x != cantidadTotalComentarios - 1):
                        newRandomTime = random.randrange(30, 120, 1)
                        if ((lastRandomTime - 5) <= newRandomTime <= (lastRandomTime + 5)):
                            newRandomTime = newRandomTime + 20
                            lastRandomTime = newRandomTime
                        else:
                            lastRandomTime = newRandomTime

                        for i in range(newRandomTime):
                            print("\nComentarios realizados: {}\nTiempo hasta el proximo comentario: {} / {} segs ".format(
                                comentariosEnviados, (lastRandomTime - i), lastRandomTime))
                            time.sleep(1)
                            os.system("cls")

                except:
                    os.system("cls")
                    print(
                        (Fore.LIGHTRED_EX + "\nERROR #5: El boton de enviar comentarios no es clickeable."))
                    print("\t- ¿Utilizaste mucho el bot ultimamente?")
                    print("\t- ¿Estas en la publicacion?")
                    print("\t- ¿Alguno/s de los que etiquetaste te bloqueo?")
                    input()

            except:
                os.system("cls")
                print(
                    (Fore.LIGHTRED_EX + "\nERROR #6: No se puede escribir el comentario."))
                print("\t- ¿Utilizaste mucho el bot ultimamente?")
                print("\t- ¿La publicacion permite comentarios?")
                print("\t- ¿Estas en la publicacion?")
                input()

        fin_script = time.time()

        print("Script terminado", "Duracion: " +
              str(datetime.timedelta(seconds=round(fin_script-inicio_script, 0))))
        print("Comentarios realizados: " + str(comentariosEnviados))

    def loadCookies(self):
        self.browser.get("https://www.instagram.com/")

        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)

            self.browser.refresh()

        except:
            print("- Warning: No hay cookies. Deberas iniciar sesion!\n")


def SiNoInput():
    rta = input((Fore.LIGHTGREEN_EX + "[s] SI") + (Fore.RESET + " | ") + (
        Fore.LIGHTRED_EX + "[n] NO ") + (Fore.RESET + ">> "))
    if rta.lower().strip() in ["s", "si", "y", "yes"]:
        return 1
    else:
        return 0


def menuTipoSorteo():
    parametros = []
    while True:
        print("\n# PASO 2: ¿Que " + (Fore.YELLOW + "tipo") +
              (Fore.WHITE + " de sorteo es?"))
        print("  1 - Solo mencionar a otros usuarios                " +
              (Fore.LIGHTBLACK_EX + "@pablo_sanchez @juancarlos1 @pepe.gomez"))
        print("  2 - Solo comentar datos                            " +
              (Fore.LIGHTBLACK_EX + "Ultimos 3 del dni"))
        print("  3 - Mencionar usuarios y datos                     " +
              (Fore.LIGHTBLACK_EX + "@pablo_sanchez Sucursal Cerro"))
        print("  9 - Salir")
        opcionMenu = input("\nIngresar una opcion >> ").strip()

        if opcionMenu == "1":
            while True:
                os.system("cls")
                print(
                    (Fore.YELLOW + "Tipo 1 de sorteo: 'Solo mencionar a otros usuarios'"))
                try:
                    cantidad_usuarios = int(
                        input("Cantidad de usuarios por comentario >> ").strip())
                    if cantidad_usuarios <= 0:
                        input("\nDebes ingresar un numero mayor a cero." +
                              ((Fore.GREEN + "\nEnter") + (Fore.WHITE + " para reintentar")))

                    else:
                        print("\n¿Estas seguro?")

                        while True:
                            si_no = SiNoInput()
                            if si_no == 1:
                                parametros.append(cantidad_usuarios)
                                return 1, parametros
                            elif si_no == 0:
                                break

                except ValueError:
                    pass

        elif opcionMenu == "2":
            while True:
                os.system("cls")
                print((Fore.YELLOW + "Tipo 2 de sorteo: 'Solo comentar datos'"))
                dato_comentario = input("Datos a comentar >> ").strip()

                try:
                    cantidad_comentarios = int(
                        input("Cantidad de comentario a enviar >> ").strip())
                    if cantidad_comentarios <= 0:
                        input("\nDebes ingresar un numero mayor a cero." +
                              ((Fore.GREEN + "\nEnter") + (Fore.WHITE + " para reintentar")))

                    else:
                        if dato_comentario != "":
                            print("\n¿Estas seguro?")

                            while True:
                                si_no = SiNoInput()
                                if si_no == 1:
                                    parametros.append(dato_comentario)
                                    parametros.append(cantidad_comentarios)
                                    return 2, parametros
                                elif si_no == 0:
                                    break
                except ValueError:
                    pass

        elif opcionMenu == "3":
            while True:
                os.system("cls")
                print((Fore.YELLOW + "Tipo 3 de sorteo: 'Mencionar usuarios y datos'"))

                try:
                    cantidad_usuarios = int(
                        input("Cantidad de usuarios por comentario >> ").strip())
                    if cantidad_usuarios <= 0:
                        input("\nDebes ingresar un numero mayor a cero." +
                              ((Fore.GREEN + "\nEnter") + (Fore.WHITE + " para reintentar")))

                    else:
                        dato_comentario = input("Datos a comentar >> ").strip()

                        if dato_comentario != "":
                            print("\n¿Estas seguro?")

                            while True:
                                si_no = SiNoInput()
                                if si_no == 1:
                                    parametros.append(cantidad_usuarios)
                                    parametros.append(dato_comentario)
                                    return 3, parametros
                                elif si_no == 0:
                                    break

                except ValueError:
                    pass

        elif opcionMenu == "9":
            mensajeSalida()
        else:
            input("\nDebes ingresar un numero valido => [1, 2, 3, 9]." + (
                (Fore.GREEN + "\nEnter") + (Fore.WHITE + " para reintentar")))


def checkFriendsFile():
    friends_usernames = []
    try:
        with open('friends_usernames.txt', encoding='utf8') as f:
            for line in f:
                if (line.strip().startswith("@") and ' ' not in line.strip()):
                    friends_usernames.append(line.strip())

                elif (' ' in line.strip()):
                    print('"' + str(line.strip()) + '"' +
                          " tiene un espacio entremedio, corregilo!")

                elif (not line.isspace()):
                    friends_usernames.append("@" + line.strip())

    except IOError:
        print((Fore.LIGHTRED_EX + "ERROR #1: El archivo ") + (Fore.YELLOW +
                                                              "friends_usernames.txt") + (Fore.LIGHTRED_EX + " no se puede leer."))
        print("\t- ¿Esta creado?")
        print("\t- ¿Tiene otro nombre?")
        mensajeSalida()

    if (len(friends_usernames) == 0):
        print((Fore.LIGHTRED_EX + "ERROR #2: Debes agregar nombres de usuarios en ") +
              (Fore.YELLOW + "friends_usernames.txt"))
        mensajeSalida()

    return friends_usernames


def enterParaSeguir():
    print(Fore.GREEN + "\n\n           - Toca ENTER para seguir -          ")
    input()


def mensajeSalida():
    print(Fore.LIGHTRED_EX + "\n\n            - Toca ENTER para salir -          ")
    input()
    sys.exit()
    # os.system("shutdown /s /t 1")


def main():
    init(autoreset=True)
    print("# PASO 0: " + (Fore.YELLOW + "INICIANDO GOOGLE CHROME... -"))

    # 1 - Load friends
    friends_usernames = checkFriendsFile()

    # 2 - Init Bot
    bot = InstagramBot(friends_usernames=friends_usernames)

    # 3 - Check cookies
    bot.loadCookies()

    # 4 - Login and enter post
    print("# PASO 1: " + (Fore.YELLOW + "Iniciar Sesion y busca la publicacion"))
    enterParaSeguir()

    # 5 - Save cookies
    while True:
        if (bot.checkLogin()):
            pickle.dump(bot.browser.get_cookies(), open("cookies.pkl", "wb"))

            # 6 - Select type of giveaway and params
            tipo_sorteo, params = menuTipoSorteo()

            # 7 - Comments
            bot.commentPost(tipo_sorteo, params)

            break

        else:
            print((Fore.LIGHTBLUE_EX + "\n- Warning: " +
                   (Fore.WHITE + "Parece que NO iniciaste sesion!")))
            enterParaSeguir()

    # 8 - Quit
    mensajeSalida()


main()
