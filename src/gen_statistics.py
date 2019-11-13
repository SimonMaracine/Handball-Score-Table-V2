import openpyxl

from src.team import Team

workbook = openpyxl.Workbook()
sheet = workbook.active


def save_to_file(file_name: str):
    workbook.save(file_name)


def generate_statistics(team1: Team, team2: Team):
    # sheet["A1"] = team1.
    pass
