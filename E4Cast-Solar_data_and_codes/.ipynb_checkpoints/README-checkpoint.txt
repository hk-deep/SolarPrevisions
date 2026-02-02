Lexique:
-> GHI = Global Horizontal Irradiance (W/m2) (https://en.wikipedia.org/wiki/Solar_irradiance)
-> temp_air = température de l'air (degrés Celsius) à 2m au dessus du sol prévue par AROME et ARPEGE (modèles météorologiques de Météo-France)
-> wind_speed = vitesse du vent (m/s) à 10m au dessus du sol prévue par AROME et ARPEGE
-> Sirta = Centre de Mesure LMD / Polytechnique - coords: 48.713, 2.208 (https://sirta.ipsl.fr/fr/home-fr-2/)

Données disponibles:
-> Prévisions de GHI réalisées par le modèle E4Cast-Solar: Cros et al. (2020) Reliability Predictors for Solar Irradiance Satellite-Based Forecast. https://doi.org/10.3390/en13215566
-> Mesures de GHI réalisées au Sirta (https://sirta.ipsl.fr/renewable-energies/)
-> Prévisions de AROME et ARPEGE au niveau du Sirta pour (GHI / temp_air / wind_speed)
-> Prévisions de GHI sous hypothèse de persistence des nuages (Les nuages restent à leur place => modèle peu complexe)
-> Calcul GHI ciel clair à partir des variables astronomiques et de tendances climatiques (GHI prévu à la surface en l'absence de nuage)

Fichiers "csv" à deux dimensions:
-> Lignes = prévision initialisée à "initial_timeslot" enregistré en ISO8601 (https://fr.wikipedia.org/wiki/ISO_8601)
-> Colonnes = horizon de prévision enregistré en ISO8601 (https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.isoformat.html)

Exemple:
-> initial_timeslot, P0DT0H0M0S, P0DT0H15M0S, P0DT0H30M0S
-> 2021-04-02T08:41:00+00:00, 489.51, 524.67, 559.83
-> Signifie que le 02/04/2021 le GHI était de 489.51 à 08h41 (UTC), 524.67 à 08h56 (UTC) et 559.83 à 09h11 (UTC)

Pour les prévisions AROME et ARPEGE (GHI / temp_air / wind_speed):
-> La prévision initialisée le jour même à minuit est utilisée (run de 00PM - minuit à J+0).
-> Si elle n'est pas disponible, la prévision initialisée à midi la veille est utilisée (run de 00AM - midi à J-1).
