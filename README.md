
# Secure Login & File Management System

This project implements a secure authentication and file management system using **two distinct backend approaches** as required:
1. A **Custom Backend** built with Python (Flask) and PostgreSQL.
2. A **Managed Backend** using Appwrite (BaaS) with a custom JavaScript adapter.

The project features secure password hashing using Argon3, strict data isolation (IDOR prevention)
---
**In This Project, I've Used **session** based authentication over JWT because:**

  1. Instant Server-Side Logout: The project requires immediate session invalidation upon logout. With cookies, session.clear() instantly destroys the session on the server. With stateless JWTs, achieving this requires complex and resource-heavy token blacklisting.
  2. Session-based authentication is generally safer for most standard web applications because it gives you absolute control over user access and mitigates the massive security risks associated with client-side token storage.
  3. Protection Against Token Theft: JWTs are frequently stored in HTML5 LocalStorage, which is highly vulnerable to Cross-Site Scripting (XSS) attacks. If an attacker injects a malicious script into your frontend, they can read the LocalStorage and steal the JWT. Sessions use HttpOnly and Secure cookies, which completely blocks JavaScript from reading the session ID.
---

## Logout implementation
**In Flask (Custom Backend):** The /logout route calls session.clear(). This instantly wipes the user's data from the server's session store.
**In Appwrite (Managed Backend):** The frontend adapter calls the SDK method account.deleteSession('current'). This sends an authenticated API request to Appwrite's servers, which explicitly revokes and deletes the session token from their database, invalidating it globally.
---
