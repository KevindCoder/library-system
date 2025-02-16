# Projekti i Sistemit të Bibliotekës

Ky projekt është një sistem i thjeshtë menaxhimi i bibliotekës, i krijuar për të menaxhuar librat, huazimet, lexuesit dhe gjoba. Projekti përdor PostgreSQL si bazë të të dhënave dhe Python për logjikën e aplikacionit.

## Përmbajtja

- [Instalimi i PostgreSQL në WSL](#instalimi-i-postgresql-në-wsl)
- [Krijimi i Skemës library_system](#krijimi-i-skëmës-library_system)
- [Instalimi i JupyterLab](#instalimi-i-jupyterlab)
- [Nisja e JupyterLab](#nisja-e-jupyterlab)
- [Përdorimi i Projektit](#përdorimi-i-projektit)

## Instalimi i PostgreSQL në WSL

1. Përditësoni sistemin:

    ```bash
    sudo apt update
    sudo apt upgrade
    ```

2. Instaloni PostgreSQL:

    ```bash
    sudo apt install postgresql postgresql-contrib
    ```

3. Nisni shërbimin PostgreSQL:

    ```bash
    sudo service postgresql start
    ```

4. Hyni në PostgreSQL si përdoruesi postgres:

    ```bash
    sudo -u postgres psql
    ```

5. Krijo një përdorues të ri dhe një bazë të dhënash:

    ```sql
    CREATE USER username WITH PASSWORD 'password';
    CREATE DATABASE library_system OWNER username;
    \q
    ```

6. Dilni nga PostgreSQL:

    ```bash
    exit
    ```

## Krijimi i Skemës library_system

1. Hyni në PostgreSQL:

    ```bash
    psql -U username -d library_system
    ```

2. Krijo skemën library_system:

    ```sql
    CREATE SCHEMA library_system;
    ```

3. Krijo tabelat e nevojshme:
    Përdorni skedarët SQL të projektit për të krijuar tabelat (p.sh., books, loans, borrowers, etj.).

4. Dilni nga PostgreSQL:

    ```sql
    \q
    ```

## Instalimi i JupyterLab

1. Instaloni Python dhe pip (nëse nuk janë të instaluar):

    ```bash
    sudo apt install python3 python3-pip
    ```

2. Instaloni JupyterLab:

    ```bash
    pip install jupyterlab
    ```

3. Instaloni libraritë e nevojshme:

    ```bash
    pip install pandas sqlalchemy psycopg2 matplotlib
    ```

## Nisja e JupyterLab

1. Nisni JupyterLab:

    ```bash
    jupyter-lab
    ```

2. Hapni JupyterLab në shfletues:
    Shfletuesi do të hapet automatikisht në `http://localhost:8888/lab`.
    
    Nëse nuk hapet automatikisht, kopjoni URL-në që shfaqet në terminal dhe ngjisni në shfletues.

3. Hapni notebook-in `SystemofLibrary.ipynb`:
    Në JupyterLab, shkoni te drejtoria ku ndodhet projekti juaj.
    
    Klikoni dy herë në skedarin `SystemofLibrary.ipynb` për ta hapur.

## Përdorimi i Projektit

1. Importoni modulin `utils`:

    ```python
    import utils
    ```

2. Lidhuni me bazën e të dhënave:

    ```python
    engine = utils.get_db_connection()
    ```

3. Merrni librat më të huazuar:

    ```python
    borrowed_books_df = utils.get_most_borrowed_books(engine)
    ```

4. Vizualizoni të dhënat:

    ```python
    utils.plot_most_borrowed_books(borrowed_books_df)
    ```

## Kontributi

Nëse dëshironi të kontribuoni në këtë projekt, ju lutem ndiqni këto hapa:

1. Krijo një "fork" të depoz.
2. Krijo një degë (git checkout -b feature/EmriIRisise).
3. Bëni ndryshimet dhe bëni commit (git commit -m 'Shtoi ndryshimet e reja').
4. Pushoni degën (git push origin feature/EmriIRisise).
5. Hapni një "Pull Request".

## Licenca

Ky projekt është i licensuar nën licencën MIT.

## Kontakt

Për pyetje ose ndihmë, ju lutem kontaktoni:

**Kevin Dule**  
Email: kevindule1010@gmail.com  
GitHub: KevindCoder

Faleminderit që kontribuoni! 🚀
