from distutils.core import setup

setup(
	name='pywall',
	version='0.1',
	packages=['pywall', 'pywall.wall', 'pywall.service', 'pywall.funnycats', 'pywall_tests'],
	url='https://github.com/pauloremoli/pywall',
	license='',
	install_requires=['jenkinsapi>=0.2.19', 'mongoengine>=0.8.7'],
	tests_require=['mock', 'nose', 'coverage'],
	author='Paulo Remoli',
	author_email='paulo.remoli@gmail.com',
	description='''Wall to visualize job\'s status from Jenkins with a continuous
	integration game that user scores points with good builds and loses points when broke the build.
	It's also included the "Wall of shame", it's a wall to show how much time since last broken and if there
	is a broken job who is responsible for that.'''
)
