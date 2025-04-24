import sqlite3

def init_db():
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS donors (
            donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            surname TEXT NOT NULL,
            business_name TEXT,
            postcode TEXT,
            house_number TEXT,
            phone_number TEXT
        );
        
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            room_info TEXT,
            booking_date TEXT,
            cost TEXT
        );
        
        CREATE TABLE IF NOT EXISTS person (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            surname TEXT NOT NULL,
            phone_number TEXT
        );
        
        CREATE TABLE IF NOT EXISTS donations (
            donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER,
            event_id INTEGER,
            amount TEXT NOT NULL,
            date TEXT NOT NULL,
            gift_aid BOOLEAN,
            notes TEXT,
            FOREIGN KEY (donor_id) REFERENCES donors(donor_id) ON DELETE CASCADE,
            FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
        );
    
        CREATE TABLE IF NOT EXISTS donation_sources (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER,
            source_type TEXT CHECK(source_type IN ('Donor', 'Event')) NOT NULL,
            FOREIGN KEY (donation_id) REFERENCES donations(donation_id) ON DELETE CASCADE
        );
    ''')
    conn.commit()
    conn.close()


def add_new_donor(first_name, surname, business_name, postcode, house_number, phone_number):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO donors (first_name, surname, business_name, postcode, house_number, phone_number) 
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (first_name, surname, business_name, postcode, house_number, phone_number))
    conn.commit()
    conn.close()
    print("Donor added successfully")
    
    
def view_current_donors():
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    for donor in cursor.fetchall():
        print(donor)
    conn.close()

def updating_donor(donor_id, first_name, surname, business_name, postcode, house_number, phone_number):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE donors SET first_name=?, surname=?, business_name=?, postcode=?, house_number=?, phone_number=?
        WHERE donor_id=?
    ''', (first_name, surname, business_name, postcode, house_number, phone_number, donor_id))
    conn.commit()
    conn.close()
    print("Donor updated")

def deleting_donor(donor_id):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM donations WHERE donor_id=?", (donor_id,))
    if cursor.fetchone()[0] > 0:
        print("Can't delete donor as they have already donated.")
    else:
        cursor.execute("DELETE FROM donors WHERE donor_id=?", (donor_id,))
        print("Donor deleted")
    conn.commit()
    conn.close()

def add_event(event_name, room_info, booking_date, cost):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (event_name, room_info, booking_date, cost) VALUES (?, ?, ?, ?)",
                   (event_name, room_info, booking_date, cost))
    conn.commit()
    conn.close()
    print("Event added")

def view_events():
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    for event in cursor.fetchall():
        print(event)
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM donations WHERE event_id=?", (event_id,))
    if cursor.fetchone()[0] > 0:
        print("cant delete event, donations have been made")
    else:
        cursor.execute("DELETE FROM events WHERE event_id=?", (event_id,))
        print("event deleted.")
    conn.commit()
    conn.close()

def add_donation(donor_id, event_id, amount, date,gift_aid, notes):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO donations (donor_id, event_id, amount, date, gift_aid, notes)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (donor_id, event_id, amount, date, gift_aid, notes))
    conn.commit()
    conn.close()
    print("donation added.")

def view_donations():
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations")
    for donation in cursor.fetchall():
        print(donation)
    conn.close()

def search_donations_by_donor(donor_id):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations WHERE donor_id=?", (donor_id,))
    results = cursor.fetchall()
    if results:
        for donation in results:
            print(donation)
    else:
        print("no donations have been made by this donor")
    conn.close()

def search_donations_by_event(event_id):
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations WHERE event_id=?", (event_id,))
    results = cursor.fetchall()
    if results:
        for donation in results:
            print(donation)
    else:
        print("no donations found in this event.")
    conn.close()
#CREATE INTERFACE HERE ON THURSDAY
def main_menu():
    while True:
        print("Charity Donation Tracker ")
        print("1 Manage Donors")
        print("2 Manage Events")
        print("3 Manage Donations")
        print("4 Exit")

        choice = input("Select an option.")

        if choice == "1":
            donor_menu()
        elif choice == "2":
            event_menu()
        elif choice == "3":
            donation_menu()
        elif choice == "4":
            print("end")
            break
        else:
            print("select from the options")

def donor_menu():
    while True:
        print("Donor Menu")
        print("1 Add Donor")
        print("2 View Donors")
        print("3 Update Donor")
        print("4 Delete Donor")
        print("5 Back")

        choice = input("Select an option. ")

        if choice == "1":
            fn = input("First Name: ")
            sn = input("Surname: ")
            bn = input("Business Name: ")
            pc = input("Postcode: ")
            hn = input("House Number: ")
            pn = input("Phone Number: ")
            add_new_donor(fn, sn, bn, pc, hn, pn)
        elif choice == "2":
            view_current_donors()
        elif choice == "3":
            donor_id = input("ID to update: ")
            fn = input("First Name: ")
            sn = input("Surname: ")
            bn = input("Business Name: ")
            pc = input("Postcode:")
            hn = input("House Number: ")
            pn = input("Phone Number: ")
            updating_donor(donor_id, fn, sn, bn, pc, hn, pn)
        elif choice == "4":
            donor_id = input("id deleting is ")
            deleting_donor(donor_id)
        elif choice == "5":
            break
        else:
            print("Invalid")

def event_menu():
    while True:
        print("Event Menu")
        print("1 Add Event")
        print("2 View Events")
        print("3 Delete Event")
        print("4 Back")

        choice = input("Select an option. ")

        if choice == "1":
            name = input("Event Name: ")
            room = input("Room Info: ")
            date = input("Booking Date: ")
            cost = input("Cost:")
            add_event(name, room, date, cost)
        elif choice == "2":
            view_events()
        elif choice == "3":
            event_id = input("id deleting is ")
            delete_event(event_id)
        elif choice == "4":
            break
        else:
            print("Invalid")

def donation_menu():
    while True:
        print("Donation Menu ")
        print("1 Add Donation")
        print("2 View Donations")
        print("3Search by Donor ID")
        print("4 Search by Event ID")
        print("5 Back")

        choice = input("Select an option ")

        if choice == "1":
            donor_id = input("Donor ID: ") or None
            event_id = input("Event ID : ") or None
            amount = input("Amount: ")
            date = input("Date: ")
            gift_aid = bool(int(input("Gift 1 yes 2 no")))
            notes = input("Notes")
            add_donation(donor_id, event_id, amount, date, gift_aid, notes)
        elif choice == "2":
            view_donations()
        elif choice == "3":
            donor_id = input("Donor ID: ")
            search_donations_by_donor(donor_id)
        elif choice == "4":
            event_id = input("Event ID: ")
            search_donations_by_event(event_id)
        elif choice == "5":
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    init_db()
    main_menu()
