# Display Switch

Display Switch est un petit utilitaire Windows 11 écrit en Python et PySide6. Il désactive ou réactive un écran secondaire dans la configuration d'affichage Windows, en conservant l'écran principal configuré.

Le projet reste volontairement simple : des fonctions pour les appels Windows, un fichier JSON pour les noms des écrans et une fenêtre Qt pour les commandes.

## Usage prévu

La configuration testée utilise deux écrans sur un PC fixe :

- MSI MAG342CQR, 34 pouces, 3440 × 1440 : principal à conserver actif.
- MAG321CURV, 32 pouces, 3840 × 2160 : secondaire à désactiver pour le télétravail.

Le 32 pouces est également branché au laptop professionnel. Le désactiver côté PC fixe retire cet écran du bureau actif de ce PC. Cela permet d'utiliser le moniteur avec le laptop sans laisser une partie du bureau du PC fixe sur cet écran.

L'application ne commande ni l'alimentation du moniteur ni sa source HDMI/DisplayPort. Le changement de source dépend du moniteur ou d'une action manuelle.

## État de la V1

Les fonctionnalités suivantes ont été testées manuellement sur la configuration ci-dessus :

- Détection des écrans actifs et des écrans inactifs encore disponibles pour Windows.
- Affichage des noms, chemins de périphérique, résolutions courantes et rôle principal.
- Désactivation du secondaire avec maintien du principal.
- Réactivation du bureau étendu avec retour à la disposition précédente sur cette machine.
- Interface Télétravail / Personnel et affichage des résultats.
- Configuration du mode Télétravail depuis l'interface, après un changement de principal dans Windows.
- Refus de la bascule si le principal Windows ne correspond plus aux réglages enregistrés.
- Exécutable Windows sans console.

Ces tests matériels ne constituent pas une garantie de comportement identique avec tous les pilotes ou d'autres topologies d'affichage.

## Prérequis

- Windows 11 et une session de bureau locale disposant des écrans à piloter.
- Python 3 pour le développement. Version utilisée : Python 3.14.7, 64 bits.
- PySide6 6.11.2, fixé dans `requirements.txt`.
- PyInstaller pour construire l'exécutable. Version installée dans l'environnement du projet lors de la documentation : 6.22.3.

Le moteur utilise `ctypes`, inclus dans Python, pour appeler les API Windows. Il ne dépend pas de MultiMonitorTool, de pywin32, d'un serveur ou d'une base de données.

## Installation pour le développement

Ouvrir PowerShell dans le dossier du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si `.venv` existe déjà, ne pas le recréer : l'activer suffit avant l'installation des dépendances.

L'activation fait utiliser le Python de ce projet dans le terminal courant. Il est aussi possible d'appeler directement `.\.venv\Scripts\python.exe` sans activer l'environnement.

Pour vérifier les versions :

```powershell
python --version
python -c "import PySide6; print(PySide6.__version__)"
```

`python -v` active les traces des imports ; pour afficher la version, utiliser `--version` ou `-V` avec un V majuscule.

## Configuration

Le fichier `config.json` contient les noms exacts renvoyés par Windows :

```json
{
  "primary_monitor": "MSI MAG342CQR",
  "secondary_monitor": "MAG321CURV"
}
```

`primary_monitor` désigne l'écran qui doit déjà être actif et principal dans Windows. Le programme ne lui attribue pas automatiquement ce rôle avant une action.

`secondary_monitor` désigne l'écran à désactiver ou réactiver. Les noms sont comparés exactement, y compris les majuscules et les espaces. Utiliser `python main.py list` pour les relever.

La V1 sélectionne les écrans par leur nom. Elle affiche aussi leur chemin de périphérique, mais n'utilise pas encore ce chemin, l'EDID ou un numéro de série pour la sélection. Un nom absent ou plusieurs écrans portant le même nom provoquent un refus de l'action. Les numéros de cible et les identifiants locaux de carte graphique servent seulement à regrouper les résultats d'une lecture.

