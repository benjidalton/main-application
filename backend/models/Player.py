class Player:
	def __init__(self, id, name, baseballReferenceUrl, pitcher) -> None:
		self.id = id
		self.name = name
		self.baseballReferenceUrl = baseballReferenceUrl
		self.pitcher = pitcher
		self.currentTeam = ''