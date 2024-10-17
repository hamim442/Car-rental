steps = [
    [
        # Create a table
        """--sql
            CREATE TABLE manufactures (
                id serial primary key not null,
                name varchar(100) not null unique,
                logo_picture_url varchar(300) not null
            );
        """,
        # Drop a table
        """-sql
            DROP TABLE manufacture;
        """,
    ],
    [
        
    ]
]