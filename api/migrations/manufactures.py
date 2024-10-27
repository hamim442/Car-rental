steps = [
    [
        # Create a table
        """--sql
        CREATE TABLE manufactures (
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL UNIQUE,
            logo_picture_url VARCHAR(300) NOT NULL
        );
        """,
        # Drop a table
        """--sql
        DROP TABLE IF EXISTS manufactures;
        """,
    ],
    [
        # Insert initial data
        """--sql
        INSERT INTO manufactures (name, logo_picture_url)
        VALUES
        ('Toyota', 'https://banner2.cleanpng.com/20180820/tl/98d2589ef1a427ad3211459d66121a22.webp');
        """,
        # "Down" SQL statement to delete all records and restart IDs
        """--sql
        TRUNCATE TABLE manufactures RESTART IDENTITY;
        """,
    ],
]
