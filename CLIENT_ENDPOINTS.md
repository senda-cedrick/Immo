# Documentation API - IMMO TRAVEL (Client)

## Base URL
```
http://localhost:8000/
```

## Authentification

L'API utilise l'authentification **JWT (JSON Web Token)** via **SimpleJWT**.

### 1. Obtenir un token JWT

**Endpoint:** `POST /api/token/`

**Description:** Authentifie un utilisateur et retourne un couple de tokens (access + refresh).

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Réponse (200 OK):**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "user": "nom_utilisateur"
}
```

**Exemple curl:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Rafraîchir le token d'accès

**Endpoint:** `POST /api/token/refresh/`

**Description:** Utilise le refresh token pour obtenir un nouveau access token.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Réponse (200 OK):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Exemple curl:**
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "eyJhbGciOiJIUzI1NiIs..."}'
```

### 3. Vérifier un token

**Endpoint:** `POST /api/token/verify/`

**Description:** Vérifie si un token est valide.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Réponse (200 OK):**
```json
{}
```

**Réponse (401 Unauthorized):**
```json
{
    "detail": "Token is invalid or expired"
}
```

**Exemple curl:**
```bash
curl -X POST http://localhost:8000/api/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token": "eyJhbGciOiJIUzI1NiIs..."}'
```

## Utilisation des tokens

Pour accéder aux endpoints protégés, inclure le token dans le header:

```
Authorization: Bearer <access_token>
```

**Exemple:**
```bash
curl http://localhost:8000/app/endpoint_protege/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

## Endpoints disponibles pour les clients

### Application de base (app_base)

Tous les endpoints sont préfixés par `/app/`

| Endpoint | Méthode | Description | Auth requise |
|----------|---------|-------------|--------------|
| `/app/agences/` | GET | Liste des agences | JWT |
| `/app/proprietaires/` | GET | Liste des propriétaires | JWT |
| `/app/proprietaires/<int:pk>/` | GET | Détails d'un propriétaire | JWT |
| `/app/clients/` | GET | Liste des clients | JWT |
| `/app/clients/<int:pk>/` | GET | Détails d'un client | JWT |
| `/app/proprietes/` | GET | Liste des propriétés | JWT |
| `/app/proprietes/<int:pk>/` | GET | Détails d'une propriété | JWT |
| `/app/logements/` | GET | Liste des logements | JWT |
| `/app/logements/<int:pk>/` | GET | Détails d'un logement | JWT |
| `/app/type_proprietes/` | GET | Liste des types de propriété | JWT |
| `/app/type_proprietes/<int:pk>/` | GET | Détails d'un type de propriété | JWT |
| `/app/type_logements/` | GET | Liste des types de logement | JWT |
| `/app/type_logements/<int:pk>/` | GET | Détails d'un type de logement | JWT |
| `/app/contrats/` | GET | Liste des contrats | JWT |
| `/app/contrats/<int:pk>/` | GET | Détails d'un contrat | JWT |
| `/app/garanties/` | GET | Liste des garanties | JWT |
| `/app/garanties/<int:pk>/` | GET | Détails d'une garantie | JWT |
| `/app/maintenances/` | GET | Liste des maintenances | JWT |
| `/app/maintenances/<int:pk>/` | GET | Détails d'une maintenance | JWT |

### Gestion des utilisateurs (app_users)

Tous les endpoints sont préfixés par `/user/`

| Endpoint | Méthode | Description | Auth requise |
|----------|---------|-------------|--------------|
| `/user/login/` | GET/POST | Page de connexion web | Non |
| `/user/logout/` | GET | Déconnexion web | Oui |
| `/user/users/` | GET | Liste des utilisateurs | Oui |
| `/user/users/add/` | GET/POST | Ajouter un utilisateur | Oui (Manager) |
| `/user/users/edit/<int:pk>/` | GET/POST | Modifier un utilisateur | Oui (Manager) |
| `/user/users/delete/<int:pk>/` | POST | Supprimer un utilisateur | Oui (Manager) |
| `/user/login-remote/` | POST | Connexion distante via IP | Non |
| `/user/profiles/` | GET | Liste des profils | Oui (Manager) |

### Gestion des paiements (app_paiements)

Tous les endpoints sont préfixés par `/paiements/`

| Endpoint | Méthode | Description | Auth requise |
|----------|---------|-------------|--------------|
| `/paiements/` | GET | Liste des paiements | JWT |
| `/paiements/ajouter/` | GET/POST | Ajouter un paiement | JWT |
| `/paiements/<int:pk>/` | GET | Détails d'un paiement | JWT |
| `/paiements/<int:pk>/modifier/` | GET/POST | Modifier un paiement | JWT |
| `/paiements/<int:pk>/supprimer/` | POST | Supprimer un paiement | JWT |

### Gestion de caisse (app_caisse)

Tous les endpoints sont préfixés par `/caisses/`

| Endpoint | Méthode | Description | Auth requise |
|----------|---------|-------------|--------------|
| `/caisses/` | GET | Liste des caisses | JWT |
| `/caisses/ajouter/` | GET/POST | Ajouter une caisse | JWT |
| `/caisses/<int:pk>/modifier/` | GET/POST | Modifier une caisse | JWT |
| `/caisses/<int:pk>/supprimer/` | POST | Supprimer une caisse | JWT |

## Codes de réponse HTTP

| Code | Description |
|------|-------------|
| 200 | OK - Requête réussie |
| 201 | Created - Ressource créée |
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - Token manquant ou invalide |
| 403 | Forbidden - Permissions insuffisantes |
| 404 | Not Found - Ressource non trouvée |
| 500 | Internal Server Error - Erreur serveur |

## Structure des tokens JWT

### Access Token
- **Durée de vie:** Configurable dans `settings.py` (par défaut: variable)
- **Usage:** Accès aux endpoints protégés
- **Type:** Bearer token

### Refresh Token
- **Durée de vie:** Plus longue que l'access token
- **Usage:** Obtenir un nouvel access token sans se reconnecter
- **Stockage:** À conserver en toute sécurité

## Exemple d'intégration Android (Java)

### 1. Ajouter les dépendances dans `build.gradle` (Module: app)

```gradle
dependencies {
    // Retrofit pour les appels API
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'

    // OkHttp pour le logging
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'

    // Gson pour la sérialisation JSON
    implementation 'com.google.code.gson:gson:2.10.1'
}
```

## Exemple d'intégration Android (Kotlin)

### 1. Ajouter les dépendances dans `build.gradle` (Module: app)

```gradle
dependencies {
    // Retrofit pour les appels API
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'

    // OkHttp pour le logging
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'

    // Gson pour la sérialisation JSON
    implementation 'com.google.code.gson:gson:2.10.1'

    // Coroutines pour la programmation asynchrone
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4'
}
```

### 2. Ajouter les permissions dans `AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### 3. Créer les modèles de réponse JWT