Pour changer les rôles habituels sans modifier le JSON manuellement :

1. Activer les deux écrans en bureau étendu dans les paramètres Windows.
2. Définir dans Windows l'écran principal à conserver pour le télétravail.
3. Ouvrir l'application et cliquer sur Configurer Télétravail…
4. Vérifier l'écran à conserver et l'écran à désactiver, puis cliquer sur Enregistrer.

La configuration reflète les rôles déjà définis dans Windows : elle ne change aucun écran ni son rôle. Annuler ou fermer la boîte de dialogue laisse le fichier intact. Le programme exige deux écrans disponibles et actifs, avec des noms distincts et un seul principal. Il relit les rôles avant l'enregistrement et refuse la sauvegarde s'ils ont changé pendant la confirmation. Le moteur n'a pas de modèle MSI codé en dur.

Si le principal est changé dans Windows sans actualiser les réglages Télétravail, la bascule est refusée. Cela protège l'écran configuré comme principal au lieu de changer automatiquement de cible.

En développement, le JSON est lu et enregistré à côté de `config.py`. Dans la version empaquetée, il est situé à côté de `DisplaySwitch.exe`. Le dossier courant du terminal n'intervient pas dans ce choix. Le JSON est relu à chaque action ; seul le bouton Enregistrer de la configuration le remplace.

La sauvegarde écrit d'abord un fichier temporaire dans le même dossier, puis remplace le JSON après écriture complète. Ce dossier doit donc être accessible en écriture. Une erreur est affichée si la sauvegarde est impossible. Le bouton Configurer Télétravail… peut aussi recréer une configuration absente ou remplacer un JSON invalide, puisqu'il part de la configuration Windows actuelle.

JSON n'accepte pas les commentaires `#` : les explications de ses clés restent donc dans ce README et dans `config.py`.

## Interface graphique

```powershell
python main.py
```

Sans argument, le programme ouvre la fenêtre :

- Télétravail appelle la désactivation du secondaire configuré.
- Personnel demande la réactivation du bureau étendu.
- Actualiser relit les écrans, notamment après un changement réalisé dans les paramètres Windows.
- Configurer Télétravail… propose d'enregistrer les rôles actuels de Windows pour les prochaines bascules.

L'état est actualisé au lancement et après chaque action. Il n'y a pas de surveillance permanente des branchements. Le résultat de la dernière action reste affiché séparément de l'état des écrans.

Les boutons sont désactivés pendant une action. Les appels Windows sont synchrones : la fenêtre peut rester brièvement occupée pendant la bascule. Fermer la fenêtre termine le programme ; il n'y a pas d'icône de notification ni de processus de surveillance prévu en arrière-plan.

## Commandes du terminal

Les commandes restent accessibles avec Python, indépendamment de la fenêtre :

```powershell
python main.py --help
python main.py list
python main.py check
python main.py disable
python main.py enable
```

| Commande | Comportement |
| --- | --- |
| `list` | Affiche les écrans disponibles, leur état et leur chemin Windows. Ne charge pas `config.json`. |
| `check` | Prépare la désactivation et demande sa validation à Windows sans appliquer de changement. Si le secondaire est déjà inactif, le signale directement. |
| `disable` | Valide puis applique la configuration sans le secondaire, et relit l'état obtenu. |
| `enable` | Demande la dernière configuration étendue de Windows, puis vérifie les deux écrans et le principal. |

Les commandes gérées renvoient le code de sortie 0 en cas de succès et 1 en cas d'erreur. `argparse` gère séparément les erreurs de syntaxe de la commande. Les erreurs attendues du moteur sont affichées sous la forme `Erreur : ...`.

L'exécutable est construit sans console et destiné à l'interface graphique. Pour les commandes et leurs sorties textuelles, utiliser `python main.py ...`.

## Contrôles avant et après une bascule

La désactivation retrouve les deux moniteurs par leur nom et vérifie qu'ils sont distincts. Elle exige que le principal configuré soit actif et situé en `(0, 0)` dans le bureau Windows. Elle refuse une duplication lorsque les deux chemins partagent le même mode source.

