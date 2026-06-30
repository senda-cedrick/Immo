# Documentation API - IMMO TRAVEL

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

## Authentification navigateur (sessions)

Pour les applications web, Django REST Framework propose une authentification par session :

**Login:** `POST /api-auth/login/`
**Logout:** `POST /api-auth/logout/`

## Endpoints disponibles

### Application de base (app_base)

Tous les endpoints sont préfixés par `/app/`

Consulter `app_base/urls.py` pour la liste complète.

### API pour Propriétaires (JWT)

Ces endpoints sont réservés aux utilisateurs avec le profil `Proprietaire`.

| Endpoint | Méthode | Description | Auth requise |
|----------|---------|-------------|--------------|
| `/app/api/proprietaire/dashboard/` | GET | Statistiques du dashboard propriétaire | JWT |
| `/app/api/proprietaire/proprietes/` | GET | Liste des propriétés du propriétaire | JWT |
| `/app/api/proprietaire/contrats/` | GET | Liste des contrats du propriétaire | JWT |

**Exemple d'utilisation:**
```bash
# Récupérer les statistiques du dashboard
curl http://localhost:8000/app/api/proprietaire/dashboard/ \
  -H "Authorization: Bearer <access_token>"

# Réponse:
{
  "nb_proprietes": 5,
  "nb_logements": 20,
  "nb_agences": 2,
  "nb_clients": 15,
  "nb_contrats_actifs": 12,
  "nb_contrats_non_signes": 3,
  "revenu_mensuel": "1500000",
  "taux_occupation": 75,
  "nb_paiements_retard": 2,
  "nb_contrats_expirant_30j": 4,
  "nb_paiements_total": 120
}

# Récupérer les propriétés
curl http://localhost:8000/app/api/proprietaire/proprietes/ \
  -H "Authorization: Bearer <access_token>"

# Récupérer les contrats
curl http://localhost:8000/app/api/proprietaire/contrats/ \
  -H "Authorization: Bearer <access_token>"
```

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

Consulter `app_paiements/urls.py` pour la liste complète.

### Gestion de caisse (app_caisse)

Tous les endpoints sont préfixés par `/caisses/`

Consulter `app_caisse/urls.py` pour la liste complète.

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

### 2. Ajouter les permissions dans `AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### 3. Créer les modèles de réponse JWT

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

// DashboardResponse.java
public class DashboardResponse {
    @SerializedName("nb_proprietes")
    private int nbProprietes;
    
    @SerializedName("nb_logements")
    private int nbLogements;
    
    @SerializedName("nb_agences")
    private int nbAgences;
    
    @SerializedName("nb_clients")
    private int nbClients;
    
    @SerializedName("nb_contrats_actifs")
    private int nbContratsActifs;
    
    @SerializedName("nb_contrats_non_signes")
    private int nbContratsNonSignes;
    
    @SerializedName("revenu_mensuel")
    private String revenuMensuel;
    
    @SerializedName("taux_occupation")
    private int tauxOccupation;
    
    @SerializedName("nb_paiements_retard")
    private int nbPaiementsRetard;
    
    @SerializedName("nb_contrats_expirant_30j")
    private int nbContratsExpirant30j;
    
    @SerializedName("nb_paiements_total")
    private int nbPaiementsTotal;
    
    // Getters
    public int getNbProprietes() { return nbProprietes; }
    public int getNbLogements() { return nbLogements; }
    public int getNbAgences() { return nbAgences; }
    public int getNbClients() { return nbClients; }
    public int getNbContratsActifs() { return nbContratsActifs; }
    public int getNbContratsNonSignes() { return nbContratsNonSignes; }
    public String getRevenuMensuel() { return revenuMensuel; }
    public int getTauxOccupation() { return tauxOccupation; }
    public int getNbPaiementsRetard() { return nbPaiementsRetard; }
    public int getNbContratsExpirant30j() { return nbContratsExpirant30j; }
    public int getNbPaiementsTotal() { return nbPaiementsTotal; }
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

### 4. Créer l'interface Retrofit

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
    
    @GET("app/api/proprietaire/dashboard/")
    Call<DashboardResponse> getDashboard(@Header("Authorization") String token);
    
    @GET("app/api/proprietaire/proprietes/")
    Call<List<ProprieteResponse>> getProprietes(@Header("Authorization") String token);
    