#### En Java

```java
// TokenResponse.java
public class TokenResponse {
    @SerializedName("refresh")
    private String refresh;

    @SerializedName("access")
    private String access;

    @SerializedName("user")
    private String user;

    public TokenResponse(String refresh, String access, String user) {
        this.refresh = refresh;
        this.access = access;
        this.user = user;
    }

    public String getRefresh() { return refresh; }
    public String getAccess() { return access; }
    public String getUser() { return user; }
}

// LoginRequest.java
public class LoginRequest {
    @SerializedName("username")
    private String username;

    @SerializedName("password")
    private String password;

    public LoginRequest(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public String getUsername() { return username; }
    public String getPassword() { return password; }
}

// RefreshTokenRequest.java
public class RefreshTokenRequest {
    @SerializedName("refresh")
    private String refresh;

    public RefreshTokenRequest(String refresh) {
        this.refresh = refresh;
    }

    public String getRefresh() { return refresh; }
}
```

#### En Kotlin

```kotlin
// TokenResponse.kt
data class TokenResponse(
    @SerializedName("refresh") val refresh: String,
    @SerializedName("access") val access: String,
    @SerializedName("user") val user: String
)

// LoginRequest.kt
data class LoginRequest(
    @SerializedName("username") val username: String,
    @SerializedName("password") val password: String
)

// RefreshTokenRequest.kt
data class RefreshTokenRequest(
    @SerializedName("refresh") val refresh: String
)
```

### 4. Créer l'interface Retrofit

#### En Java

