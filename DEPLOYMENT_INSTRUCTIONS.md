# Deployment og GitHub Tilgangsinstruksjoner

## Problemet
Det ser ut som GitHub-brukeren "GmailHelene" ikke har skrivetilgang til repositoriet "GmailHelene/aksjeradarv2". 

## Løsningsalternativer

### Alternativ 1: Sjekk repository-tilgangene
1. Gå til GitHub-repositoriet: https://github.com/GmailHelene/aksjeradarv2
2. Gå til "Settings" > "Collaborators and teams"
3. Sjekk at din GitHub-bruker har skrivetilgang ("Write" access)

### Alternativ 2: Bruk personlig tilgangstoken (PAT)
1. Gå til GitHub.com og logg inn
2. Klikk på profilbildet ditt (øverst til høyre) > Settings
3. Bla ned til "Developer settings" (helt nederst i menyen til venstre)
4. Klikk på "Personal access tokens" > "Tokens (classic)"
5. Klikk "Generate new token" > "Generate new token (classic)"
6. Gi tokenet et navn, f.eks. "Aksjeradar deployment"
7. Velg følgende tilganger:
   - repo (alle underpunkter)
   - workflow
8. Klikk "Generate token"
9. Kopier tokenet (du får bare se det én gang)
10. Kjør følgende kommando i terminalen:
    ```
    git remote set-url origin https://DITT_BRUKERNAVN:DITT_TOKEN@github.com/GmailHelene/aksjeradarv2.git
    ```
11. Prøv å pushe igjen:
    ```
    git push
    ```

### Alternativ 3: Opprett et nytt repository
Hvis du eier koden og vil lage et nytt repository:
1. Gå til GitHub.com og logg inn
2. Klikk på "+" i øvre høyre hjørne > "New repository"
3. Opprett et nytt repository med navnet "aksjeradar"
4. Følg instruksjonene for å pushe et eksisterende repository

### Alternativ 4: Midlertidig løsning - Eksporter koden
Hvis du trenger en kopi av alle endringene:
```bash
# Lag en zip-fil av hele prosjektet
cd /workspaces
zip -r aksjeradar.zip aksjeradar
# Last ned zip-filen og last den opp til GitHub manuelt
```

## Hvordan pushe endringer etter at dette er løst
```bash
git add .
git commit -m "Lagt til personvernerklæring for Google Play Store og fikset styling på navbar/footer"
git push
```
