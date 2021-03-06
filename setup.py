from setuptools import setup, find_packages

setup(
    name='jupyterhub-ltiauthenticator',
    version='1.0.1.dev',
    description='JupyterHub authenticator implementing LTI v1',
    url='https://github.com/fh-swf-hgi/jupyterhub-ltiauthenticator',
    author='Yuvi Panda',
    author_email='giefers.heiner@fh-swf.de',
    license='3 Clause BSD',
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'jupyterhub>=0.8',
        'oauthlib>=3.1',
        'lti>=0.9.5'
    ]
)
