
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

##SETUP AND INSTALLATION
