from django.utils.safestring import mark_safe
from sqlalchemy import true
"""
自定义分页组，以后如果想要使用这个分页组件，你需要做如下几件事：

	#1. 根据自己的情况去筛选自己的数据
	queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

	#2. 实例化分页对象
	page_object = Pagination(request,queryset)
	
	page_queryset = page_object.page_queryset
	page_string = page_object.html()
	
	context = {
		"queryset":page_queryset, 
		"search_data":search_data, #分完页的数据
		"page_string":page_string   #页码
		}
	
	return render(request, "mobile_list.html", context)
	
	#在html页面中:
	<ul class="pagination">
            {{ page_string}}
          </ul>
"""
  

class Pagination(object):
	def __init__(self, request, queryset, page_size=10,page_param="page",plus=5):
		"""_summary_

		Args:
			request (_type_): 请求的对象
			queryset (_type_): 符合条件的数据（根据这个数据给他进行分页处理）
			page_size (int, optional): 每页显示多少条数据
			page_param (str, optional): 在URL中传递的获取分页的参数，例如/pretty/list/?page=12
			plus (int, optional):现实当前页的 前或后 几页（页码）
		"""
		import copy
		query_dict = copy.deepcopy(request.GET)
		query_dict._mutable = True
		self.query_dict = query_dict
  		#1. 根据用户想要访问的页码，计算出起止位置
		page = request.GET.get('page',"1")
		self.param = page_param
		if page.isdecimal():
			page = int(page)
		else:
			page = 1
		self.page = page
		self.page_size = page_size
		self.start = (page-1)*page_size
		self.end = page*page_size
		self.page_queryset = queryset[self.start:self.end]
  		#数据总条数
		total_count = queryset.count()
    
		total_page_num,div = divmod(total_count,page_size)
		if div:
			total_page_num += 1
			
		self.total_page_count = total_page_num
		self.plus = plus
	
	def html(self):
		 #计算出当前页的前5页，后5页
		#已经知道plus=5
		if self.total_page_count <= 2*self.plus+1:
			#数据库数据较少，总共不到11页
			start_page = 1
			end_page = self.total_page_count
		else:
			#当前页<5时
			if self.page <= self.plus:
				start_page = 1
				end_page = 2*self.plus 
			else:
				# 当前页 > 5
				# 当前页+5 > 总页码
				if(self.page+self.plus) > self.total_page_count:
					start_page = self.total_page_count - 2*self.plus
					end_page = self.total_page_count
				else:
					start_page = self.page - self.plus + 1
					end_page = self.page + self.plus
		page_str_list = []

		self.query_dict.setlist(self.param,[1])
		#print(self.query_dict.urlencode())
  
		first_page = '<li><a href="?{}">首页</span></a><li>'.format(self.query_dict.urlencode())
		if self.page > 1:
			self.query_dict.setlist(self.param,[self.page - 1])
			prev = '<li><a href="?{}">上一页</span></a><li>'.format(self.query_dict.urlencode())
		else:
			self.query_dict.setlist(self.param,[1])
			prev = '<li><a href="?{}">上一页</span></a><li>'.format(self.query_dict.urlencode())
		page_str_list.append(first_page)
		page_str_list.append(prev)
		for i in range (start_page, end_page+1):  
			self.query_dict.setlist(self.param,[i])
			if i==self.page:  
				ele = '<li class="active"><a href="?{}">{} </a></li>'.format(self.query_dict.urlencode(),i)    #/mobile/list/可以被忽略
			else:
				ele = '<li><a href="?{}">{} </a></li>'.format(self.query_dict.urlencode(),i)
			page_str_list.append(ele)
		if self.page < self.total_page_count:
			self.query_dict.setlist(self.param,[self.page+1])
			next = '<li><a href="?{}">下一页</span></a><li>'.format(self.query_dict.urlencode())
		else:
			self.query_dict.setlist(self.param,[self.total_page_count])
			next = '<li><a href="?{}">下一页</span></a><li>'.format(self.query_dict.urlencode())
		last_page = '<li><a href="?{}">尾页</span></a><li>'.format(self.query_dict.urlencode())
		page_str_list.append(next)
		page_str_list.append(last_page)
		page_string = mark_safe("".join(page_str_list))    #因为这里是个字符串，所以需要from django.utils.safestring import mark_safe来标记这个字符串是安全的
		return page_string
		'''
		页码
				<li><a href="/mobile/list/?page=1">1 </a></li>
				<li><a href="/mobile/list/?page=2">2 </a></li>
				<li><a href="/mobile/list/?page=3">3 </a></li>
				<li><a href="/mobile/list/?page=4">4 </a></li>
				<li><a href="/mobile/list/?page=5">5 </a></li>
		'''