Elle construit ensuite une liste des chemins actifs en retirant uniquement le secondaire. La liste doit rester non vide et contenir le principal. Windows valide cette proposition avant son application. Après application, le moteur relit les écrans pour vérifier le principal et l'inactivité du secondaire.

La réactivation nécessite exactement deux cibles disponibles. Elle demande à Windows sa dernière topologie étendue mémorisée, puis vérifie que le secondaire est actif, que le principal configuré est conservé et que les deux écrans ne partagent pas le même mode source.

Si l'application ou la vérification de cette réactivation échoue, le moteur tente de remettre les chemins et modes actifs capturés juste avant l'appel. Cette sauvegarde est temporaire en mémoire : ce n'est pas une mémorisation persistante de toute la disposition. Si le retour arrière échoue aussi, les deux erreurs sont signalées. Un retour arrière accepté par Windows n'est pas suivi d'une nouvelle lecture dans le code actuel.

La désactivation ne possède pas de retour arrière automatique équivalent : une erreur de contrôle après son application est signalée, mais ne signifie pas qu'aucun changement n'a eu lieu. Un périphérique peut aussi devenir indisponible entre deux appels.

Le logiciel contrôle ce que Windows déclare actif. Il ne peut pas confirmer que le moniteur physique affiche effectivement l'entrée du PC plutôt que celle du laptop. La restauration exacte de la disposition repose sur Windows ; elle a été confirmée sur la machine de développement.

## Organisation du code

| Fichier | Rôle |
| --- | --- |
| `main.py` | Choix entre interface et CLI, analyse des arguments, erreurs et codes de sortie. |
| `config.py` | Localisation du JSON, lecture, validation et sauvegarde des valeurs. |
| `config.json` | Noms des deux moniteurs configurés. |
| `monitors.py` | Structures natives, signatures Windows, lecture, identification, désactivation et réactivation. |
| `ui/__init__.py` | Déclaration du paquet Python `ui`. |
| `ui/main_window.py` | Fenêtre, connexion des boutons au moteur et actualisation du bloc des écrans. |
| `ui/widgets.py` | Petits éléments de la fenêtre : rangée de deux boutons, ligne d'écran, point d'état. |
| `ui/config_dialog.py` | Boîte de confirmation « Configurer Télétravail ». |
| `ui/theme.py` | Couleurs, tailles, espacements et feuille de style Qt du design system. |
| `requirements.txt` | Dépendance graphique nécessaire au développement et à l'exécution Python. |
| `DisplaySwitch.spec` | Recette de construction PyInstaller, commentée. |
| `.gitignore` | Exclusion de l'environnement local, des caches et des sorties de construction. |

Les dossiers `.venv`, `__pycache__`, `build` et `dist` sont générés. Ils ne constituent pas le code source à maintenir ou à commenter.

## Comprendre le moteur Windows

Un chemin d'affichage relie une source de la carte graphique à une cible. La source décrit une surface du bureau ; la cible correspond à une sortie vers un moniteur. Un mode décrit les dimensions, la position ou les caractéristiques du signal. Il existe plusieurs chemins possibles pour un même écran, ce qui explique qu'une requête puisse retourner bien plus de chemins que de moniteurs.

Les classes `ctypes.Structure` décrivent le format mémoire des structures C attendues par Windows. Elles ne représentent pas une architecture orientée objet de l'application. `_fields_` fixe les champs et leur ordre ; `ctypes` calcule leur taille et leur alignement. Une `ctypes.Union` superpose plusieurs interprétations de la même zone mémoire, et le code doit vérifier le type avant de choisir l'interprétation.

Quelques expressions à reconnaître dans le code :

