# utils.py
import pandas as pd
import random
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import time

# Funksione për Normalizimin e të Dhënave
def normalize_authors(df):
    """
    Normalizon të dhënat për tabelën 'authors'.
    """
    authors_df = df[['Author']].drop_duplicates().reset_index(drop=True)
    authors_df['author_id'] = authors_df.index + 1
    authors_df = authors_df.rename(columns={'Author': 'author_name'})
    return authors_df

def normalize_publishers(df):
    """
    Normalizon të dhënat për tabelën 'publishers'.
    """
    publishers_df = df[['Publisher']].drop_duplicates().reset_index(drop=True)
    publishers_df['publisher_id'] = publishers_df.index + 1
    publishers_df = publishers_df.rename(columns={'Publisher': 'publisher_name'})
    return publishers_df

def normalize_genres(df):
    """
    Normalizon të dhënat për tabelën 'genres'.
    """
    genres_df = df[['Genre']].drop_duplicates().reset_index(drop=True)
    genres_df['genre_id'] = genres_df.index + 1
    genres_df = genres_df.rename(columns={'Genre': 'genre_name'})
    return genres_df

def normalize_memberships(df):
    """
    Normalizon të dhënat për tabelën 'memberships'.
    """
    memberships_df = df[['Membership_Type']].drop_duplicates().reset_index(drop=True)
    memberships_df['membership_type_id'] = memberships_df.index + 1
    memberships_df = memberships_df.rename(columns={'Membership_Type': 'membership_type'})
    return memberships_df

def normalize_books(df, authors_df, publishers_df, genres_df):
    """
    Normalizon të dhënat për tabelën 'books'.
    """
    books_df = df[['Book_ID', 'Title', 'Author', 'Genre', 'ISBN', 'Publication_Year', 'Publisher', 'Copies_Available']]
    books_df = books_df.merge(authors_df, left_on='Author', right_on='author_name')
    books_df = books_df.merge(publishers_df, left_on='Publisher', right_on='publisher_name')
    books_df = books_df.merge(genres_df, left_on='Genre', right_on='genre_name')
    books_df = books_df.rename(columns={
        'Book_ID': 'book_id',
        'Title': 'title',
        'ISBN': 'isbn',
        'Publication_Year': 'publication_year',
        'Copies_Available': 'copies_available'
    })
    books_df = books_df[['book_id', 'title', 'author_id', 'genre_id', 'isbn', 'publication_year', 'publisher_id', 'copies_available']]
    return books_df

def normalize_borrowers(df, memberships_df):
    """
    Normalizon të dhënat për tabelën 'borrowers'.
    """
    borrowers_df = df[['Borrower_ID', 'Borrower_Name', 'Borrower_Age', 'Borrower_Gender', 'Membership_Type']]
    borrowers_df = borrowers_df.merge(memberships_df, left_on='Membership_Type', right_on='membership_type')
    borrowers_df = borrowers_df.rename(columns={
        'Borrower_ID': 'borrower_id',
        'Borrower_Name': 'borrower_name',
        'Borrower_Age': 'borrower_age',
        'Borrower_Gender': 'borrower_gender'
    })
    borrowers_df = borrowers_df[['borrower_id', 'borrower_name', 'borrower_age', 'borrower_gender', 'membership_type_id']]
    return borrowers_df

def normalize_loans(df):
    """
    Normalizon të dhënat për tabelën 'loans'.
    """
    loans_df = df[['Book_ID', 'Borrower_ID', 'Issued_Date', 'Due_Date', 'Return_Date', 'Fine_Amount']]
    loans_df = loans_df.rename(columns={
        'Book_ID': 'book_id',
        'Borrower_ID': 'borrower_id',
        'Issued_Date': 'issued_date',
        'Due_Date': 'due_date',
        'Return_Date': 'return_date',
        'Fine_Amount': 'fine_amount'
    })
    return loans_df

def normalize_fines(df):
    """
    Normalizon të dhënat për tabelën 'fines' bazuar në kolonën 'Fine_Amount' nga CSV.
    """
    fines_data = []
    for index, row in df.iterrows():
        if pd.notna(row['Fine_Amount']) and row['Fine_Amount'] > 0:  # Kontrollo nëse ka gjobe
            fines_data.append({
                'loan_id': index + 1,  # Supozojmë që 'loan_id' është i njëpasnjëshëm
                'fine_amount': row['Fine_Amount'],
                'paid': False  # Supozojmë që gjoba nuk është paguar fillimisht
            })
    return pd.DataFrame(fines_data)

