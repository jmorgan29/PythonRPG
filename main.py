import classes
from classes.game import *
from classes.magic import *
from classes.inventory import Item

print("\n\n")
print("NAME           HP                               MP")
print("               ________________________         __________")
print(bcolors.BOLD + "Valos:"+
      "460/460 |"+bcolors.OKGREEN + "████████████████████████" + bcolors.ENDC + bcolors.BOLD+ "| "+
      "65/65 |"+bcolors.OKBLUE + "██████████"+bcolors.ENDC+"|")

#Create Black Magic
fire = Spell("Fire",10, 100, "black")
thunder = Spell("Thunder", 10 ,100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 12, 120, "black")

#Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create some Items
potion = Item("Potion","potion","Heals 50 HP",50)
hipotion = Item("Hi-Potion","potion","Heals 100 HP",100)
superpotion = Item("Super Potion","potion","Heals 500 HP",500)
elixer = Item("Elixer","elixer","Fully restores HP/MP of one party member",9999) # 9999 is just a random number because it is irrelevant
hielixer = Item("MegaElixer","elixer","Fully restores party's HP/MP",9999)
grenade = Item("Grenade","attack","Deals 500 Damage",500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
#player_items = [potion, hipotion, superpotion, elixer, hielixer,grenade]
player_items = [{"item":potion, "quantity":15},{"item":hipotion,"quantity":5},
                {"item":superpotion,"quantity":5},{"item":elixer,"quantity":5},
                {"item":hielixer,"quantity":2},{"item":grenade,"quantity":5}]
#Instatiate People
player = Person(460, 65, 60, 34, player_spells,player_items)

enemy = Person(1200, 65, 45, 25, [],[])

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("========================")
    player.choose_action()
    choice = input("Choose action:")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())
    elif index ==1:
        player.choose_magic()
        magic_choice = int(input("Choose magic:")) - 1

        if magic_choice == -1:
            continue

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enought MP\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
        elif spell.type == "black":
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)
    elif index==2:
        player.choose_item()
        item_choice = int(input("Choose item:")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]["item"]
        

        if player.items[item_choice]["quantity"] ==0:
            print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
            continue

        player.items[item_choice]["quantity"] -=1
        
        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop),"HP",bcolors.ENDC)
        elif item.type == "elixer":
            player.hp = player.maxhp
            player.mp = player.maxmp
            print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
        elif item.type == "attack":
            enemy.take_damage(item.prop)
            print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage" + bcolors.ENDC)


    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg, "points of damage.")
    print("----------------------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")
    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp())+bcolors.ENDC)
    print("Your MP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC + "\n")

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False


