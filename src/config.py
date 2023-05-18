import os

from environs import Env

env = Env()
env.read_env()

DB_HOST = env("DB_HOST")
DB_PORT = env("DB_PORT")
DB_NAME = env("DB_NAME")
DB_USER = env("DB_USER")
DB_PASS = env("DB_PASS")

REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")

SECRET = env('SECRET')
SECRET_ADMIN = env('SECRET_ADMIN')
