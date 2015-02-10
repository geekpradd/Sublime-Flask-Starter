import sublime,sublime_plugin,os

FLASK_CODE='''from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()'''


class FlaskStarterBase(object):
	@staticmethod
	def createFolder(name,paths):
		if not len(paths):
			raise ValueError("No path data available from SideBar")
		else:
			path=paths[0]+'\\'+ name 
			if not os.path.exists(path):
				os.makedirs(path)
			return path
	@staticmethod
	def createSubFiles(name,path):
		dirs=[path+'\\static',path+'\\templates']
		for dir in dirs:
			if not os.path.exists(dir):
				os.makedirs(dir)
		appPath=path+'\\'+name+'.py'
		with open(appPath,'w') as f:
			f.write(FLASK_CODE)

class RelativeflaskCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		f=self.view.file_name()
		self.path=[self.getFolderName(f)]
		sublime.active_window().show_input_panel("Please enter Project Name:", '', lambda s: self.rest(s), None, None)
	def rest(self,name):
		folderName = FlaskStarterBase.createFolder(name,self.path)
		FlaskStarterBase.createSubFiles(name,folderName)
	def getFolderName(self,file):
		return file.replace(file.split('\\')[-1],'')

class NewflaskCommand(sublime_plugin.WindowCommand):
	def run(self, paths=[]):
		self.path=paths
		self.window.show_input_panel("Please enter Project Name:", '', lambda s: self.doRest(s), None, None)

	def doRest(self,name):
		folderName = FlaskStarterBase.createFolder(name,self.path)
		FlaskStarterBase.createSubFiles(name,folderName)

