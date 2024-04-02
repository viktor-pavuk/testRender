import json 
from typing import Optional
import requests
from fastapi import FastAPI, Response, HTTPException

import numpy as np

app = FastAPI()

class Game:
    def __init__(self, bet: int):
        self.board = np.array([0, 0, 0, 0, 0])
        self.bet = bet
        self.level = 1
        self.coin_value = 1

        self.values = {
            'scatter' :[0, 0, 0, 0, 0],
            'rogach' : [0, 0, 0, 0, 0],
            'bronze_coin' : [0, 0, 4, 10, 30],
            'black_coin' : [0, 0, 4, 10, 30],
            'silver_coin' : [0, 0, 4, 10, 30],
            'gold_coin' : [0, 0, 4, 10, 30],
            'bull' : [0, 0, 10, 30, 100],
            'eagle' : [0, 0, 10, 40, 110],
            'lion' : [0, 0, 10, 50, 120],
            'spearman' : [0, 0, 40, 100, 1000],
            'bulavist' : [0, 0, 40, 110, 1100],
            'mechnik' : [0, 0, 40, 120, 1200],
        }
        # 'scatter' 'rogach' 'wild'
        self.symbols = [ 'bronze_coin', 'black_coin', 'silver_coin', 'gold_coin', 'bull', 'lion', 'eagle', 'spearman', 'bulavist', 'mechnik']

        self.lines =           [[1, 1, 1, 1, 1],
                               [0, 0, 0, 0, 0],
                               [2, 2, 2, 2, 2],
                               [0, 1, 2, 1, 0],
                               [2, 1, 0, 1, 2],
                               [0, 1, 1, 1, 0],
                               [2, 1, 1, 1, 2],
                               [1, 0, 0, 0, 1],
                               [1, 2, 2, 2, 1],
                               [1, 1, 0, 1, 1],
                               [1, 1, 2, 1, 1],
                               [0, 0, 1, 0, 0],
                               [2, 2, 1, 2, 2],
                               [0, 1, 0, 1, 0],
                               [2, 1, 2, 1, 2],
                               [1, 0, 1, 0, 1],
                               [1, 2, 1, 2, 1],
                               [0, 2, 2, 2, 0],
                               [2, 0, 0, 0, 2],
                               [2, 2, 0, 2, 2]]
    def gen_board(self):
        length = len(self.symbols)
        self.board = np.random.randint(0,length,(3,5))

    def add_wilds(self):
        new_board = []
        for line in self.board:
            new_line = []
            for element in line:
                new_line.append(self.symbols[element])
            new_board.append(new_line)
        self.board = new_board
        if np.random.rand() < 0.50:
          for i in range(np.random.randint(1,4)):
            row = np.random.randint(0,3)
            column = np.random.randint(0,5)
            self.board[row][column] = 'wild'
        self.board = np.array(self.board)
        print()
        print(np.array(new_board))


    def print_balance(self):
        print(self.balance)

    def check_line(self, line):
      counter = 0
      symbol = [x for x in line if x != 'wild'][0]
      if not symbol:
        symbol = self.symbols[-1]
      line = [x if x != 'wild' else symbol for x in line]
      for i in range(1,5):
        if line[i] != symbol:
          break
        counter+=1
        
      return self.values[symbol][counter]


    def check_lines(self):
      result = []
      total_win = 0
      value = 0
      for line in self.lines:
        temp_line = []
        for column, row  in enumerate(line):
          temp_line.append(self.board[row][column])
        result.append(self.check_line(temp_line))
      return result


    def spin(self):
        self.gen_board()
        self.add_wilds()
        spin_result = self.check_lines()
        win = sum(spin_result)
        lines = [(x, self.lines[i]) for i,x in enumerate(spin_result) if x!=0]
        res = {'Board': self.board.tolist(),
               'Lines': lines,
               'Win': win}
        print(res)
        return res


@app.post('/spin')
async def extract_text(bet: int):
    g = Game(bet)
    spin_result = g.spin()
    res_json = json.dumps(spin_result, indent = 4)
    return Response(content=res_json, media_type="application/json")
