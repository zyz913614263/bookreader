#coding:utf8
'''
Copyright (c) 2014 http://9miao.com All rights reserved.
'''

from gfirefly.server.globalobject import webserviceHandle,GlobalObject

class VNode:
	"""virtual node to manage all nc nodes"""
	def __init__(self, node_name):
		self.node_name = node_name
		self.called_count = 0

	def callNC(self,func_name,*args):
		print "current calling vnode::::" + self.node_name
		self.called_count += 1
		print self
		
		try:
			result = GlobalObject().root.callChild(self.node_name,func_name,*args)
		except Exception, e:
			return "timeout,please retry!"
		
		self.called_count -= 1
		return result

	def __repr__(self):
		return self.node_name+" --- "+str(self.called_count)


from gfirefly.utils.singleton import Singleton
class VNodeManger:
	"""node manager"""

	__metaclass__ = Singleton

	def __init__(self):
		self.vnodes_dict = {}
		self.init_nodes_dic()

	def init_nodes_dic(self):
		for child in GlobalObject().root.childsmanager._childs.values():
			child_name = child.getName()
			vnode = VNode(child_name)
			self.vnodes_dict[child_name]=vnode

	def reload_nodes(self):
		now_nodes_name = set(GlobalObject().root.childsmanager._childs.keys())
		old_nodes_name = set(self.vnodes_dict.keys())
		all_nodes_name = now_nodes_name|old_nodes_name
		died_nodes_name = old_nodes_name-(now_nodes_name&old_nodes_name)
		new_nodes_name = all_nodes_name-old_nodes_name
		for _nodename in died_nodes_name:
			del self.vnodes_dict[_nodename]
		for _nodename in new_nodes_name:
			vnode = VNode(_nodename)
			self.vnodes_dict[_nodename]=vnode

	def callNC(self,func_name,*args):
		bestVNode = self.getBestVNode()
		result = bestVNode.callNC(func_name,*args)
		return result

	def getBestVNode(self):
		self.reload_nodes()
		print "current all nodes::::::"+str(self.vnodes_dict.values())
		vlist = sorted(self.vnodes_dict.values(),key = lambda v:v.called_count)
		return vlist[0]