- `ctypes.c_uint32()` réserve un entier natif de 32 bits initialisé à zéro.
- `ctypes.byref(value)` transmet son adresse pour que Windows puisse le lire ou le remplir.
- `value.value` récupère la valeur d'un entier ctypes sous forme Python.
- `(Structure * count)()` réserve un tableau de `count` structures.
- `(Structure * len(items))(*items)` crée un tableau et le remplit avec les éléments d'une liste.
- `flags & option` teste un bit ; `option_a | option_b` combine des options.
- `is` compare l'identité de deux objets ; `==` compare leurs valeurs.
- `raise` interrompt le traitement avec une exception, que la CLI ou l'interface affiche.

La lecture suit ce parcours :

1. `get_buffer_sizes` demande les capacités nécessaires à Windows.
2. `query_displays` alloue les tableaux puis appelle `QueryDisplayConfig`. Elle peut recommencer jusqu'à trois fois si la capacité devient insuffisante.
3. `get_connected_displays` garde les cibles disponibles et regroupe les chemins, en privilégiant les actifs.
4. `get_monitor_identity` récupère le nom et le chemin Windows avec `DisplayConfigGetDeviceInfo`.
5. `get_displays` rassemble le nom, l'état, le rôle et la résolution de chaque écran. La fenêtre s'en sert directement ; `get_display_text` en fait le texte de la CLI.

Pour configurer Télétravail, `detect_telework_config` déduit les deux rôles des écrans actifs. La fenêtre présente cette proposition, la vérifie à nouveau après confirmation, puis appelle `save_config`. Ce parcours n'appelle jamais `SetDisplayConfig`.

Les chemins et leurs modes doivent provenir de la même requête : `modeInfoIdx` est un index dans ce tableau précis. Les chemins inactifs n'ont pas de résolution courante à lire.

Pour changer l'affichage, `SetDisplayConfig` est appelé avec `SDC_VALIDATE` pour tester et `SDC_APPLY` pour appliquer. Ces deux options s'utilisent dans deux appels distincts. Les fonctions natives renvoient un code d'état : 0 indique le succès, une autre valeur devient une exception `ctypes.WinError`.

Pour relire le projet, commencer par `main.py`, puis `config.py` et les fonctions de fin de `monitors.py`. Revenir ensuite aux structures du début selon les types rencontrés. Lire `ui/main_window.py` pour comprendre comment les mêmes fonctions sont appelées au clic.

## Construire l'exécutable

Fermer l'exécutable existant avant de le reconstruire. Dans l'environnement virtuel du projet, installer l'outil de construction :

```powershell
python -m pip install pyinstaller==6.22.3
```

Utiliser la recette versionnée pour conserver ses paramètres et ses commentaires :

```powershell
python -m PyInstaller --clean --noconfirm DisplaySwitch.spec
if (-not (Test-Path -LiteralPath .\dist\config.json)) {
    Copy-Item -LiteralPath .\config.json -Destination .\dist\config.json
}
```

`--clean` nettoie les fichiers temporaires de construction ; `--noconfirm` autorise le remplacement de la sortie précédente. La copie conditionnelle initialise le JSON distribué seulement s'il n'existe pas, afin de conserver les préférences déjà enregistrées depuis le `.exe`. Les réglages du projet et ceux de `dist` sont deux fichiers indépendants ; utiliser Configurer Télétravail… dans l'exécutable pour actualiser ses propres réglages.

Pour régénérer entièrement la recette à partir du point d'entrée, la commande initiale était :

```powershell
python -m PyInstaller --onefile --windowed --name DisplaySwitch main.py
```

Cette dernière commande peut réécrire `DisplaySwitch.spec` et perdre ses réglages. Préférer la construction depuis le `.spec` : il limite la recherche des DLL à Python et Windows pour éviter d'embarquer une bibliothèque incompatible provenant d'un autre outil installé (par exemple `icuuc.dll`). Ce réglage concerne seulement le processus de construction, pas le PATH permanent de Windows.

Le résultat à distribuer contient deux fichiers dans `dist` :

```text
DisplaySwitch.exe
config.json
```

