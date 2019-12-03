from dataclasses import dataclass
from typing import List

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, Alignment

from src.team import Team

NORMAL_FONT = Font(name="Arial", size=10)
BOLD_FONT = Font(name="Arial", size=10, bold=True)
ALIGNMENT = Alignment(horizontal="center")


@dataclass
class RoundData:
    team1: Team
    team2: Team


class MatchData:

    def __init__(self):
        self.rounds: List[RoundData] = []

    def __str__(self):
        return f"MatchData({self.rounds})"

    def get_team_round_score(self, team: int, match_round: int) -> int:
        team_score = 0

        if team == 1:
            for player in self.rounds[match_round - 1].team1.players:  # TODO this might raise exception
                team_score += player.scores
        else:
            for player in self.rounds[match_round - 1].team2.players:
                team_score += player.scores

        return team_score


def save_to_file(workbook: Workbook, file_name: str):
    workbook.save(file_name)


def generate_report(match_data: MatchData):
    workbook = Workbook()
    sheet1 = workbook.active
    sheet2 = None

    _write_to_sheet(sheet1, match_data, team=1)

    # sheet1.cell(2, 2).font = BOLD_FONT
    # Set font first table

    save_to_file(workbook, "test.xls")


def _write_to_sheet(sheet: Worksheet, match_data: MatchData, team: int):
    # Merge top cells first table, but not rounds
    sheet.merge_cells(start_row=2, start_column=2, end_row=2, end_column=7)
    sheet.merge_cells(start_row=3, start_column=2, end_row=4, end_column=2)
    sheet.merge_cells(start_row=3, start_column=3, end_row=4, end_column=3)
    for col in range(2, 4 + len(match_data.rounds) * 2):
        sheet.merge_cells(start_row=5, start_column=col, end_row=6, end_column=col)
    # sheet1.merge_cells(start_row=4, start_column=4, end_row=4, end_column=5)

    # Merge top cells second table, but not rounds
    sheet.merge_cells(start_row=8, start_column=2, end_row=8, end_column=7)
    sheet.merge_cells(start_row=9, start_column=2, end_row=10, end_column=2)
    sheet.merge_cells(start_row=9, start_column=3, end_row=10, end_column=3)

    # For every match round merge the cells and enter the data
    match_round: RoundData
    for r, match_round in enumerate(match_data.rounds):  # r starts from 0
        round_team_score: int = match_data.get_team_round_score(team, r + 1)

        sheet.merge_cells(start_row=4, start_column=3 + r * 2, end_row=4, end_column=4 + r * 2)
        sheet.merge_cells(start_row=10, start_column=3 + r * 2, end_row=10, end_column=4 + r * 2)

        sheet.cell(4, 4 + r * 2, "Round " + str(r + 1))  # TODO this raises exception
        sheet.cell(5, 4 + r * 2, round_team_score)
        if team == 1:
            sheet.cell(5, 5 + r * 2, match_round.team1.time_out_requests)
        else:
            sheet.cell(5, 5 + r * 2, match_round.team2.time_out_requests)

        sheet.cell(10, 4 + r * 2, "Round " + str(r + 1))
        if team == 1:
            for i, player in enumerate(match_round.team1.players):
                sheet.cell(11 + i, 4 + r * 2, player.scores)
                sheet.cell(11 + i, 5 + r * 2, f"{player.yellow_cards}, {player.red_cards}")
        else:
            for i, player in enumerate(match_round.team2.players):
                sheet.cell(11 + i, 4 + r * 2, player.scores)
                sheet.cell(11 + i, 5 + r * 2, f"{player.yellow_cards}, {player.red_cards}")
