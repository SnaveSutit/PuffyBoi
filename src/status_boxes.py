import discord



class StatusBox:
	def __init__(self, title, description, thumbnail, footer, author=None):
		self.embed = discord.Embed(
			title=title,
			description = description
		).set_thumbnail(
			url=thumbnail
		).set_footer(
			text=footer
		)

		if author:
			self.embed = self.embed.set_author(name=author.display_name, icon_url=author.avatar_url)

	def set_footer(self, footer):
		self.embed = self.embed.set_footer(text=footer)

	def set_thumbnail(self, thumbnail):
		self.embed = self.embed.set_thumbnail(url=thumbnail)

	def to_dict(self):
		return self.embed.to_dict()