Garder ces deux fichiers ensemble dans un dossier accessible en écriture et lancer le `.exe` par double-clic. Python et PySide6 sont embarqués : leur installation séparée n'est pas nécessaire sur la machine cible. Le format `onefile` extrait ses dépendances dans un dossier temporaire au démarrage ; le JSON externe reste à côté du `.exe` et demeure modifiable depuis l'interface.

Modifier les sources ne met pas à jour un exécutable déjà construit. Il faut le reconstruire pour diffuser une modification de code. Une modification du JSON externe est en revanche lue à la prochaine action.

## Vérifications manuelles

Les commandes de ce parcours modifient réellement l'affichage à partir de `disable` :

```powershell
python main.py list
python main.py check
python main.py disable
python main.py list
python main.py enable
python main.py list
```

Vérifier que le principal reste actif et principal, que le secondaire devient inactif puis actif, que le bureau étendu et la disposition reviennent, et que les fenêtres restent accessibles. Refaire le cycle avec les boutons puis avec l'exécutable lorsqu'une modification le justifie.

Pour vérifier le réglage Télétravail dans l'interface :

1. Avec les deux écrans actifs en extension, ouvrir Configurer Télétravail… et vérifier les noms proposés.
2. Annuler et vérifier que le JSON n'a pas changé ; rouvrir, enregistrer et vérifier le message de confirmation.
3. Avec un écran inactif, vérifier que la configuration est refusée, puis revenir en bureau étendu.
4. Pour tester l'inversion des rôles, changer le principal dans Windows. Avant de réenregistrer, Télétravail doit refuser l'ancienne configuration.
5. Enregistrer les nouveaux rôles via le bouton, puis tester Télétravail et Personnel.

Revenir à l'organisation habituelle dans Windows et la réenregistrer après ce test. La construction d'un nouvel exécutable ne remplace pas à elle seule ses préférences existantes.

Pour vérifier uniquement la syntaxe sans importer le moteur ni basculer d'écran :

```powershell
python -m py_compile main.py config.py monitors.py ui\__init__.py ui\main_window.py ui\widgets.py ui\config_dialog.py ui\theme.py DisplaySwitch.spec
```

Le projet ne contient pas actuellement de suite de tests automatisés du comportement matériel.

## Problèmes courants

- Moniteur introuvable : vérifier les noms avec `list`, le branchement et la disponibilité du moniteur dans Windows.
- Plusieurs moniteurs portent le même nom : la V1 refuse cette ambiguïté ; elle ne sait pas encore sélectionner par numéro de série ou chemin.
- Le principal configuré n'est pas principal : rétablir le rôle attendu dans Windows ou enregistrer la nouvelle organisation avec Configurer Télétravail…
- Écrans en duplication : passer en bureau étendu dans Windows avant d'utiliser les actions de cette V1.
- JSON introuvable dans l'exécutable : placer `config.json` à côté de `DisplaySwitch.exe` ou le créer avec Configurer Télétravail… avec les deux écrans actifs.
- Configuration impossible avec un écran inactif : réactiver le bureau étendu avant d'enregistrer les rôles.
- Sauvegarde refusée : vérifier les droits d'écriture du dossier contenant le `.exe` et le JSON.
- Erreur après une bascule : relire l'état avec Actualiser ou `list`. Une erreur n'implique pas que l'état d'avant l'action est encore présent ; les paramètres d'affichage Windows restent le moyen de remettre manuellement le bureau étendu.

## Évolutions envisagées

Le choix ponctuel de l'écran à désactiver et le changement automatique de principal restent hors périmètre : l'application sert la routine Télétravail et enregistre une organisation préparée dans Windows. L'icône de notification, les raccourcis, le démarrage automatique et le changement HDMI/DisplayPort ne sont pas implémentés.

## Références

- [QueryDisplayConfig](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-querydisplayconfig)
- [SetDisplayConfig](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setdisplayconfig)
- [DisplayConfigGetDeviceInfo](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-displayconfiggetdeviceinfo)
- [Première application Qt Widgets](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/widgets.html)
- [Localisation des fichiers avec PyInstaller](https://pyinstaller.org/en/stable/runtime-information.html)
