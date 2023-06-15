import os

from django.apps import AppConfig
import pickle

from PFE_CODE.settings import BASE_DIR


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    workout_model = pickle.load(open(os.path.join(BASE_DIR, 'models/workout_model.bin'), 'rb'))
    workout_scaler = pickle.load(open(os.path.join(BASE_DIR, 'models/workout_scaler.bin'), 'rb'))
    #meal_model = pickle.load(open('models/meal_plan.bin','rb'))
