# Guide API Propriétaire - IMMO TRAVEL

## Table des matières
1. [Introduction](#introduction)
2. [Authentification](#authentification)
3. [Endpoints Propriétaires](#endpoints-propriétaires)
4. [Endpoints Généraux Utiles](#endpoints-généraux-utiles)
5. [Exemples d'Utilisation](#exemples-dutilisation)
6. [Intégration Android](#intégration-android)
7. [Gestion des Erreurs](#gestion-des-erreurs)
8. [Bonnes Pratiques](#bonnes-pratiques)

## Introduction

Ce guide fournit une documentation complète pour les développeurs travaillant avec l'API Propriétaire d'IMMO TRAVEL. L'API permet aux propriétaires de gérer leurs propriétés, contrats et accéder à des statistiques détaillées.

**Base URL:** `http://localhost:8000/`

## Authentification

L'API utilise **JWT (JSON Web Token)** via **SimpleJWT** pour l'authentification.

### 1. Obtenir un token JWT

**Endpoint:** `POST /api/token/`

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

### 2. Utilisation des tokens

Pour accéder aux endpoints protégés, inclure le token dans le header:
```
Authorization: Bearer <access_token>
```

## Endpoints Propriétaires

Ces endpoints sont réservés aux utilisateurs avec le profil **Proprietaire**.

### Dashboard Propriétaire

**Endpoint:** `GET /app/api/proprietaire/dashboard/`

**Description:** Statistiques complètes du dashboard propriétaire

**Auth requise:** JWT (Propriétaire)

**Réponse:**
```json
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
```

### Liste des Propriétés

**Endpoint:** `GET /app/api/proprietaire/proprietes/`

**Description:** Liste des propriétés appartenant au propriétaire connecté

**Auth requise:** JWT (Propriétaire)

### Liste des Contrats

**Endpoint:** `GET /app/api/proprietaire/contrats/`

**Description:** Liste des contrats associés aux propriétés du propriétaire

**Auth requise:** JWT (Propriétaire)

## Endpoints Généraux Utiles

### Liste des Propriétaires

**Endpoint:** `GET /app/proprietaires/`

**Description:** Liste de tous les propriétaires (accessible aux managers)

**Auth requise:** JWT

### Détails d'un Propriétaire

**Endpoint:** `GET /app/proprietaires/<int:pk>/`

**Description:** Détails spécifiques d'un propriétaire

**Auth requise:** JWT

### Liste des Logements

**Endpoint:** `GET /app/logements/`

**Description:** Liste de tous les logements

**Auth requise:** JWT

### Liste des Contrats

**Endpoint:** `GET /app/contrats/`

**Description:** Liste de tous les contrats

**Auth requise:** JWT

## Exemples d'Utilisation

### Récupérer les statistiques du dashboard

```bash
curl http://localhost:8000/app/api/proprietaire/dashboard/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

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
```

### Récupérer les propriétés du propriétaire

```bash
curl http://localhost:8000/app/api/proprietaire/proprietes/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Récupérer les contrats du propriétaire

```bash
curl http://localhost:8000/app/api/proprietaire/contrats/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

## Intégration Android

### Modèles de données

#### DashboardResponse.java
```java
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
```

### Interface Retrofit

```java
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

    @GET("app/proprietaires/")
    Call<List<ProprietaireResponse>> getProprietaires(@Header("Authorization") String token);

    @GET("app/proprietaires/{id}/")
    Call<ProprietaireResponse> getProprietaireDetails(@Header("Authorization") String token, @Path("id") int id);
}
```

### Exemple d'Activity Android

```java
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

    private void updateUI(DashboardResponse data) {
        TextView tvProprietes = findViewById(R.id.tvProprietes);
        TextView tvLogements = findViewById(R.id.tvLogements);
        TextView tvRevenu = findViewById(R.id.tvRevenu);

        tvProprietes.setText(String.valueOf(data.getNbProprietes()));
        tvLogements.setText(String.valueOf(data.getNbLogements()));
        tvRevenu.setText(data.getRevenuMensuel() + " FC");
    }

    private void refreshTokenAndRetry() {
        String refreshToken = tokenManager.getRefreshToken();
        if (refreshToken == null) {
            Toast.makeText(this, "Session expirée", Toast.LENGTH_SHORT).show();
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
                    loadDashboard();
                } else {
                    tokenManager.clearTokens();
                    Toast.makeText(ProprietaireDashboardActivity.this,
                        "Session expirée", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<TokenResponse> call, Throwable t) {
                Toast.makeText(ProprietaireDashboardActivity.this,
                    "Erreur réseau", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
```

## Gestion des Erreurs

### Codes de réponse HTTP

| Code | Description |
|------|-------------|
| 200 | OK - Requête réussie |
| 201 | Created - Ressource créée |
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - Token manquant ou invalide |
| 403 | Forbidden - Permissions insuffisantes |
| 404 | Not Found - Ressource non trouvée |
| 500 | Internal Server Error - Erreur serveur |

### Gestion des erreurs 401

Lorsque vous recevez une erreur 401 (Unauthorized), suivez ce processus:

1. Vérifiez si vous avez un refresh token valide
2. Appelez `/api/token/refresh/` pour obtenir un nouveau access token
3. Réessayez la requête originale avec le nouveau token
4. Si le refresh échoue, redirigez l'utilisateur vers l'écran de connexion

## Bonnes Pratiques

1. **Sécurité des tokens:**
   - Ne jamais stocker les tokens en clair dans le code source
   - Utiliser des mécanismes sécurisés comme SharedPreferences avec chiffrement
   - Toujours utiliser HTTPS en production

2. **Gestion de session:**
   - Implémenter un mécanisme de rafraîchissement automatique des tokens
   - Déconnecter l'utilisateur après plusieurs échecs d'authentification

3. **Performance:**
   - Mettre en cache les données lorsque possible
   - Utiliser la pagination pour les listes de données volumineuses

4. **Gestion des erreurs:**
   - Toujours afficher des messages d'erreur conviviaux à l'utilisateur
   - Logger les erreurs pour le débogage

5. **Tests:**
   - Tester avec différents scénarios d'authentification
   - Vérifier les permissions et rôles d'accès

## Support

Pour toute question ou problème technique, contacter l'équipe de développement d'IMMO TRAVEL.