```java
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.POST;

public interface ApiService {

    @POST("api/token/")
    Call<TokenResponse> login(@Body LoginRequest request);

    @POST("api/token/refresh/")
    Call<TokenResponse> refreshToken(@Body RefreshTokenRequest request);

    @GET("app/agences/")
    Call<List<AgenceResponse>> getAgences(@Header("Authorization") String token);

    @GET("app/clients/")
    Call<List<ClientResponse>> getClients(@Header("Authorization") String token);

    @GET("app/proprietes/")
    Call<List<ProprieteResponse>> getProprietes(@Header("Authorization") String token);

    @GET("app/logements/")
    Call<List<LogementResponse>> getLogements(@Header("Authorization") String token);

    @GET("app/contrats/")
    Call<List<ContratResponse>> getContrats(@Header("Authorization") String token);
}
```

#### En Kotlin

```kotlin
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST

interface ApiService {

    @POST("api/token/")
    fun login(@Body request: LoginRequest): Call<TokenResponse>

    @POST("api/token/refresh/")
    fun refreshToken(@Body request: RefreshTokenRequest): Call<TokenResponse>

    @GET("app/agences/")
    fun getAgences(@Header("Authorization") token: String): Call<List<AgenceResponse>>

    @GET("app/clients/")
    fun getClients(@Header("Authorization") token: String): Call<List<ClientResponse>>

    @GET("app/proprietes/")
    fun getProprietes(@Header("Authorization") token: String): Call<List<ProprieteResponse>>

    @GET("app/logements/")
    fun getLogements(@Header("Authorization") token: String): Call<List<LogementResponse>>

    @GET("app/contrats/")
    fun getContrats(@Header("Authorization") token: String): Call<List<ContratResponse>>
}
```

### 5. Créer le singleton Retrofit

#### En Java

```java
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitClient {
    private static final String BASE_URL = "http://localhost:8000/";
    private static Retrofit retrofit = null;

    public static ApiService getApiService() {
        if (retrofit == null) {
            HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor();
            loggingInterceptor.setLevel(HttpLoggingInterceptor.Level.BODY);

            OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .addInterceptor(loggingInterceptor)
                .build();

            retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        }
        return retrofit.create(ApiService.class);
    }
}
```

#### En Kotlin

```kotlin
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    private const val BASE_URL = "http://localhost:8000/"
    private var retrofit: Retrofit? = null

    fun getApiService(): ApiService {
        if (retrofit == null) {
            val loggingInterceptor = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val okHttpClient = OkHttpClient.Builder()
                .addInterceptor(loggingInterceptor)
                .build()

            retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        }
        return retrofit!!.create(ApiService::class.java)
    }
}
```

### 6. Créer un TokenManager pour gérer les tokens (SharedPreferences)

#### En Java

```java
import android.content.Context;
import android.content.SharedPreferences;

public class TokenManager {
    private SharedPreferences prefs;
    private static final String PREF_NAME = "app_prefs";
    private static final String KEY_ACCESS_TOKEN = "access_token";
    private static final String KEY_REFRESH_TOKEN = "refresh_token";

    public TokenManager(Context context) {
        prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    public void saveTokens(String accessToken, String refreshToken) {
        prefs.edit()
            .putString(KEY_ACCESS_TOKEN, accessToken)
            .putString(KEY_REFRESH_TOKEN, refreshToken)
            .apply();
    }

    public String getAccessToken() {
        return prefs.getString(KEY_ACCESS_TOKEN, null);
    }

    public String getRefreshToken() {
        return prefs.getString(KEY_REFRESH_TOKEN, null);
    }

    public void clearTokens() {
        prefs.edit().clear().apply();
    }
}
```

#### En Kotlin

```kotlin
import android.content.Context
import android.content.SharedPreferences

class TokenManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)

    companion object {
        private const val KEY_ACCESS_TOKEN = "access_token"
        private const val KEY_REFRESH_TOKEN = "refresh_token"
    }

    fun saveTokens(accessToken: String, refreshToken: String) {
        prefs.edit()
            .putString(KEY_ACCESS_TOKEN, accessToken)
            .putString(KEY_REFRESH_TOKEN, refreshToken)
            .apply()
    }

    fun getAccessToken(): String? {
        return prefs.getString(KEY_ACCESS_TOKEN, null)
    }

    fun getRefreshToken(): String? {
        return prefs.getString(KEY_REFRESH_TOKEN, null)
    }

    fun clearTokens() {
        prefs.edit().clear().apply()
    }
}
```

