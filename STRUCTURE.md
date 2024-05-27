/pokemon-project                # Root directory of your project
│
├── /app                        # Application code
│   ├── /api                    # Web route handlers and routing
│   │   ├── /endpoints          # Different routes (endpoints)
│   │   │   ├── pokemon.py      # Pokémon routes
│   │   │   └── trainer.py      # Trainer routes
│   │   └── deps.py             # Dependency injection (e.g., get_db)
│   │
│   ├── /core                   # Application configuration, startup events, etc.
│   │   └── config.py           # Configuration settings
│   │
│   ├── /crud                   # CRUD utils (create, read, update, delete)
│   │   ├── crud_pokemon.py     # Pokémon-specific CRUD operations
│   │   └── curd_trainer.py     # trainer-specific CRUD operations
│   │
│   ├── /db                     # Database-related modules
│   │   ├── create_tables.sql   # sql script to create the DB and tables in SQL
│   │   ├── migrate_json_to_sql.py   # python script to migrate the JSON to SQL
│   │   ├── pokemon_queries.py  # SQL queries related to pokemon
│   │   ├── trainer_queries.py  # SQL queries related to trainer
│   │   ├── database.py         # Database session management
│   │   └── pokemon_data.json   # source of local data
│   │
│   ├── /schemas                # Pydantic schemas for request/response validation
│   │   ├── pokemon.py          # Pokémon schemas
│   │   └── trainer.py          # Trainer schemas
│   │
│   └── main.py                 # FastAPI application creation and configuration
│
├── /tests                      # Test suite
│   ├── /test_api               # Tests for the API endpoints
│   │   ├── test_pokemon.py     # Tests for Pokémon endpoint
│   │   └── test_trainer.py     # Tests for Trainer endpoint
│   │
│   ├── /test_crud              # Tests for CRUD utilities
│   │
│   └── /test_db                # Tests for database interactions
│       └── test_models.py      # Tests SQLAlchemy models
│
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
└── README.md                   # Project overview and instructions
