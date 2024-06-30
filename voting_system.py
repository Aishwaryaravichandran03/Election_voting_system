import sqlite3
import smtplib
from datetime import datetime

# Connect to the SQLite3 database
mydb = sqlite3.connect("voting.db")
mycursor = mydb.cursor()

# Database setup
def setup_database():
    # Create users table
    mycursor.execute("create table if not exists users (email varchar(50) primary key, name varchar(50), age int, location varchar(70))")

    # Create votes table
    mycursor.execute("create table if not exists votes (candidate varchar(20) primary key, count int)")

    # Insert initial candidates with zero votes if they don't exist
    candidates = ["thiru", "vignesh", "priya","karthika","divya"]
    for candidate in candidates:
        mycursor.execute("insert or ignore into votes (candidate, count) values (?, ?)", (candidate, 0)) 
    mydb.commit()  

# Sending thank you email
def send_thank_you_email(email, name):
    sender_email = "aishwaryar0386@gmail.com"
    sender_password = "nwvc mihn apds tvel"
    now = datetime.now()
    subject = "Thank You email"
    body = f"Dear {name},\n\nThank you for voting!\n\nBest regards,\nElection Team\n\n{now}"
    msg = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg)
        server.quit()
        print(f"Thank you email send to {email}")
    except:
        print("Error: email not sent")

# Main voting function
def main():
    setup_database()
    candidates = ["thiru", "vignesh", "priya","karthika","divya"]
    print("Vote for your candidate:")
    for i, candidate in enumerate(candidates, start=1):
        print(f"Press {i} -> {candidate}")
    
    while True:
        try: 
            email = input("Enter your email id: ")
           
            if email=="q":
            	break
            mycursor.execute("select * from users where email = ?", (email,))
            if mycursor.fetchone():
                print("You have already voted.")
            else:
                name = input("Enter your name: ")
                age = int(input("Enter your age: "))
                location = input("Enter your location: ")
                vote = int(input("Press your vote: "))
                if vote in [1,2,3,4,5]:
                    mycursor.execute("insert into users (email, name, age, location) values (?, ?, ?, ?)", (email, name, age, location))
                    mycursor.execute("update votes set count = count + 1 where candidate = ?", (candidates[vote - 1],))
                    mydb.commit()
                    send_thank_you_email(email, name)
                    f= open("email_sended_person.txt", "a") 
                    f.write(f"Thank you mail send to {name} at {datetime.now()}\n")
                    print(f"You voted for {candidates[vote - 1]}")
                else:
                    print("Invalid vote, please try again.")
        except ValueError:
            print("Invalid input, please enter a valid number.")

main()