## CryptoDrink

**CryptoDrink** est un bot Discord implémentant un tableau des
scores local pour [https://cryptohack.org/](CryptoHack).

 - Annonce lorsqu'un membre du tableau des scores résout un
   challenge
 - Affichage des statistiques d'un utilisateur CryptoHack
 - Tableau des scores
 - Liste des membres ayant résolu un challenge

## Installation

### NixOS

```bash
git clone https://github.com/PoustouFlan/Crypto-Drink.git
cd Crypto-Drink
```
Ensuite, modifier le fichier `configuration.yaml`, qui doit
ressembler à :
```yaml
token:      "LeTokenDe.Votre.Bot_Ici"
guild_id:   123456789012345678
channel_id: 1234567890123456789
```
en remplaçant la valeur de `guild_id` par l'identifiant de votre serveur,
et `channel_id` par l'identifiant du salon des annonces.

Enfin, pour lancer le bot, vous pouvez exécuter :
```bash
nix-shell --run make
```

Le bot aura besoin des permissions pour voir les messages, envoyer les
messages et inclure des embeds. Aussi, il faut avoir actif le *Message Intent.*
