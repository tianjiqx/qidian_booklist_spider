
class UrlManager(object):

	# 分区数/进程数
	partion = 1;
	cursor = 0;
	def __init__(self,partion):
		# self.new_urls = set()
		# self.old_urls = set()

		self.partion = partion

		# 广度遍历而不用集合，用list
		self.new_urls = []
		self.old_urls = []
		for i in range(partion):
			self.new_urls.append([])
			self.old_urls.append([])

	def add_new_url(self,url):
		if url is None:
			return
		# for i in range(self.partion):
		if url not in self.new_urls[self.cursor] and url not in self.old_urls[self.cursor]:
			#self.new_urls.add(url)
			self.new_urls[self.cursor].append(url)
			print('add new url at', self.cursor, url)
			# 下一个url应该插入的位置
			self.cursor = (self.cursor + 1) % self.partion

			self.show()


	def add_new_urls(self,urls):
		if urls is None or len(urls) == 0:
			return
		for url in urls:
			self.add_new_url(url)

	def has_new_url(self,no):
		self.show()
		return len(self.new_urls[no]) != 0


	def get_new_url(self,i):
		# new_url = self.new_urls.pop()
		# self.old_urls.add(new_url)
		print('process ',i,'get_new_url')
		if len(self.new_urls[i]) != 0:
			new_url = self.new_urls[i].pop()
			self.old_urls[i].append(new_url)
			return new_url
		else:
			return None

	# 显示各分区各有多少url
	def show(self):
		for i in range(self.partion):
			print(i,"new url count =",len(self.new_urls[i]),"old url count =",len(self.old_urls[i]))