    @GET("app/api/proprietaire/contrats/")
    Call<List<ContratResponse>> getContrats(@Header("Authorization") String token);
}
```

### 5. Créer le singleton Retrofit

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

### 6. Créer un TokenManager pour gérer les tokens (SharedPreferences)

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

### 7. Exemple d'utilisation dans une Activity

```java
import android.os.Bundle;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ProprietaireDashboardActivity extends AppCompatActivity {
    
    private TokenManager tokenManager;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_proprietaire_dashboard);
        
        tokenManager = new TokenManager(this);
        loadDashboard();
    }
    
    private void loadDashboard() {
        String accessToken = tokenManager.getAccessToken();
        if (accessToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show();
            // Rediriger vers l'écran de login
            return;
        }
        
        String authHeader = "Bearer " + accessToken;
        Call<DashboardResponse> call = RetrofitClient.getApiService()
            .getDashboard(authHeader);
        
        call.enqueue(new Callback<DashboardResponse>() {
            @Override
            public void onResponse(Call<DashboardResponse> call, Response<DashboardResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    DashboardResponse data = response.body();
                    updateUI(data);
                } else if (response.code() == 401) {
                    refreshTokenAndRetry();
                } else {
                    Toast.makeText(ProprietaireDashboardActivity.this, 
                        "Erreur: " + response.code(), Toast.LENGTH_SHORT).show();
                }
            }
            
            @Override
            public void onFailure(Call<DashboardResponse> call, Throwable t) {
                Toast.makeText(ProprietaireDashboardActivity.this, 
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
                    loadDashboard(); // Réessayer la requête initiale
                } else {
                    tokenManager.clearTokens();
                    Toast.makeText(ProprietaireDashboardActivity.this, 
                        "Session expirée", Toast.LENGTH_SHORT).show();
                    // Rediriger vers l'écran de login
                }
            }
            
            @Override
            public void onFailure(Call<TokenResponse> call, Throwable t) {
                Toast.makeText(ProprietaireDashboardActivity.this, 
                    "Erreur réseau", Toast.LENGTH_SHORT).show();
            }
        });
    }
    
    private void updateUI(DashboardResponse data) {
        // Mettre à jour l'interface avec les données
        TextView tvProprietes = findViewById(R.id.tvProprietes);
        TextView tvLogements = findViewById(R.id.tvLogements);
        TextView tvAgences = findViewById(R.id.tvAgences);
        TextView tvClients = findViewById(R.id.tvClients);
        TextView tvRevenu = findViewById(R.id.tvRevenu);
        
        tvProprietes.setText(String.valueOf(data.getNbProprietes()));
        tvLogements.setText(String.valueOf(data.getNbLogements()));
        tvAgences.setText(String.valueOf(data.getNbAgences()));
        tvClients.setText(String.valueOf(data.getNbClients()));
        tvRevenu.setText(data.getRevenuMensuel() + " FC");
    }
}
```

### 8. Exemple de layout XML (activity_proprietaire_dashboard.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp">
    
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:spacing="16dp">
        
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Tableau de bord Propriétaire"
            android:textSize="24sp"
            android:textStyle="bold"
            android:layout_gravity="center"
            android:paddingBottom="16dp"/>
        
        <androidx.cardview.widget.CardView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginBottom="16dp"
            app:cardCornerRadius="8dp"
            app:cardElevation="4dp">
            
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="vertical"
                android:padding="16dp"
                android:spacing="12dp">
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Propriétés"/>
                    <TextView
                        android:id="@+id/tvProprietes"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Logements"/>
                    <TextView
                        android:id="@+id/tvLogements"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Agences"/>
                    <TextView
                        android:id="@+id/tvAgences"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Clients"/>
                    <TextView
                        android:id="@+id/tvClients"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Contrats actifs"/>
                    <TextView
                        android:id="@+id/tvContratsActifs"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Revenu mensuel"/>
                    <TextView
                        android:id="@+id/tvRevenu"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Taux d'occupation"/>
                    <TextView
                        android:id="@+id/tvTauxOccupation"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Paiements en retard"/>
                    <TextView
                        android:id="@+id/tvPaiementsRetard"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
                <Row
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="space_between">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Contrats expirant (30j)"/>
                    <TextView
                        android:id="@+id/tvContratsExpirant"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:textStyle="bold"/>
                </Row>
                
            </LinearLayout>
        </androidx.cardview.widget.CardView>
    </LinearLayout>
</ScrollView>
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