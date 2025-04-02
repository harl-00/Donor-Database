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
        );''')
    

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
    
#FIX SYNTAX ERROR IN ADD_NEW_DONOR WHEN HOME
    
def view_current_donors():
    conn = sqlite3.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    conn.close()
    for donor in donors:
        print(donor)

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
    cursor.execute("DELETE FROM donors WHERE donor_id=?", (donor_id,))
    conn.commit()
    conn.close()
    print("Donor deleted")

if __name__ == "__main__":
    init_db()
    print("Database online")
    while True:
        print("1. Add Donor 2. View Donors 3. Update Donor 4. Delete Donor 5.Exit")
       
        choice = input("Enter choice: ")
        if choice == "1":
            first_name = input("First Name: ")
            surname = input("Surname: ")
            business_name = input("Business Name: ")
            postcode = input("Postcode: ")
            house_number = input("House Number: ")
            phone_number = input("Phone Number: ")
            add_new_donor(first_name, surname, business_name, postcode, house_number, phone_number)
            
        elif choice == "2":
            view_current_donors()
            
        elif choice == "3":
            donor_id = input("Enter Donor ID To update: ")
            first_name = input("New First Name: ")
            surname = input("New Surname: ")
            bussiness_name = input("New Business Name: ")
            postcode = input("New Postcode: ")
            house_number = input("New House Number: ")
            phone_number = input("New Phone Number: ")
            update_donor(donor_id, first_name, surname, business_name, postcode, house_number, phone_number)
            
        elif choice == "4":
            donor_id = input("Enter Donor ID To delete: ")
            deleting_donor(donor_id)
            
