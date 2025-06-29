import os
from setuptools import setup, find_packages

requirements = [
    "fastapi==0.110.0",
    "uvicorn==0.29.0",
    "python-multipart==0.0.7",
    "python-jose==3.3.0",
    "passlib[bcrypt]==1.7.4",
    "cryptography==41.0.3",
    "requests",
    "httpx==0.28.1",
    "SQLAlchemy==2.0.19",
    "psycopg2-binary==2.9.7",
    "python-dotenv==1.0.0",
    "aiofiles==23.2.1",
    "psutil==5.9.8",
    "PyYAML==6.0.1",
    "APScheduler==3.10.4",
    "aiohttp>=3.9.0",
    "aioredis>=2.0.0",
    "pydantic>=1.10.0",
    "pydantic-settings>=2.0.0",
]

setup(
    name="sheily_light_api",
    version="0.1.0",
    packages=find_packages(where='apps', include=['sheily_light_api*']),
    package_dir={'': 'apps'},
    install_requires=requirements,
    python_requires='>=3.8',
    author="Your Name",
    author_email="your.email@example.com",
    description="SHEILY Light API - FastAPI backend service",
    long_description=open('README.md').read() if os.path.exists('README.md') else "SHEILY Light API",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sheily-light",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
