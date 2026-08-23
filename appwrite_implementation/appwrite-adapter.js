// appwrite-adapter.js

// 1. Define the Adapter Functions
const appwriteAdapter = {
    async register(email, password) {
        try {
            const config = getAppwriteConfig();
            const client = new Appwrite.Client().setEndpoint(config.endpoint).setProject(config.projectId);
            const account = new Appwrite.Account(client);
            const databases = new Appwrite.Databases(client);

            // 1. Create user using exact v14 signature
            const user = await account.create(Appwrite.ID.unique(), email, password, email.split('@')[0]);

            // 2. Create profile document mapping the auth user.$id to your custom 'id' field
            try {
                await databases.createDocument(config.dbId, 'profiles', Appwrite.ID.unique(), {
                    id: user.$id, 
                    fullName: email.split('@')[0], 
                    displayName: email.split('@')[0], 
                    bio: 'New user', 
                    role: 'user'
                });
            } catch (e) { 
                console.warn("Profile creation failed (check required attributes):", e); 
            }

            // 3. Create session instantly so they are logged in
            await account.createEmailPasswordSession(email, password);

            // 4. Generate JWT for the UI token box
            let token = null;
            try {
                const jwtRes = await account.createJWT();
                token = jwtRes.jwt;
            } catch (e) { 
                console.warn("Could not generate JWT"); 
            }

            return { id: user.$id, email: user.email, token, status: 201 };
        } catch (error) {
            if (error.code === 429) return { error: 'Rate limit exceeded. Wait a minute and try again.', status: 429 };
            if (error.code === 409) return { error: 'An account with that email already exists', status: 409 };
            return { error: error.message || 'Failed to register', status: 400 };
        }
    },

    async login(email, password) {
        try {
            const config = getAppwriteConfig();
            const client = new Appwrite.Client().setEndpoint(config.endpoint).setProject(config.projectId);
            const account = new Appwrite.Account(client);

            try {
                await account.createEmailPasswordSession(email, password);
            } catch (e) {
                if (e.type === 'user_session_already_exists' || (e.message && e.message.includes('active'))) {
                    await account.deleteSession('current');
                    await account.createEmailPasswordSession(email, password);
                } else {
                    throw e;
                }
            }

            const user = await account.get();
            let token = null;
            try {
                const jwtRes = await account.createJWT();
                token = jwtRes.jwt;
            } catch (e) { 
                console.warn("Could not generate JWT"); 
            }

            return { id: user.$id, email: user.email, token, status: 200 };
        } catch (error) {
            return { error: error.message || 'Invalid email or password', status: (error.code === 401 ? 401 : 400) };
        }
    },

    async logout() {
        try {
            const config = getAppwriteConfig();
            const client = new Appwrite.Client().setEndpoint(config.endpoint).setProject(config.projectId);
            const account = new Appwrite.Account(client);
            
            await account.deleteSession('current');
            return { message: "Logged out", status: 200 };
        } catch (error) {
            if (error.code === 401 || (error.message && error.message.includes('guests'))) {
                return { message: "Already logged out", status: 200 };
            }
            return { error: error.message, status: 400 };
        }
    },

    async getMe() {
        try {
            const config = getAppwriteConfig();
            const client = new Appwrite.Client().setEndpoint(config.endpoint).setProject(config.projectId);
            const account = new Appwrite.Account(client);
            const databases = new Appwrite.Databases(client);
            
            const user = await account.get();
            let profile = {};
            
            // Search the profiles collection using your custom 'id' attribute
            try { 
                const res = await databases.listDocuments(config.dbId, 'profiles', [
                    Appwrite.Query.equal('id', user.$id)
                ]);
                if (res.documents.length > 0) {
                    profile = res.documents[0];
                }
            } catch(e){ 
                console.warn("Profile fetch failed:", e); 
            }
            
            return { id: user.$id, email: user.email, profile: profile, status: 200 };
        } catch (error) {
            return { error: "Not authenticated", status: 401 };
        }
    },

    async getFiles() {
        try {
            const config = getAppwriteConfig();
            const client = new Appwrite.Client().setEndpoint(config.endpoint).setProject(config.projectId);
            const account = new Appwrite.Account(client);
            const databases = new Appwrite.Databases(client);
            
            const user = await account.get();
            
            // Search the files collection using your custom 'ownerId' attribute
            const files = await databases.listDocuments(config.dbId, config.filesCollectionId, [
                Appwrite.Query.equal('ownerId', user.$id)
            ]);
            
            return { files: files.documents, status: 200 };
        } catch (error) {
            return { error: error.message, status: 400 };
        }
    },

    async getFileById(fileId) {
        try {
            const config = getAppwriteConfig();
            const client = new Appwrite.Client().setEndpoint(config.endpoint).setProject(config.projectId);
            const databases = new Appwrite.Databases(client);
            
            // Search the files collection using your custom 'id' attribute
            const res = await databases.listDocuments(config.dbId, config.filesCollectionId, [
                Appwrite.Query.equal('id', fileId)
            ]);
            
            if (res.documents.length === 0) {
                return { error: "File not found", status: 404 };
            }
            
            return { file: res.documents[0], status: 200 };
        } catch (error) {
            return { error: "File not found", status: 404 };
        }
    },

    async downloadFileById(fileId) {
        try {
            const config = getAppwriteConfig();
            const client = new Appwrite.Client().setEndpoint(config.endpoint).setProject(config.projectId);
            const databases = new Appwrite.Databases(client);
            
            // Search the files collection using your custom 'id' attribute
            const res = await databases.listDocuments(config.dbId, config.filesCollectionId, [
                Appwrite.Query.equal('id', fileId)
            ]);
            
            if (res.documents.length === 0) {
                return { error: "File not found", status: 404 };
            }
            
            const fileMeta = res.documents[0];
            const mockText = `This is a mock stand-in for "${fileMeta.fileName}" (${fileMeta.mimeType}, ${fileMeta.sizeBytes} bytes).`;
            
            return {
                blob: new Blob([mockText], { type: fileMeta.mimeType || 'text/plain' }),
                fileName: fileMeta.fileName
            };
        } catch (error) {
            return { error: "File not found", status: 404 };
        }
    }
};

