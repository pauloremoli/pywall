from distutils.core import setup

setup(
	name='pywall',
	version='0.1.0',
	packages=['pywall', 'pywall.wall', 'pywall.service', 'pywall.funnycats', 'pywall.tests'],
	url='https://github.com/pauloremoli/pywall',
	license='',
	install_requires=['jenkinsapi>=0.2.19', 'mongoengine>=0.8.7', 'click>=0.7'],
	tests_require=['mock', 'nose', 'coverage'],
	author='Paulo Remoli',
	author_email='paulo.remoli@gmail.com',
	description='''PyWall is status monitor to Jenkins'''
)
