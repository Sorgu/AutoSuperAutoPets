from ahk import AHK
import time
from python_imagesearch.imagesearch import *
from SuperAutoPetsPack1 import pets, gold


class Slot:
    def __init__(self, coords, pet=None):
        self.coords = coords
        self.middleCoords = self.coords[0] + 37, self.coords[1] + 74
        self.pet = pet


shop1 = Slot((623, 541, 698, 639))
shop2 = Slot((721, 541, 796, 639))
shop3 = Slot((819, 541, 894, 639))
shop4 = Slot((917, 541, 992, 639))
shop5 = Slot((1015, 541, 1090, 639))
shop6 = Slot((1113, 541, 1188, 639))
foodshop1 = Slot((1211, 541, 1186, 639))
foodshop2 = Slot((1309, 541, 1284, 639))

pet1 = Slot((627, 349, 702, 447))
pet2 = Slot((723, 349, 798, 447))
pet3 = Slot((819, 349, 894, 447))
pet4 = Slot((915, 349, 990, 447))
pet5 = Slot((1011, 349, 1086, 447))

shopPets = [shop1, shop2, shop3, shop4, shop5, shop6]
Pets = [pet1, pet2, pet3, pet4, pet5]

ahk = AHK()
win = ahk.get_active_window()
title = b"Super Auto Pets (Public testing) by teamwood - Google Chrome"
if win.title == title:
    print("pog")
else:
    sap_window = ahk.find_window(
        title=b"Super Auto Pets (Public testing) by teamwood - Google Chrome")  # Super Auto Pets (Public testing) by teamwood - Google Chrome
    sap_window.activate()
    print(sap_window.title)

time.sleep(0.2)


# Function to search the screen within the provided coordinates for the picture provided
def imageSearch(coords, picture):
    nwx, nwy, sex, sey = coords
    pos = imagesearcharea(picture, x1=nwx, y1=nwy, x2=sex, y2=sey)
    if pos[0] != -1:
        print("position : ", pos[0], pos[1])
        return True
    else:
        print("image not found")
        return False


# Function to get color code from pixel
def getpixel(spot, flag=False):
    if flag == True:
        spot = (spot[0] - 38, spot[1] - 38)

    result = ahk.pixel_get_color(spot[0], spot[1])
    return result


# Transition function that takes a number and calls the buyPet function with the corrosponding Slot object as argument
def buyPetPrep(petSpot):
    if petSpot == 0:
        buyPet(pet1)
    elif petSpot == 1:
        buyPet(pet2)
    elif petSpot == 2:
        buyPet(pet3)
    elif petSpot == 3:
        buyPet(pet4)
    elif petSpot == 4:
        buyPet(pet5)


# Function to buy a new pet
def buyPet(className):
    for each in shopPets:
        print(each.pet)
        if each.pet:
            ahk.mouse_position = (each.middleCoords)
            time.sleep(0.2)
            ahk.mouse_drag(className.middleCoords, speed=10)
            className.pet = each.pet
            time.sleep(1)
            checkStore()
            return
    roll()  # Rolls the store if there are no pets to be bought
    return


# Function to press the roll button
def roll():
    ahk.mouse_move(450, 780)
    ahk.click()
    time.sleep(1.5)
    checkStore()


# Function to check the current gold value
def goldCheck():
    rg = region_grabber((321, 133, 424, 194))
    for each in gold:
        test = imagesearcharea(each["picture"], 321, 133, 424, 194, im=rg, precision=0.9)
        if test[0] != -1:
            print(each["amount"])
            return each["amount"]
    print("GOLD ERROR")
    return False


def checkDeafeat():
    if getpixel((462, 750)) != "0x3C3C3C":
        return
    ahk.mouse_move(960, 540)
    ahk.click()
    print("Defeat :(")
    time.sleep(0.5)
    ahk.click()


def checkNewTier():
    if getpixel((850, 388)) == "0xFFFFFF" and getpixel((548, 143)) == "0x191919":
        ahk.mouse_move(960)
        ahk.click()


def checkNameCreate():
    if getpixel((437, 367)) == "0x1F31A0":
        ahk.mouse_move(575, 383)
        ahk.click()
        ahk.mouse_move(575, 583)
        ahk.click()
        ahk.mouse_move(1450, 778)
        ahk.click()


def checkRoundOver():
    continueAfterRound = (952, 403)
    if getpixel(continueAfterRound) == "0xF5CF55":
        ahk.mouse_move(continueAfterRound)
        ahk.click()
        time.sleep(3)


# Function to upgrade pets that are eligible
def upgradePets():
    for each in shopPets:
        if not each.pet:
            continue
        for every in Pets:
            if each.pet == every.pet:
                print(each.pet, each.middleCoords, every.pet, every.middleCoords)
                ahk.mouse_position = each.middleCoords
                ahk.mouse_drag(every.middleCoords, speed=10)
                checkStore()
                time.sleep(0.5)
                return 1


# Function to use image recognition on every store pet and save the known ones as Slot.pet
def checkStore():
    for each in shopPets:
        rg = region_grabber(each.coords)
        for every in pets:
            result = imagesearcharea(every["picture"], each.coords[0], each.coords[1], each.coords[2], each.coords[3],
                                     im=rg)
            if result[0] == -1:
                each.pet = None
                continue
            else:
                each.pet = every["name"]
                print("checkStore", each.pet)
                break


# Main function that infinitely loops
def main():
    while True:
        checkRoundOver()
        checkNewTier()
        checkNameCreate()
        checkStore()
        while goldCheck() != 0:
            if goldCheck() <= 2:
                roll()
            elif imageSearch(pet1.coords, "./pics/emptyPedestal.jpg"):
                buyPetPrep(0)
            elif imageSearch(pet2.coords, "./pics/emptyPedestal.jpg"):
                buyPetPrep(1)
            elif imageSearch(pet3.coords, "./pics/emptyPedestal.jpg"):
                buyPetPrep(2)
            elif imageSearch(pet4.coords, "./pics/emptyPedestal.jpg"):
                buyPetPrep(3)
            elif imageSearch(pet5.coords, "./pics/emptyPedestal.jpg"):
                buyPetPrep(4)
            elif upgradePets():
                pass
            else:
                print("no buy or upgrades")
                roll()
                checkStore()
            time.sleep(1)
        ahk.mouse_move(1396, 779)
        ahk.click()
        checkDeafeat()
        time.sleep(4)


main()
