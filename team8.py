# Team 8, D15C0 
# Arjun Nemani 20161027
# Mashrukh Islam 20161137

import copy

class Team8():
	def __init__ (self):
		self.maxDepth = 4
		self.winPos = [
						[0,1,2,3],
						[4,5,6,7], 
		 				[8,9,10,11],
		 				[12,13,14,15],
		 				[0,4,8,12], 
		 				[1,5,9,13], 
		 				[2,6,10,14], 
		 				[3,7,11,15], 
		 				[6,9,11,14], 
		 				[5,8,10,13],
		 				[2,5,7,10],
		 				[1,4,6,9]
		 			  ]

		self.scoreTable = {
						'edge': 400,
						'corner': 600,		
						'center': 300,	
						'2inrow': 13,		
						'block2': 40,
						'3inrow': 49,
						'block3': 99,
						'win': 1000,
						}

		self.inf = 100000000
		self.goodMoves = []
		self.lolPos = []

	def getBlockCord(self, old_move):
		bx = old_move[0] / 4
		cx = old_move[0] % 4
		by = old_move[1] / 4
		cy = old_move[1] % 4
		return (bx,cx,by,cy)


	def Hfunc(self, board, flag, old_move):
		value = 0
		glaf = 'x' if flag == 'o' else 'o'

		blockCord = self.getBlockCord(old_move)
		self.lolPos = []
		bs = board.board_status
		for pos in self.winPos:
			a = [ pos[0] / 4 + blockCord[2] * 4, pos[0] % 4 + blockCord[0] * 4 ]
			b = [ pos[1] / 4 + blockCord[2] * 4, pos[1] % 4 + blockCord[0] * 4 ]
			c = [ pos[2] / 4 + blockCord[2] * 4, pos[2] % 4 + blockCord[0] * 4 ]
			d = [ pos[3] / 4 + blockCord[2] * 4, pos[3] % 4 + blockCord[0] * 4 ]
			
			self.lolPos.append((a,b,c,d))


		# evaluate win positions
		for (a,b,c,d) in self.lolPos:
			p = bs[a[0]][a[1]]
			q = bs[b[0]][a[1]]
			r = bs[c[0]][c[1]]
			s = bs[d[0]][d[1]]

			if bs[a[0]][a[1]] == flag and q == flag and r == flag and s == flag:
				value += self.scoreTable["win"]
			
			elif bs[a[0]][a[1]] == glaf and q == glaf and r == glaf and s == glaf:
				value -= self.scoreTable["win"]


		# evaluate three in rows
		for (a,b,c,d) in self.lolPos:
			p = bs[a[0]][a[1]]
			q = bs[b[0]][a[1]]
			r = bs[c[0]][c[1]]
			s = bs[d[0]][d[1]]

			# 3 of self in row, one blank
			if p == flag and q == flag and r == flag and s == '-':
				value += self.scoreTable["3inrow"]
			elif p == flag and q == flag and r == '-' and s == flag:
				value += self.scoreTable["3inrow"]
			elif p == flag and q == '-' and r == flag and s == flag:
				value += self.scoreTable["3inrow"]
			elif p == '-' and q == flag and r == flag and s == flag:
				value += self.scoreTable["3inrow"]

			# 3 of self in row, one blocked by opponent
			elif p == flag and q == flag and r == flag and s == glaf:
				value -= self.scoreTable["block3"]
			elif p == flag and q == flag and r == glaf and s == flag:
				value -= self.scoreTable["block3"]
			elif p == flag and q == glaf and r == flag and s == flag:
				value -= self.scoreTable["block3"]
			elif p == glaf and q == flag and r == flag and s == flag:
				value -= self.scoreTable["block3"]

			# 3 of opponent in row, one blank
			elif p == glaf and q == glaf and r == glaf and s == '-':
				value -= self.scoreTable["3inrow"]
			elif p == glaf and q == glaf and r == '-' and s == glaf:
				value -= self.scoreTable["3inrow"]
			elif p == glaf and q == '-' and r == glaf and s == glaf:
				value -= self.scoreTable["3inrow"]
			elif p == '-' and q == glaf and r == glaf and s == glaf:
				value -= self.scoreTable["3inrow"]

			# 3 of opponent in row, one blocked by self
			elif p == glaf and q == glaf and r == glaf and s == flag:
				value += self.scoreTable["block3"]
			elif p == glaf and q == glaf and r == flag and s == glaf:
				value += self.scoreTable["block3"]
			elif p == glaf and q == flag and r == glaf and s == glaf:
				value += self.scoreTable["block3"]
			elif p == flag and q == glaf and r == glaf and s == glaf:
				value += self.scoreTable["block3"]


		# evaluate two in rows
		for (a,b,c,d) in self.lolPos:
			p = bs[a[0]][a[1]]
			q = bs[b[0]][a[1]]
			r = bs[c[0]][c[1]]
			s = bs[d[0]][d[1]]

			# 2 of self in row, 2 blank
			if p == flag and q == flag and r == '-' and s == '-':
				value += self.scoreTable["2inrow"]
			elif p == flag and q == '-' and r == '-' and s == flag:
				value += self.scoreTable["2inrow"]
			elif p == '-' and q == '-' and r == flag and s == flag:
				value += self.scoreTable["2inrow"]
			elif p == '-' and q == flag and r == '-' and s == flag:
				value += self.scoreTable["2inrow"]
			elif p == '-' and q == flag and r == flag and s == '-':
				value += self.scoreTable["2inrow"]
			elif p == flag and q == '-' and r == flag and s == '-':
				value += self.scoreTable["2inrow"]
			
			# 2 of self in row, 1 blocked by opponent, 1 blank
			if p == flag and q == flag and r == glaf and s == '-':
				value -= self.scoreTable["block2"]
			elif p == flag and q == glaf and r == '-' and s == flag:
				value -= self.scoreTable["block2"]
			elif p == glaf and q == '-' and r == flag and s == flag:
				value -= self.scoreTable["block2"]
			elif p == glaf and q == flag and r == '-' and s == flag:
				value -= self.scoreTable["block2"]
			elif p == glaf and q == flag and r == flag and s == '-':
				value -= self.scoreTable["block2"]
			elif p == flag and q == glaf and r == flag and s == '-':
				value -= self.scoreTable["block2"]
			elif p == flag and q == flag and r == '-' and s == glaf:
				value -= self.scoreTable["block2"]
			elif p == flag and q == '-' and r == glaf and s == flag:
				value -= self.scoreTable["block2"]
			elif p == '-' and q == glaf and r == flag and s == flag:
				value -= self.scoreTable["block2"]
			elif p == '-' and q == flag and r == glaf and s == flag:
				value -= self.scoreTable["block2"]
			elif p == '-' and q == flag and r == flag and s == glaf:
				value -= self.scoreTable["block2"]
			elif p == flag and q == '-' and r == flag and s == glaf:
				value -= self.scoreTable["block2"]			

			# 2 of opponent in row, 2 blank
			if p == glaf and q == glaf and r == '-' and s == '-':
				value -= self.scoreTable["2inrow"]
			elif p == glaf and q == '-' and r == '-' and s == glaf:
				value -= self.scoreTable["2inrow"]
			elif p == '-' and q == '-' and r == glaf and s == glaf:
				value -= self.scoreTable["2inrow"]
			elif p == '-' and q == glaf and r == '-' and s == glaf:
				value -= self.scoreTable["2inrow"]
			elif p == '-' and q == glaf and r == glaf and s == '-':
				value -= self.scoreTable["2inrow"]
			elif p == glaf and q == '-' and r == glaf and s == '-':
				value -= self.scoreTable["2inrow"]

			# 2 of opponent in row, 1 blocked by self, 1 blank
			if p == glaf and q == glaf and r == flag and s == '-':
				value += self.scoreTable["block2"]
			elif p == glaf and q == flag and r == '-' and s == glaf:
				value += self.scoreTable["block2"]
			elif p == flag and q == '-' and r == glaf and s == glaf:
				value += self.scoreTable["block2"]
			elif p == flag and q == glaf and r == '-' and s == glaf:
				value += self.scoreTable["block2"]
			elif p == flag and q == glaf and r == glaf and s == '-':
				value += self.scoreTable["block2"]
			elif p == glaf and q == flag and r == glaf and s == '-':
				value += self.scoreTable["block2"]
			elif p == glaf and q == glaf and r == '-' and s == flag:
				value += self.scoreTable["block2"]
			elif p == glaf and q == '-' and r == flag and s == glaf:
				value += self.scoreTable["block2"]
			elif p == '-' and q == flag and r == glaf and s == glaf:
				value += self.scoreTable["block2"]
			elif p == '-' and q == glaf and r == flag and s == glaf:
				value += self.scoreTable["block2"]
			elif p == '-' and q == glaf and r == glaf and s == flag:
				value += self.scoreTable["block2"]
			elif p == glaf and q == '-' and r == glaf and s == flag:
				value += self.scoreTable["block2"]

		k = (blockCord[1], blockCord[0])

		if k in [(0,0), (3,0), (0,3), (3,3)]:
			value += self.scoreTable["corner"]
 
		# self edge
		elif k in [(1,0),(2,0),(0,1),(0,2),(1,3),(2,3),(3,1),(3,2)]:
			value += self.scoreTable["edge"]

		# self center
		elif k in [(1,1),(1,2),(2,1),(2,2)]:
			value += self.scoreTable["center"]

		return value

	def MiniMax(self, board, alpha, beta, isMaxPlayer, old_move, depth, flag):
		
		availableMoves = board.find_valid_move_cells(old_move)
		
		if len(availableMoves) >= 300:
			print "free move -- "+str(len(availableMoves))

		tempBoard = copy.deepcopy(board)
		
		if depth == 0:
			return self.Hfunc(tempBoard, flag, old_move)

		else:
			if isMaxPlayer:
				bestVal = -self.inf
				for move in availableMoves:
					tempBoard.update(old_move, move, flag)
					nexFlag = 'x' if flag == 'o' else 'o'
					value = self.MiniMax(tempBoard, alpha, beta, False, move, depth-1, nexFlag)
					if bestVal <= value:
						bestVal = value
						if(depth == self.maxDepth):
							self.goodMoves.append(move)
					alpha = max(bestVal, alpha)
					if beta <= alpha:
						break
				return bestVal
			else:
				bestVal = self.inf
				for move in availableMoves:
					tempBoard.update(old_move, move, flag)
					nexFlag = 'x' if flag == 'o' else 'o'
					value = self.MiniMax(tempBoard, alpha, beta, True, move, depth-1, nexFlag)
					if bestVal > value:
						bestVal = value
					beta = min(bestVal, beta)
					if beta <= alpha:
						break
				return bestVal
	
	def move(self, board, old_move, flag):
		if old_move == (-1,-1):
			return (5,11)
		self.goodMoves = []
		self.MiniMax(board, -self.inf, self.inf, True, old_move, self.maxDepth, flag)
		leng = len(self.goodMoves)
 		return self.goodMoves[leng-1]
		 
