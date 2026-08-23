
# Secure Login & File Management System


This project implements a secure login system authentication and file access system using **two distinct backend approaches** as required:
1. A **Custom Backend** built with Python (Flask) and PostgreSQL.
2. A **Managed Backend** using Appwrite (BaaS) with a custom JavaScript adapter.

## SETUP AND INSTALLATION

*Better clone repo and run this proj inside python virtual env for avoiding any kind of external errors.*

***Open `localhost:xxxx` in BROWSER only. Dont open in VS Code directly***

## Running the Flask Backend

1. **Clone the repository** to your local computer.
2. **Navigate to the backend folder:** Open the `/flask_backend_implementation` directory. *(Note: All subsequent steps must be performed inside this folder).*
3. **Configure environment variables:** Open the `.env.example` file in a text editor. This file contains placeholder values required to run the app.
4. **Update the Database URL:** Replace the sample PostgreSQL database URL with your actual local database URL (ensure the format matches exactly).
5. **Update the Secret Key:** Replace the sample secret key with your own secure, randomly generated string.
6. **Create the `.env` file:** Once you have updated the variables in `.env.example`, type `cp .env.example .env` in your terminal to generate the active environment file. *(Windows users can also just copy and rename the file manually in File Explorer).*
7. Windows: `py -m pip install -r requirements.txt`
8. macOS / Linux: `python3 -m pip install -r requirements.txt`
9. **Start the server:** Type `python app.py` in your terminal to run the server.
10. **View the application:** Open your web browser and navigate to `http://localhost:5000` **IN BROWSER only**.
11. **Windows Alternative:** If you are a Windows user, you can skip the manual terminal commands entirely by simply double-clicking the `start.bat` file inside the `/flask_backend_implementation` folder to automatically configure and start the server.




<figure>
   <img width="877" height="327" alt="image" src="https://github.com/user-attachments/assets/589a38e6-f6d4-4e7b-b0be-cfc842fc9aab" style="display:inline"/>
   <br>
   <figcaption>Sample .env credentials</figcaption>
</figure>

<figure>
   <img width="877" height="400" alt="image" src="https://github.com/user-attachments/assets/20790724-9e81-4e50-a48e-6dc541ad707b" />
   
   <br>
   <figcaption>Sample app test</figcaption>
</figure>

---

## Running Appwrite as Backend
1. open  `/appwrite_implementation` (`cd appwrite_implementation` )
2. Linux/Mac user: `python3 -m http.server 8080`
3. Windows users: `python -m http.server 8080`
4. once you strted the server inside your `/appwrite_implementation` , go to web browser
5. open `localhost:8080`, **IN BROWSER only**

---

## Changes in Default Values (`templates/index.html`)

1. **Updated Default Port**: Changed the default host value from `localhost:3000` to `localhost:5000` on line 31 to optimize the setup for the **Flask backend implementation**.
2. **Flask Radio Selection**: Added the `checked` attribute to the "Backend" radio button on line 25 to streamline the process for Flask users.
3. **Appwrite Radio Selection**: Updated the `checked` attribute on line 26 to improve the default experience for the **Appwrite implementation**.


Only these changes are made, other then that, no changes are made in the Graphical User Interface.

---

## Security Features and Seed-Data (Flask Backend)

1. **Password Hashing**: Implemented **Argon2id** for secure password hashing and user authentication.
2. **UUID User IDs**: Maintained static IDs from `seed-data.json` for existing mock accounts, but implemented **UUIDv4** for all newly registered users. This prevents sequential ID harvesting attacks and enhances system security.
3. **Database Seeding**: Created a `seed_data_into_db()` function in `seed.py` to automatically parse and insert the contents of `seed-data.json` into the PostgreSQL database.
4. Introduced an `AppSettings` table to track whether the seed data has already been populated. On server startup, the application checks this Boolean flag; it skips the seeding process if it is `True`, preventing duplicate database entries.

   
---

## In This Project, I've Used **session** based authentication over JWT because:

  1. Instant Server-Side Logout: The project requires immediate session invalidation upon logout. With cookies, session.clear() instantly destroys the session on the server. With stateless JWTs, achieving this requires complex and resource-heavy token blacklisting.
  2. Session-based authentication is generally safer for most standard web applications because it gives you absolute control over user access and mitigates the massive security risks associated with client-side token storage.
  3. Protection Against Token Theft: JWTs are frequently stored in HTML5 LocalStorage, which is highly vulnerable to Cross-Site Scripting (XSS) attacks. If an attacker injects a malicious script into your frontend, they can read the LocalStorage and steal the JWT. Sessions use HttpOnly and Secure cookies, which completely blocks JavaScript from reading the session ID.

---

## Logout implementation 

**In Flask (Custom Backend):** The /logout route calls session.clear(). This instantly wipes the user's data from the server's session store.
**In Appwrite (Managed Backend):** The frontend adapter calls the SDK method account.deleteSession('current'). This sends an authenticated API request to Appwrite's servers, which explicitly revokes and deletes the session token from their database, invalidating it globally.

---

## Data Isolation

In Flask (Custom Backend): We prevent Insecure Direct Object Reference (IDOR) attacks by never trusting the client. For protected routes, the server extracts the user_id directly from the secure, server-side session cookie. It then explicitly checks if file.owner_id != session_user_id. If they don't match, the server returns a 403 Forbidden error, blocking access even if a user manually manipulates the URL.

In Appwrite (Managed Backend): Isolation is enforced at the database level using Collection Permissions (Row-Level Security). The database is configured to only allow Read access to authenticated users. Furthermore, the frontend adapter explicitly filters all requests using Query.equal('ownerId', user.$id), ensuring the database only ever returns documents owned by the currently logged-in user.

---

**Handled Automatically by Appwrite:**
Secure password hashing, salting, and validation.
Session management, cookie handling, and token generation.
Server infrastructure, CORS policies, and basic security.
**Configured Manually by Me:**
Database Schema: Creating the profiles and files collections and defining their attributes.
Permissions: Setting up Row-Level Security to ensure users can only access their own documents.
Data Seeding: Manually creating the 3 test users (Alice, Bob, Carol) in the Auth dashboard.
Frontend Integration: Writing the appwrite-adapter.js to map the UI button clicks to the Appwrite Web SDK.

---

## What I Would Improve Given More Time?

1. I would have added forget password feature
2. I would have added real files download features using cloud
3. maintain more modularity in files
4. added more comments and instructions for developers to read, the comments are still there, but need to improved for easy undestanding
5. added session timeout features
6. Add a comprehensive test suite using pytest
7. would have implemented 2FA


