# -*- coding: utf-8 -*-
"""Project File



Original file is located at
    https://colab.research.google.com/drive/1n7zXN5qbx6o8JX6AdgaoB3tSzm7g9mZg

ACM-STUDENT MANAGEMENT SYSTEM
"""

import csv
import random
import matplotlib.pyplot as plt

# Load Data from CSV
def load_data(filename):
    data = []
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File {filename} not found. Creating new file.")
    return data

# Save Data to CSV
def save_data(filename, data):
    fieldnames = ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender', 'Year', 'Member ID', 'Password']
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename} successfully.")

# Generate a unique 4-digit Member ID
def generate_member_id():
    return random.randint(1000, 9999)

# Register a new user
def register(filename):
    data = load_data(filename)
    member_id = generate_member_id()
    existing_ids = {member['Member ID'] for member in data}

    while str(member_id) in existing_ids:
        member_id = generate_member_id()

    print(f"Your Member ID is: {member_id}")

    password = input("Set your password (4 characters): ")
    while len(password) != 4:
        print("Password must be exactly 4 characters.")
        password = input("Set your password (4 characters): ")

    profile = personal_profile()
    profile.update({'Member ID': str(member_id), 'Password': password})

    data.append(profile)
    save_data(filename, data)
    print("\nProfile created successfully!")
    return profile

# Authenticate user
def authenticate(filename):
    print("\nLogin:")
    member_id = input("Enter your Member ID: ")
    password = input("Enter your password: ")

    data = load_data(filename)
    for member in data:
        if member['Member ID'] == member_id and member['Password'] == password:
            print("\nLogin successful.")
            return member
    print("\nInvalid Member ID or Password.")
    return None

# Personal Profile
def personal_profile():
    print("\nPersonal Profile Setup")
    print("----------------------")
    first_name = input("Enter your first name: ")
    middle_name = input("Enter your middle name (optional): ")
    last_name = input("Enter your last name: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender (Male/Female/Other): ")

    valid_years = ["First", "Second", "Third", "Fourth"]
    year = input("Enter your year (First/Second/Third/Fourth): ").capitalize()
    if year not in valid_years:
        print("Invalid year. Setting year to 'Unknown'.")
        year = "Unknown"

    return {
        'First Name': first_name,
        'Middle Name': middle_name,
        'Last Name': last_name,
        'Age': age,
        'Gender': gender,
        'Year': year
    }

# Display Members and plot distribution charts
def display_members(data):
    print("\nClub Members")
    print("------------")
    for member in data:
        print(f"{member['First Name']} {member['Last Name']} - Gender: {member['Gender']}, Year: {member['Year']}")

    while True:
        print("\nOptions:")
        print("1. View Gender Distribution")
        print("2. View Year Distribution")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            plot_gender_distribution(data)
        elif choice == "2":
            plot_year_distribution(data)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Plot Gender Distribution
def plot_gender_distribution(data):
    gender_counts = {}
    for member in data:
        gender = member['Gender']
        gender_counts[gender] = gender_counts.get(gender, 0) + 1
    labels = list(gender_counts)
    sizes = list(gender_counts.values())

    plt.pie(sizes, labels=labels)
    plt.title('Gender Distribution of Members')
    plt.show()


# Plot Year Distribution
def plot_year_distribution(data):
    year_counts = {}
    for member in data:
        year = member['Year']
        year_counts[year] = year_counts.get(year, 0) + 1
    plt.bar(year_counts.keys(), year_counts.values())
    plt.title('Year Distribution of Members')
    plt.xlabel('Year')
    plt.ylabel('Number of Members')
    plt.show()

# Display and plot events
def display_events(filename):
    data = load_data(filename)
    if not data:
        print("No events found.")
        return
    plot_participant_distribution(data)

# Plot Participants Distribution
def plot_participant_distribution(data):
    participants_counts = [int(event['Participants']) for event in data]
    event_names = [event['Event Name'] for event in data]

    plt.bar(event_names, participants_counts)
    plt.title('Participants Distribution by Event')
    plt.xlabel('Event Name')
    plt.ylabel('Number of Participants')
    plt.tight_layout()
    plt.show()


# Search for a member by name
def search_member(data):
    name = input("Enter the name to search (first or last): ").strip().lower()
    results = [member for member in data if name in member['First Name'].lower() or name in member['Last Name'].lower()]
    if results:
        print("\nSearch Results:")
        for member in results:
            print(f"{member['First Name']} {member['Last Name']} - Gender: {member['Gender']}, Year: {member['Year']}")
    else:
        print("No member found with that name.")

# Main Menu
def main_menu(filename, event_file, user_profile):
    while True:
        print("\nMain Menu")
        print("---------")
        print("1. About Members")
        print("2. Search Member")
        print("3. View Events")
        print("4. Logout ")
        choice = input("Enter your choice: ")

        if choice == "1":
            display_members(load_data(filename))
        elif choice == "2":
            search_member(load_data(filename))
        elif choice == "3":
            display_events(event_file)
        elif choice == "4":
            print(" Successfully Logging out")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Main Function
def main():
    filename = 'members.csv'
    event_file = 'events.csv'

    print("WELCOME TO ACM CHAPTER DASHBOARD")
    print("--------------------------")
    print("1. Create New Account")
    print("2. Login to Existing Account")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        user_profile = register(filename)
        main_menu(filename, event_file, user_profile)
    elif choice == "2":
        user_profile = authenticate(filename)
        if user_profile:
            main_menu(filename, event_file, user_profile)
    else:
        print("Invalid choice. Please restart and choose 1 or 2.")

# Run the program
if __name__ == "__main__":
    main()