// Helper to get config from HTML inputs
function getAppwriteConfig() {
    return {
        endpoint: document.getElementById('awEndpoint').value,
        projectId: document.getElementById('awProjectId').value,
        dbId: document.getElementById('awDatabaseId').value,
        filesCollectionId: document.getElementById('awFilesCollectionId').value,
    };
}

// 2. THE MAGIC TRICK: Intercept the global fetch() function
window.addEventListener('load', () => {
    const originalFetch = window.fetch;

    window.fetch = async function(url, options = {}) {
        const modeRadio = document.querySelector('input[name="backendMode"]:checked');
        const isAppwrite = modeRadio && modeRadio.value === 'appwrite';

        if (isAppwrite) {
            const config = getAppwriteConfig();
            if (typeof Appwrite === 'undefined' || !config.projectId || config.projectId === 'YOUR_PROJECT_ID') {
                return new Response(JSON.stringify({ error: 'Appwrite SDK missing/configured incorrectly.' }), { status: 500 });
            }
            
            // Normalize URL and method safely
            const urlString = url instanceof Request ? url.url : url.toString();
            const urlObj = new URL(urlString, window.location.href);
            const path = urlObj.pathname + (urlObj.search || '') + (urlObj.hash || '');
            
            let method = (options.method || 'GET').toString().toUpperCase();
            if (url instanceof Request && !options.method) method = url.method.toUpperCase();

            if (path === '/register' && method === 'POST') {
                const body = JSON.parse(options.body);
                const res = await appwriteAdapter.register(body.email, body.password);
                return new Response(JSON.stringify(res), { status: res.status, headers: {'Content-Type': 'application/json'} });
            }
            
            if (path === '/login' && method === 'POST') {
                const body = JSON.parse(options.body);
                const res = await appwriteAdapter.login(body.email, body.password);
                return new Response(JSON.stringify(res), { status: res.status, headers: {'Content-Type': 'application/json'} });
            }

            if (path === '/logout' && method === 'POST') {
                const res = await appwriteAdapter.logout();
                return new Response(JSON.stringify(res), { status: res.status, headers: {'Content-Type': 'application/json'} });
            }

            if (path === '/me' && method === 'GET') {
                const res = await appwriteAdapter.getMe();
                return new Response(JSON.stringify(res), { status: res.status, headers: {'Content-Type': 'application/json'} });
            }

            if (path === '/files' && method === 'GET') {
                const res = await appwriteAdapter.getFiles();
                return new Response(JSON.stringify(res), { status: res.status, headers: {'Content-Type': 'application/json'} });
            }

            const fileMatch = path.match(/^\/files\/([^/]+)(\/download)?$/);
            if (fileMatch) {
                const fileId = fileMatch[1];
                if (fileMatch[2]) { 
                    const res = await appwriteAdapter.downloadFileById(fileId);
                    if (res.error) return new Response(res.error, { status: res.status });
                    return new Response(res.blob, { status: 200, headers: {'Content-Type': res.blob.type} });
                } else { 
                    const res = await appwriteAdapter.getFileById(fileId);
                    return new Response(JSON.stringify(res), { status: res.status, headers: {'Content-Type': 'application/json'} });
                }
            }
        }
        return originalFetch.apply(this, arguments);
    };
});