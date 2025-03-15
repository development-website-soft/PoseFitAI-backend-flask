


import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = '5+v3AKBds942NJdnYRuPdvR2ORBoqZ8DrVvrfoc49kE='
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:MHeDtGXaGPejuOytQEEqAlzEtFfBxCop@tramway.proxy.rlwy.net:42624/railway'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '28rmoPJIuUoQD6uLhd/X2sQX+7+1ZHMH1oJcndxl2oo='
