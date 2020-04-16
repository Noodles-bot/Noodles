import yaml

with open('utils/config.yml', 'r', encoding='utf8') as config:
    con = yaml.safe_load(config)

conf = dict(con)