def generate_reservations_data(books_df, borrowers_df):
    """
    Gjeneron të dhëna artificiale për tabelën 'reservations'.
    """
    reservations_data = []
    for _ in range(20):  # Gjenero 20 rezervime
        book = books_df.sample(1).iloc[0]
        borrower = borrowers_df.sample(1).iloc[0]
        reservation_date = datetime.now() - timedelta(days=random.randint(1, 30))
        status = random.choice(['Pending', 'Completed'])
        reservations_data.append({
            'book_id': book['book_id'],
            'borrower_id': borrower['borrower_id'],
            'reservation_date': reservation_date,
            'status': status
        })
    return pd.DataFrame(reservations_data)

def generate_reviews_data(loans_df):
    """
    Gjeneron të dhëna artificiale për tabelën 'reviews'.
    """
    reviews_data = []
    for index, row in loans_df.iterrows():
        if random.random() < 0.5:  # 50% e huazimeve kanë review
            rating = random.randint(1, 5)  # Vlerësimi nga 1 në 5
            review_text = f"This is a sample review for book {row['book_id']}."
            review_date = row['return_date'] if pd.notna(row['return_date']) else datetime.now()
            reviews_data.append({
                'book_id': row['book_id'],
                'borrower_id': row['borrower_id'],
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            })
    return pd.DataFrame(reviews_data)

# Funksione për Validimin e të Dhënave
def check_for_null_values(df):
    """
    Kontrollon nëse ka vlera null në DataFrame.
    """
    null_values = df.isnull().sum()
    if null_values.any():
        print("Vlerat null në secilën kolonë:")
        print(null_values)
        return False
    else:
        print("Nuk ka vlera null në të dhënat.")
        return True

def check_for_duplicates(df, column):
    """
    Kontrollon nëse ka dublika në një kolonë të caktuar.
    """
    duplicates = df[column].duplicated().sum()
    if duplicates > 0:
        print(f"Ka {duplicates} dublika në kolonën '{column}'.")
        return False
    else:
        print(f"Nuk ka dublika në kolonën '{column}'.")
        return True

def validate_date_format(df, column, date_format):
    """
    Validon nëse të dhënat në një kolonë janë në formatin e duhur të datës.
    """
    try:
        pd.to_datetime(df[column], format=date_format)
        print(f"Të dhënat në kolonën '{column}' janë në formatin e duhur të datës ({date_format}).")
        return True
    except ValueError:
        print(f"Gabim: Të dhënat në kolonën '{column}' nuk janë në formatin e duhur të datës ({date_format}).")
        return False

def validate_numeric_range(df, column, min_value, max_value):
    """
    Validon nëse të dhënat në një kolonë numerike janë brenda një intervali të caktuar.
    """
    if df[column].between(min_value, max_value).all():
        print(f"Të dhënat në kolonën '{column}' janë brenda intervalit [{min_value}, {max_value}].")
        return True
    else:
        print(f"Gabim: Të dhënat në kolonën '{column}' janë jashtë intervalit [{min_value}, {max_value}].")
        return False

def validate_unique_ids(df, column):
    """
    Validon nëse të gjitha ID-të në një kolonë janë unike.
    """
    if df[column].is_unique:
        print(f"Të gjitha ID-të në kolonën '{column}' janë unike.")
        return True
    else:
        print(f"Gabim: Ka ID të përsëritura në kolonën '{column}'.")
        return False

# Funksione për Futjen e të Dhënave në Bazën e të Dhënave
def insert_data_with_timing(engine, table_name, dataframe):
    """
    Fut të dhënat në një tabelë dhe mat kohën e futjes.
    """
    start_time = time.time()
    dataframe.to_sql(table_name, engine, if_exists='append', index=False, schema="library_system")
    end_time = time.time()
    print(f"Të dhënat janë futur në tabelën '{table_name}' në {end_time - start_time:.2f} sekonda.")

    # Lidhja me bazën e të dhënave PostgreSQL
def get_db_connection():
    db_url = 'postgresql://kevin:1234@localhost:5432/library_system'
    engine = create_engine(db_url)
    return engine

def get_most_borrowed_books(engine):
    query = """
    SELECT b.title, COUNT(*) AS borrow_count
    FROM library_system.loans l
    JOIN library_system.books b ON l.book_id = b.book_id
    GROUP BY b.title
    ORDER BY borrow_count DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, engine)
    return df

# Vizualizimi i të dhënave
def plot_most_borrowed_books(df):
    plt.figure(figsize=(10, 6))
    plt.barh(df['title'], df['borrow_count'], color='skyblue')
    plt.xlabel('Numri i Huazimeve')
    plt.ylabel('Titulli i Librit')
    plt.title('10 Librat Më të Huazuar')
    plt.gca().invert_yaxis()  # Për të shfaqur librin më të huazuar në krye
    plt.show()