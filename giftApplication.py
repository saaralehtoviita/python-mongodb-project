from pymongo import MongoClient
from bson.objectid import ObjectId

# yhdistään paikalliseen klusteriin
client = MongoClient("mongodb://localhost:27017/") 
# asetetaan kannaksi christmas
db = client["christmas"]

print("Welcome to the christmas gift application!")

def print_commands():
    print("The application allows you to: ")
    print("\t1) List family members ")
    print("\t2) List gifts")
    print("\t3) Add a gift")
    print("\t4) Add a familymember")
    print("\t5) Edit a gift")
    print("\t6) Edit a familymember")
    print("\t7) Delete a gift")
    print("\t8) Delete a familymember")
    print("\t9) Find gifts of one familymember")
    print("\t10) Exit application")

def list_familyMembers():
    print("List of all familymember names")
    for member in db.family_members.find():
        print(member["member_name"])

def list_gifts():
    print("List of all gifts and their information:")
    for gift in db.gifts.find():
        print("gift id:", gift["_id"])
        print("name of gift:", gift["gift_name"])
        print("price:", gift["price"])
        print("category:", gift["category"])
        print(20*"*")

def add_gift():
    print("Provide the gift information: ")
    memberId = input("MemberId:")
    gift_name = input("gift_name:")
    price = input("price:")
    category = input("category:")

    db.gifts.insert_one({
        "memberId": ObjectId(memberId), "gift_name": gift_name, "price": price, "category": category
    })

    print(f"Gift {gift_name} has been added!")

def add_familyMember():
    print("Provide the familymember information: ")
    name = input("Name of new familymember: ")
    age = input("Age of new familymember: ")
    hobbies = input("Hobbies of new familymember (please separate with comma): ")
    color = input("Favourite color of new familymember: ")

    comma = ","

    if comma in hobbies:
        hobbies = hobbies.split(comma)
        hobbies = [h.strip() for h in hobbies]






    db.family_members.insert_one({ "member_name": name, "age": age, "hobbies": hobbies, "favourite_color": color
    })


def edit_gift():
    print("Which gift do you wanna edit?")
    gift_id = input("Gift ID:")
    print("Provide the new information for the gift: ")
    gift_name = input("gift_name:")
    price = input("price:")
    category = input("category:")

    db.gifts.update_one({ "_id": ObjectId(gift_id) },
                            { "$set": {
                                "gift_name": gift_name,
                                "price": price,
                                "category": category 
                            }}
                    )

def delete_gift():
    print("Which gift do you wanna delete?")
    gift_id = input("Gift ID:")
    obj_id = ObjectId(gift_id)
    gift = db.gifts.find_one({"_id":obj_id})
    print(f"You are about to delete this gift: {gift["gift_name"]}. Do you want to proceed?")
    commandDelete = input("1=yes, 2=no:")
    if commandDelete == "1":
        db.gifts.delete_one({"_id": obj_id})
        print("Gift deleted")
    else:
        print("Deletion cancelled")

def find_gifts_by_familymember():
    print("Whose gifts do you wanna list?")
    memberId = input("Family member ID:")
    obj_id = ObjectId(memberId)
    member = db.family_members.find_one({"_id": obj_id})
    print(f"Listing gifts of {member["member_name"]}")
    for gift in db.gifts.find({"memberId": obj_id}):
        print(gift["gift_name"])

print_commands()

while True:
    command = input("Type in the command number: ")

    if command == "1":
        list_familyMembers()
    elif command == "2":
        list_gifts()
    elif command == "3":
        add_gift()
    elif command =="4":
        add_familyMember()
    elif command == "5":
        edit_gift()
    elif command =="7":
        delete_gift()
    elif command == "9":
        find_gifts_by_familymember()
    elif command == "10":
        break

print("Thank you for using the gift application, goodbye!")