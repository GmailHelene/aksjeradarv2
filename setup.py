from setuptools import setup, find_packages

setup(
    name="aksjeradar",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-migrate",
        "flask-login",
        "gunicorn",
        "python-dotenv",
        "pandas",
        "matplotlib",
        "plotly",
        "yfinance",
        "requests",
        "Werkzeug",
        "openai",
        "fpdf",
        "newsapi-python",
        "numpy",
        "python-dateutil",
        "alembic",
    ],
)