### 7. Exemple d'utilisation dans une Activity

#### En Java

```java
import android.os.Bundle;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ClientDashboardActivity extends AppCompatActivity {

    private TokenManager tokenManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_client_dashboard);

        tokenManager = new TokenManager(this);
        loadClients();
    }

    private void loadClients() {
        String accessToken = tokenManager.getAccessToken();
        if (accessToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show();
            // Rediriger vers l'écran de login
            return;
        }

        String authHeader = "Bearer " + accessToken;
        Call<List<ClientResponse>> call = RetrofitClient.getApiService()
            .getClients(authHeader);

        call.enqueue(new Callback<List<ClientResponse>>() {
            @Override
            public void onResponse(Call<List<ClientResponse>> call, Response<List<ClientResponse>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    List<ClientResponse> clients = response.body();
                    updateUI(clients);
                } else if (response.code() == 401) {
                    refreshTokenAndRetry();
                } else {
                    Toast.makeText(ClientDashboardActivity.this,
                        "Erreur: " + response.code(), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<ClientResponse>> call, Throwable t) {
                Toast.makeText(ClientDashboardActivity.this,
                    "Erreur réseau: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void refreshTokenAndRetry() {
        String refreshToken = tokenManager.getRefreshToken();
        if (refreshToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show();
            // Rediriger vers l'écran de login
            return;
        }

        Call<TokenResponse> refreshCall = RetrofitClient.getApiService()
            .refreshToken(new RefreshTokenRequest(refreshToken));

        refreshCall.enqueue(new Callback<TokenResponse>() {
            @Override
            public void onResponse(Call<TokenResponse> call, Response<TokenResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    TokenResponse tokenResponse = response.body();
                    tokenManager.saveTokens(tokenResponse.getAccess(), tokenResponse.getRefresh());
                    loadClients(); // Réessayer la requête initiale
                } else {
                    tokenManager.clearTokens();
                    Toast.makeText(ClientDashboardActivity.this,
                        "Session expirée", Toast.LENGTH_SHORT).show();
                    // Rediriger vers l'écran de login
                }
            }

            @Override
            public void onFailure(Call<TokenResponse> call, Throwable t) {
                Toast.makeText(ClientDashboardActivity.this,
                    "Erreur réseau", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void updateUI(List<ClientResponse> clients) {
        // Mettre à jour l'interface avec les données des clients
        // Exemple: afficher la liste des clients dans un RecyclerView
    }
}
```

#### En Kotlin

```kotlin
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ClientDashboardActivity : AppCompatActivity() {

    private lateinit var tokenManager: TokenManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_client_dashboard)

        tokenManager = TokenManager(this)
        loadClients()
    }

    private fun loadClients() {
        val accessToken = tokenManager.getAccessToken()
        if (accessToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show()
            // Rediriger vers l'écran de login
            return
        }

        val authHeader = "Bearer $accessToken"
        val call = RetrofitClient.getApiService().getClients(authHeader)

        call.enqueue(object : Callback<List<ClientResponse>> {
            override fun onResponse(
                call: Call<List<ClientResponse>>,
                response: Response<List<ClientResponse>>
            ) {
                if (response.isSuccessful && response.body() != null) {
                    val clients = response.body()!!
                    updateUI(clients)
                } else if (response.code() == 401) {
                    refreshTokenAndRetry()
                } else {
                    Toast.makeText(
                        this@ClientDashboardActivity,
                        "Erreur: ${response.code()}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }

            override fun onFailure(call: Call<List<ClientResponse>>, t: Throwable) {
                Toast.makeText(
                    this@ClientDashboardActivity,
                    "Erreur réseau: ${t.message}",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }

    private fun refreshTokenAndRetry() {
        val refreshToken = tokenManager.getRefreshToken()
        if (refreshToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show()
            // Rediriger vers l'écran de login
            return
        }

        val refreshCall = RetrofitClient.getApiService().refreshToken(RefreshTokenRequest(refreshToken))

        refreshCall.enqueue(object : Callback<TokenResponse> {
            override fun onResponse(call: Call<TokenResponse>, response: Response<TokenResponse>) {
                if (response.isSuccessful && response.body() != null) {
                    val tokenResponse = response.body()!!
                    tokenManager.saveTokens(tokenResponse.access, tokenResponse.refresh)
                    loadClients() // Réessayer la requête initiale
                } else {
                    tokenManager.clearTokens()
                    Toast.makeText(
                        this@ClientDashboardActivity,
                        "Session expirée",
                        Toast.LENGTH_SHORT
                    ).show()
                    // Rediriger vers l'écran de login
                }
            }

            override fun onFailure(call: Call<TokenResponse>, t: Throwable) {
                Toast.makeText(
                    this@ClientDashboardActivity,
                    "Erreur réseau",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }

    private fun updateUI(clients: List<ClientResponse>) {
        // Mettre à jour l'interface avec les données des clients
        // Exemple: afficher la liste des clients dans un RecyclerView
    }
}
```

