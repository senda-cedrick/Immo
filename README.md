# Immo
## Réponse de l'API `/app/api/client/dashboard/`

### Structure Complète de la Réponse

```json
{
  "profil": {
    "id": 1,
    "noms": "Jean Dupont",
    "email": "jean@example.com",
    "telephone": "+243 123 456 789",
    "adresse": "123 Rue Principale, Kinshasa",
    "date_inscription": "2023-01-10"
  },
  "nb_contrats_actifs": 2,
  "paiements_payes": 15,
  "paiements_retard": 1,
  "montant_du": 150000,
  "paiements_a_venir": 3,
  "montant_retard": 50000,
  "taux_paiements_a_jour": 94,
  "contrats_proches_expiration": 1,
  "paiements_prochains": [
    {
      "id": 123,
      "contrat_reference": "CONT-2026-001",
      "type_paiement": "Loyer",
      "montant": "75000",
      "date_echeance": "2026-06-15",
      "statut": "EN_ATTENTE"
    },
    {
      "id": 124,
      "contrat_reference": "CONT-2026-002",
      "type_paiement": "Charges",
      "montant": "25000",
      "date_echeance": "2026-06-20",
      "statut": "EN_ATTENTE"
    }
  ]
}
```

### Explication des Champs

| Champ | Type | Description |
|-------|------|-------------|
| `profil` | Object | Informations personnelles du client |
| `nb_contrats_actifs` | Integer | Nombre de contrats actifs |
| `paiements_payes` | Integer | Nombre total de paiements effectués |
| `paiements_retard` | Integer | Nombre de paiements en retard |
| `montant_du` | Number | Montant total dû (en devise) |
| `paiements_a_venir` | Integer | Paiements à venir (non en retard) |
| `montant_retard` | Number | Montant total des paiements en retard |
| `taux_paiements_a_jour` | Integer | Pourcentage de paiements à jour (0-100) |
| `contrats_proches_expiration` | Integer | Contrats expirant dans 30 jours |
| `paiements_prochains` | Array | Liste des paiements à venir |

### Exemple d'Utilisation

```python
import requests

# Obtenir le token
auth = requests.post(
    "http://localhost:8000/app/api/token/",
    json={"email": "client@example.com", "password": "password"}
)
token = auth.json()['access']

# Appeler l'API dashboard
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/app/api/client/dashboard/",
    headers=headers
)

# Afficher la réponse
print("Status:", response.status_code)
print("Profil:", response.json()['profil'])
print("Contrats actifs:", response.json()['nb_contrats_actifs'])
print("Paiements payés:", response.json()['paiements_payes'])
print("Taux de conformité:", response.json()['taux_paiements_a_jour'] + "%")
```

### Points Clés

✅ **Données complètes** : Profil + statistiques + paiements
✅ **Format standard** : JSON structuré et lisible
✅ **Prêt pour mobile** : Structure idéale pour applications mobiles

Cette réponse fournit toutes les informations nécessaires pour une interface client complète.