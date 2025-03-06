# IBM ACE Prometheus Exporter

## Description
Ce projet est un exporter Prometheus pour IBM App Connect Enterprise (ACE). Il collecte des métriques sur les serveurs d'intégration, les applications et les flux de messages d'ACE, et les expose via un endpoint HTTP pour être scrapées par Prometheus.

## Fonctionnalités
- Collecte de métriques des serveurs ACE, applications et flux de messages
- Exposition des métriques au format Prometheus
- Mise à jour parallélisée des métriques pour une meilleure performance
- Authentification Basic Auth pour l'API ACE
- Logging des opérations avec horodatage

## Prérequis
- Python 3.9+
- Accès à l'API d'administration d'IBM ACE

## Installation
1. Clonez le dépôt :

```Shell
git clone https://github.com/votre-username/ibm-ace-prometheus-exporter.git
cd ibm-ace-prometheus-exporter
```

2. Créez un environnement virtuel et activez-le :

```Shell
python3 -m venv venv
source venv/bin/activate 
```

3. Installez les dépendances :

```Shell
pip install -r requirements.txt
```

## Configuration
Définissez les variables d'environnement suivantes :

```Shell
export ACE_USERNAME=votre_nom_utilisateur # Nom d'utilisateur pour l'authentification à l'API ACE
export ACE_PASSWORD=votre_mot_de_passe # Mot de passe pour l'authentification à l'API ACE
export ACE_URL=https://localhost:4414 # URL pour l'API ACE
```

## Utilisation
Exécutez le script principal :

```Shell
python3 src/ace_exporter.py
```

L'exporter sera accessible sur `http://localhost:8000/metrics`.

## Docker
Pour exécuter l'exporter dans un conteneur Docker :

1. Construisez l'image :

```Shell
docker build -t ace-exporter .
```

2. Exécutez le conteneur :

```Shell
docker run -p 8000:8000 -e ACE_USERNAME=votre_username -e ACE_PASSWORD=votre_password -e ACE_URL=votre_url ace-exporter
```

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