#### En Kotlin avec Coroutines

```kotlin
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ClientDashboardActivity : AppCompatActivity() {

    private lateinit var tokenManager: TokenManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_client_dashboard)

        tokenManager = TokenManager(this)
        loadClients()
    }

    private fun loadClients() {
        val accessToken = tokenManager.getAccessToken()
        if (accessToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show()
            // Rediriger vers l'écran de login
            return
        }

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val authHeader = "Bearer $accessToken"
                val response = RetrofitClient.getApiService().getClients(authHeader).execute()

                withContext(Dispatchers.Main) {
                    if (response.isSuccessful && response.body() != null) {
                        val clients = response.body()!!
                        updateUI(clients)
                    } else if (response.code() == 401) {
                        refreshTokenAndRetry()
                    } else {
                        Toast.makeText(
                            this@ClientDashboardActivity,
                            "Erreur: ${response.code()}",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    Toast.makeText(
                        this@ClientDashboardActivity,
                        "Erreur réseau: ${e.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }
    }

    private fun refreshTokenAndRetry() {
        val refreshToken = tokenManager.getRefreshToken()
        if (refreshToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show()
            // Rediriger vers l'écran de login
            return
        }

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val response = RetrofitClient.getApiService()
                    .refreshToken(RefreshTokenRequest(refreshToken))
                    .execute()

                withContext(Dispatchers.Main) {
                    if (response.isSuccessful && response.body() != null) {
                        val tokenResponse = response.body()!!
                        tokenManager.saveTokens(tokenResponse.access, tokenResponse.refresh)
                        loadClients() // Réessayer la requête initiale
                    } else {
                        tokenManager.clearTokens()
                        Toast.makeText(
                            this@ClientDashboardActivity,
                            "Session expirée",
                            Toast.LENGTH_SHORT
                        ).show()
                        // Rediriger vers l'écran de login
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    Toast.makeText(
                        this@ClientDashboardActivity,
                        "Erreur réseau",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }
    }

    private fun updateUI(clients: List<ClientResponse>) {
        // Mettre à jour l'interface avec les données des clients
        // Exemple: afficher la liste des clients dans un RecyclerView
    }
}
```

## Notes importantes

1. **CORS:** Configurer les origines autorisées dans `settings.py` si l'API est appelée depuis un domaine différent
2. **HTTPS:** En production, toujours utiliser HTTPS pour protéger les tokens
3. **Sécurité:** Ne jamais stocker les tokens en clair dans le code source
4. **Durée des tokens:** Configurer les durées de vie dans `settings.py` selon vos besoins
5. **Gestion des erreurs:** Toujours gérer les erreurs 401, 403 et 500 dans l'application mobile

## Tests avec Postman/Insomnia

1. **Créer une requête POST sur `/api/token/`**
2. **Body → raw → JSON:**
```json
{
    "username": "admin",
    "password": "admin123"
}
```
3. **Envoyer la requête**
4. **Copier le `access` token**
5. **Pour les requêtes suivantes, ajouter dans Headers:**
```
Key: Authorization
Value: Bearer <access_token>
```

## Support

Pour toute question, contacter l'équipe de développement.