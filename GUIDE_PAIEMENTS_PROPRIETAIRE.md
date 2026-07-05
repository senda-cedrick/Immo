# Guide API Paiements Propriétaire - IMMO TRAVEL

## Table des matières
1. [Introduction](#introduction)
2. [Fonctionnement des Paiements pour Propriétaires](#fonctionnement-des-paiements-pour-propriétaires)
3. [Endpoints de Paiement](#endpoints-de-paiement)
4. [Exemples d'Utilisation](#exemples-dutilisation)
5. [Structure des Données](#structure-des-données)
6. [Gestion des Erreurs](#gestion-des-erreurs)
7. [Bonnes Pratiques](#bonnes-pratiques)

## Introduction

Ce guide explique comment les propriétaires peuvent utiliser l'API de paiements d'IMMO TRAVEL pour gérer les paiements liés à leurs propriétés et contrats.

**Base URL:** `http://localhost:8000/`

## Fonctionnement des Paiements pour Propriétaires

### Filtrage Automatique

L'API utilise un système de filtrage intelligent basé sur le profil utilisateur :

1. **Authentification requise** : Tous les endpoints de paiement nécessitent une authentification JWT
2. **Filtrage par profil** : Lorsque un propriétaire se connecte, le système filtre automatiquement les paiements pour ne montrer que ceux liés à ses propriétés
3. **Logique de filtrage** :
   - Le système identifie les propriétés appartenant au propriétaire
   - Il trouve tous les contrats associés à ces propriétés
   - Il retourne uniquement les paiements liés à ces contrats

### Processus de Filtrage

```mermaid
graph TD
    A[Propriétaire connecté] --> B[Identification des propriétés]
    B --> C[Trouver les contrats liés]
    C --> D[Filtrer les paiements par contrats]
    D --> E[Retourner les paiements filtrés]
```

## Endpoints de Paiement

### Liste des Paiements

**Endpoint:** `GET /paiements/`

**Description:** Liste des paiements filtrés pour le propriétaire connecté

**Auth requise:** JWT (Propriétaire)

**Paramètres optionnels:**
- `statut` : Filtrer par statut (ex: `?statut=PAYE,EN_ATTENTE`)
- `non_retard` : Filtrer les paiements non en retard
- `en_retard` : Filtrer les paiements en retard

**Exemple de réponse:**
```json
[
  {
    "id": 123,
    "contrat": 456,
    "contrat_info": "Contrat #456 - Appartement Lumière",
    "client_noms": "Jean Dupont",
    "montant": "150000",
    "date_paiement": "2023-10-15",
    "date_echeance": "2023-10-10",
    "mode_paiement": "MOBILE_MONEY",
    "reference": "REF202310001",
    "statut": "PAYE",
    "penalites": "0",
    "situation": "A_JOUR",
    "detail": "Paiement loyer octobre 2023",
    "created_at": "2023-10-15T08:30:00Z",
    "updated_at": "2023-10-15T08:30:00Z"
  },
  {
    "id": 124,
    "contrat": 457,
    "contrat_info": "Contrat #457 - Maison Soleil",
    "client_noms": "Marie Martin",
    "montant": "200000",
    "date_paiement": null,
    "date_echeance": "2023-10-12",
    "mode_paiement": "ESPECES",
    "reference": "",
    "statut": "EN_ATTENTE",
    "penalites": "20000",
    "situation": "EN_RETARD",
    "detail": "Paiement loyer octobre 2023 - En retard",
    "created_at": "2023-10-01T09:00:00Z",
    "updated_at": "2023-10-13T14:20:00Z"
  }
]
```

### Détails d'un Paiement

**Endpoint:** `GET /paiements/{id}/`

**Description:** Détails complets d'un paiement spécifique

**Auth requise:** JWT (Propriétaire)

**Note:** Le propriétaire ne peut accéder qu'aux paiements liés à ses propriétés

### Ajouter un Paiement

**Endpoint:** `POST /paiements/ajouter/`

**Description:** Ajouter un nouveau paiement

**Auth requise:** JWT (Propriétaire)

**Body:**
```json
{
  "contrat": 456,
  "client": 789,
  "agent": 101,
  "montant": "150000",
  "type_paiement": "LOYER",
  "date_paiement": "2023-10-15",
  "date_echeance": "2023-10-10",
  "statut": "PAYE",
  "notes": "Paiement reçu en espèces"
}
```

### Modifier un Paiement

**Endpoint:** `POST /paiements/{id}/modifier/`

**Description:** Modifier un paiement existant

**Auth requise:** JWT (Propriétaire)

**Note:** Le propriétaire ne peut modifier que les paiements liés à ses propriétés

### Supprimer un Paiement

**Endpoint:** `POST /paiements/{id}/supprimer/`

**Description:** Supprimer un paiement

**Auth requise:** JWT (Propriétaire)

**Note:** Le propriétaire ne peut supprimer que les paiements liés à ses propriétés

## Exemples d'Utilisation

### Récupérer tous les paiements du propriétaire

```bash
curl http://localhost:8000/paiements/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json"
```

### Récupérer les paiements en retard

```bash
curl "http://localhost:8000/paiements/?en_retard=true" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json"
```

### Récupérer les détails d'un paiement spécifique

```bash
curl http://localhost:8000/paiements/123/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json"
```

### Ajouter un nouveau paiement

```bash
curl -X POST http://localhost:8000/paiements/ajouter/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "contrat": 456,
    "client": 789,
    "agent": 101,
    "montant": "150000",
    "type_paiement": "LOYER",
    "date_paiement": "2023-10-15",
    "date_echeance": "2023-10-10",
    "statut": "PAYE",
    "notes": "Paiement reçu en espèces"
  }'
```

## Structure des Données

### PaiementSerializer

Le serializer de paiement inclut les champs suivants :

```json
{
  "id": "integer",
  "contrat": "integer",
  "contrat_info": "string (read-only)",
  "client_noms": "string (read-only)",
  "montant": "string",
  "date_paiement": "date",
  "date_echeance": "date",
  "mode_paiement": "string",
  "reference": "string",
  "statut": "string",
  "penalites": "string",
  "date_regularisation": "date",
  "situation": "string",
  "detail": "string",
  "created_at": "datetime (read-only)",
  "updated_at": "datetime (read-only)"
}
```

### Statuts de Paiement

| Statut | Description |
|--------|-------------|
| `PAYE` | Paiement effectué |
| `EN_ATTENTE` | Paiement attendu |
| `EN_RETARD` | Paiement en retard |
| `ANNULE` | Paiement annulé |
| `PARTIEL` | Paiement partiel |

### Situations de Paiement

| Situation | Description |
|-----------|-------------|
| `A_JOUR` | Paiement à jour |
| `EN_RETARD` | Paiement en retard |
| `REGULARISE` | Paiement regularisé |

## Gestion des Erreurs

### Codes de réponse HTTP

| Code | Description | Solution |
|------|-------------|----------|
| 200 | OK | Requête réussie |
| 201 | Created | Ressource créée avec succès |
| 400 | Bad Request | Données invalides | Vérifier le format des données envoyées |
| 401 | Unauthorized | Token manquant ou invalide | Rafraîchir le token ou se reconnecter |
| 403 | Forbidden | Accès refusé | Vérifier que l'utilisateur est propriétaire |
| 404 | Not Found | Ressource non trouvée | Vérifier l'ID du paiement |
| 405 | Method Not Allowed | Méthode HTTP incorrecte | Utiliser la méthode correcte (GET/POST) |

### Erreurs Courantes

1. **403 Forbidden sur un paiement** :
   - Cause : Le propriétaire essaie d'accéder à un paiement qui ne lui appartient pas
   - Solution : Vérifier que le paiement est bien lié à une propriété du propriétaire

2. **400 Bad Request lors de la création** :
   - Cause : Données manquantes ou invalides
   - Solution : Vérifier que tous les champs requis sont présents

## Bonnes Pratiques

### Sécurité

1. **Gestion des tokens** :
   - Toujours utiliser HTTPS en production
   - Ne jamais stocker les tokens en clair
   - Implémenter le rafraîchissement automatique des tokens

2. **Validation des données** :
   - Valider les montants avant envoi
   - Vérifier les dates de paiement et d'échéance

### Performance

1. **Filtrage efficace** :
   - Utiliser les paramètres de filtrage (`statut`, `en_retard`) pour réduire la taille des réponses
   - Implémenter la pagination côté client pour les grandes listes

2. **Mise en cache** :
   - Mettre en cache les listes de paiements lorsque possible
   - Rafraîchir le cache après les opérations de modification

### Expérience Utilisateur

1. **Notifications** :
   - Notifier le propriétaire des paiements en retard
   - Envoyer des rappels avant les dates d'échéance

2. **Historique** :
   - Conserver un historique des modifications des paiements
   - Afficher les changements de statut

## Intégration Android

### Exemple de Modèle de Données

```java
public class PaiementResponse {
    @SerializedName("id")
    private int id;

    @SerializedName("contrat")
    private int contratId;

    @SerializedName("contrat_info")
    private String contratInfo;

    @SerializedName("client_noms")
    private String clientNoms;

    @SerializedName("montant")
    private String montant;

    @SerializedName("date_paiement")
    private String datePaiement;

    @SerializedName("date_echeance")
    private String dateEcheance;

    @SerializedName("mode_paiement")
    private String modePaiement;

    @SerializedName("statut")
    private String statut;

    @SerializedName("situation")
    private String situation;

    @SerializedName("detail")
    private String detail;

    // Getters et setters
    public int getId() { return id; }
    public int getContratId() { return contratId; }
    public String getContratInfo() { return contratInfo; }
    public String getClientNoms() { return clientNoms; }
    public String getMontant() { return montant; }
    public String getDatePaiement() { return datePaiement; }
    public String getDateEcheance() { return dateEcheance; }
    public String getModePaiement() { return modePaiement; }
    public String getStatut() { return statut; }
    public String getSituation() { return situation; }
    public String getDetail() { return detail; }
}
```

### Exemple d'Interface Retrofit

```java
public interface ApiService {
    @GET("paiements/")
    Call<List<PaiementResponse>> getPaiementsProprietaire(
        @Header("Authorization") String token,
        @Query("statut") String statut,
        @Query("en_retard") Boolean enRetard
    );

    @GET("paiements/{id}/")
    Call<PaiementResponse> getPaiementDetail(
        @Header("Authorization") String token,
        @Path("id") int paiementId
    );

    @POST("paiements/ajouter/")
    Call<PaiementResponse> ajouterPaiement(
        @Header("Authorization") String token,
        @Body PaiementRequest paiementRequest
    );
}
```

## Support

Pour toute question ou problème technique concernant l'API de paiements pour propriétaires, contacter l'équipe de développement d'IMMO TRAVEL.